from sympy import solve, symbols, sympify, Rational, expand
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
    """求解方程组
    
    Args:
        equations: 方程组列表或单个方程字符串
        target_var: 目标求解变量（可选）
    
    Returns:
        包含以下字段的字典：
        - equations: 原始方程组
        - all_solutions: 所有解
        - positive_solutions: 所有正数解
        - target_value: 目标变量的值（如果指定了target_var）
        - error: 如果有错误会包含此字段
    """
    try:
        # 确保输入是列表
        if isinstance(equations, str):
            equations = [equations]
        
        # 预处理方程
        valid_equations = []
        for eq in equations:
            # 清理空格
            eq = eq.strip()
            # 确保方程包含等号
            if "=" not in eq:
                eq = f"{eq} = 0"
            valid_equations.append(eq)
        
        # 转换方程
        sympy_eqs = []
        for eq in valid_equations:
            try:
                # 检查是否包含等号
                if "=" not in eq:
                    return {"error": f"方程格式错误: 缺少等号, 方程: {eq}"}
                
                left, right = eq.split('=')
                # 先计算常数表达式
                left_expr = expand(sympify(left))
                right_expr = expand(sympify(right))
                # 创建标准形式方程：左侧-右侧=0
                sympy_eq = left_expr - right_expr
                sympy_eqs.append(sympy_eq)
                
                # 打印调试信息
                print(f"处理方程: {eq}")
                print(f"转换为: {sympy_eq}")
            except Exception as e:
                print(f"方程转换错误: {str(e)}, 方程: {eq}")
                return {"error": f"方程转换错误: {str(e)}, 方程: {eq}"}
        
        # 提取所有变量
        all_vars = set()
        for eq in sympy_eqs:
            all_vars.update(eq.free_symbols)
        
        # 如果没有变量，返回错误
        if not all_vars:
            return {"error": "方程中没有变量"}
        
        # 求解方程组
        solution = solve(sympy_eqs, list(all_vars), dict=True)
        
        # 如果没有解，返回错误
        if not solution:
            return {"error": "方程无解"}
        
        # 对于简单线性方程，添加手动验证
        if len(sympy_eqs) == 1 and len(all_vars) == 1 and len(solution) == 1:
            eq = sympy_eqs[0]
            var = list(all_vars)[0]
            
            # 检查是否为线性方程
            if eq.is_polynomial(var) and eq.as_poly(var).degree() == 1:
                # 提取系数和常数项
                coeff = eq.coeff(var, 1)
                constant = -eq.subs({var: 0})
                
                # 手动计算解
                if coeff != 0:  # 避免除以零
                    manual_sol = constant / coeff
                    
                    # 获取自动解
                    auto_sol = solution[0][var]
                    
                    # 比较自动解和手动解
                    if abs(float(auto_sol) - float(manual_sol)) > 1e-10:
                        print(f"警告：自动解 {auto_sol} 与手动解 {manual_sol} 不一致，使用手动解")
                        solution[0][var] = manual_sol
        
        # 验证所有解
        verified_solutions = []
        for sol in solution:
            valid = True
            for eq in sympy_eqs:
                # 将解代入方程检查是否接近零
                result = eq.subs(sol)
                if abs(float(result)) > 1e-10:
                    print(f"警告：解 {sol} 在方程 {eq} 中的结果为 {result}，不接近零")
                    valid = False
                    break
            if valid:
                verified_solutions.append(sol)
        
        # 如果验证后没有有效解，但原始解存在，使用原始解
        if not verified_solutions and solution:
            verified_solutions = solution
            print("警告：所有解验证失败，使用原始解")
        
        # 筛选正数解
        positive_solutions = []
        for sol in verified_solutions:
            if all(float(v) > 0 for v in sol.values()):
                positive_solutions.append(sol)
        
        # 转换结果为更易读的格式
        result = {
            "equations": valid_equations,
            "all_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in verified_solutions],
            "positive_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in positive_solutions]
        }
        
        # 如果指定了目标变量，添加目标变量的值
        if target_var:
            target_sym = symbols(target_var) if isinstance(target_var, str) else target_var
            target_var_str = str(target_sym)
            
            if verified_solutions:
                # 优先使用正数解
                if positive_solutions:
                    result["target_value"] = float(positive_solutions[0][target_sym])
                else:
                    result["target_value"] = float(verified_solutions[0][target_sym])
            else:
                return {"error": "无法求解目标变量"}
        
        return result
    
    except Exception as e:
        return {"error": f"求解错误: {str(e)}"} 