from sympy import solve, symbols, sympify, Rational, expand
import re

def extract_equations(text):
    """Extract mathematical equations from text"""
    equations = []
    pattern = r'([^=]+=[^,]+)'
    matches = re.finditer(pattern, text)
    for match in matches:
        eq = match.group(1).strip()
        equations.append(eq)
    return equations

def solve_equations(equations, target_var=None):
    """Solve system of equations
    
    Args:
        equations: List of equations or single equation string
        target_var: Target variable to solve for (optional)
    
    Returns:
        Dictionary containing:
        - equations: Original equations
        - all_solutions: All solutions
        - positive_solutions: All positive solutions
        - target_value: Value of target variable (if specified)
        - error: Error message if any
    """
    try:
        # Ensure input is list
        if isinstance(equations, str):
            equations = [equations]
        
        # Preprocess equations
        valid_equations = []
        for eq in equations:
            # Clean whitespace
            eq = eq.strip()
            # Ensure equation has equals sign
            if "=" not in eq:
                eq = f"{eq} = 0"
            valid_equations.append(eq)
        
        # Convert equations
        sympy_eqs = []
        for eq in valid_equations:
            try:
                # Check for equals sign
                if "=" not in eq:
                    return {"error": f"Invalid equation format: Missing equals sign, equation: {eq}"}
                
                left, right = eq.split('=')
                # Calculate constant expressions first
                left_expr = expand(sympify(left))
                right_expr = expand(sympify(right))
                # Create standard form equation: left-right=0
                sympy_eq = left_expr - right_expr
                sympy_eqs.append(sympy_eq)
                
                # Print debug info
                print(f"Processing equation: {eq}")
                print(f"Converted to: {sympy_eq}")
            except Exception as e:
                print(f"Equation conversion error: {str(e)}, equation: {eq}")
                return {"error": f"Equation conversion error: {str(e)}, equation: {eq}"}
        
        # Extract all variables
        all_vars = set()
        for eq in sympy_eqs:
            all_vars.update(eq.free_symbols)
        
        # Check for variables
        if not all_vars:
            return {"error": "No variables found in equations"}
        
        # Solve equation system
        solution = solve(sympy_eqs, list(all_vars), dict=True)
        
        # Check for solutions
        if not solution:
            return {"error": "No solution found"}
        
        # For simple linear equations, add manual verification
        if len(sympy_eqs) == 1 and len(all_vars) == 1 and len(solution) == 1:
            eq = sympy_eqs[0]
            var = list(all_vars)[0]
            
            # Check if linear equation
            if eq.is_polynomial(var) and eq.as_poly(var).degree() == 1:
                # Extract coefficient and constant term
                coeff = eq.coeff(var, 1)
                constant = -eq.subs({var: 0})
                
                # Manual solution
                if coeff != 0:  # Avoid division by zero
                    manual_sol = constant / coeff
                    
                    # Get automatic solution
                    auto_sol = solution[0][var]
                    
                    # Compare automatic and manual solutions
                    if abs(float(auto_sol) - float(manual_sol)) > 1e-10:
                        print(f"Warning: Automatic solution {auto_sol} differs from manual solution {manual_sol}, using manual solution")
                        solution[0][var] = manual_sol
        
        # Verify all solutions
        verified_solutions = []
        for sol in solution:
            valid = True
            for eq in sympy_eqs:
                # Substitute solution back into equation
                result = eq.subs(sol)
                if abs(float(result)) > 1e-10:
                    print(f"Warning: Solution {sol} gives result {result} in equation {eq}, not close to zero")
                    valid = False
                    break
            if valid:
                verified_solutions.append(sol)
        
        # If no verified solutions but original solutions exist, use original
        if not verified_solutions and solution:
            verified_solutions = solution
            print("Warning: No solutions passed verification, using original solutions")
        
        # Filter positive solutions
        positive_solutions = []
        for sol in verified_solutions:
            if all(float(v) > 0 for v in sol.values()):
                positive_solutions.append(sol)
        
        # Convert results to readable format
        result = {
            "equations": valid_equations,
            "all_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in verified_solutions],
            "positive_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in positive_solutions]
        }
        
        # If target variable specified, add its value
        if target_var:
            target_sym = symbols(target_var) if isinstance(target_var, str) else target_var
            target_var_str = str(target_sym)
            
            if verified_solutions:
                # Prefer positive solutions
                if positive_solutions:
                    result["target_value"] = float(positive_solutions[0][target_sym])
                else:
                    result["target_value"] = float(verified_solutions[0][target_sym])
            else:
                return {"error": "Could not solve for target variable"}
        
        return result
    
    except Exception as e:
        return {"error": f"Solution error: {str(e)}"} 