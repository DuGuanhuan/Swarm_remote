from sympy import solve, symbols, sympify
import re

def extract_equations(text):
    """从文本中提取数学公式"""
    equations = []
    pattern = r'([^=]+=[^,]+)'
    matches = re.finditer(pattern, text)
    for match in matches:
        eq = match.group(1).strip()
        equations.append(eq)
    return equations

def solve_equations(equations, target_var=None):
    """使用 SymPy 解方程组"""
    try:
        # print("\n=== 方程求解过程 ===")
        # print("输入方程组:", equations)
        
        sympy_eqs = []
        for eq in equations:
            left, right = eq.split('=')
            sympy_eq = sympify(f"{left}-({right})")
            sympy_eqs.append(sympy_eq)
            print(f"转换方程: {sympy_eq} = 0")
        
        all_symbols = set()
        for eq in sympy_eqs:
            all_symbols.update(eq.free_symbols)
        print("涉及的变量:", [str(s) for s in all_symbols])
            
        solution = solve(sympy_eqs, dict=True)
        print("原始解:", solution)
        
        # 筛选正数解
        positive_solutions = []
        for sol in solution:
            if all(v > 0 for v in sol.values()):
                positive_solutions.append(sol)
        print("正数解:", positive_solutions)
        
        if target_var:
            target_var = symbols(target_var)
            if positive_solutions:
                return {str(target_var): positive_solutions[0][target_var]}
            return {str(target_var): solution[0][target_var]}
            
        if positive_solutions:
            return {str(k): v for k, v in positive_solutions[0].items()}
        return {str(k): v for k, v in solution[0].items()}
    
    except Exception as e:
        return f"求解错误: {str(e)}"

__all__ = ["extract_equations", "solve_equations"] 