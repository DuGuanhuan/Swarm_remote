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
    """求解方程组
    
    Args:
        equations: 方程组列表或单个方程字符串
        target_var: 目标求解变量（可选）
    
    Returns:
        包含以下字段的字典：
        - equations: 原始方程组
        - all_solutions: 所有解
        - positive_solutions: 所有正数解
        - error: 如果有错误会包含此字段
        
    使用说明：
    1. 方程必须使用标准的代数表达式格式，不要使用 LaTeX 格式
    2. 正确的格式示例：
       - "3/2*a + 7 = 10"  # 不要写成 \frac{3}{2}a + 7 = 10
       - "x^2 + 2*x = 5"   # 不要写成 x² + 2x = 5
       - "2*x + y = 3"     # 不要写成 2x + y = 3
    3. 运算符号说明：
       - 乘法必须用 * 表示
       - 除法用 / 表示
       - 幂运算用 ^ 或 ** 表示
       - 变量和数字之间的乘法必须显式写出 *
       
    Examples:
        >>> solve_equations(["x + y = 5", "2*x - y = 3"])
        {'equations': ['x + y = 5', '2*x - y = 3'], 
         'all_solutions': [{'x': 2.6, 'y': 2.4}],
         'positive_solutions': [{'x': 2.6, 'y': 2.4}]}
        
        >>> solve_equations("4.5*a + 21 = 120")
        {'equations': ['4.5*a + 21 = 120'],
         'all_solutions': [{'a': 22.0}],
         'positive_solutions': [{'a': 22.0}]}
    """
    try:
        # 验证输入
        if not isinstance(equations, (list, tuple)):
            if isinstance(equations, str):
                equations = [equations]
            else:
                return {"error": "求解错误: 请提供有效的方程组"}
            
        # 预处理方程组
        valid_equations = []
        seen = set()
        for eq in equations:
            eq = eq.strip()
            
            # 标准化方程格式
            if '=' not in eq:
                eq = f"{eq} = 0"
                
            # 处理括号和表达式
            try:
                left, right = eq.split('=')
                left = left.strip()
                right = right.strip()
                
                # 展开括号，化简表达式
                left = str(sympify(left))
                right = str(sympify(right))
                
                # 确保乘法使用 *
                left = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', left)
                right = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', right)
                
                # 构建标准格式方程
                eq = f"{left} = {right}"
                
            except Exception as e:
                return {"error": f"方程格式错误: {str(e)}。请使用标准的代数表达式，如 '2*x + 3 = 7'"}
            
            if eq and eq not in seen:
                seen.add(eq)
                valid_equations.append(eq)
                
        if not valid_equations:
            return {"error": "求解错误: 没有有效的方程"}
            
        # 转换方程
        sympy_eqs = []
        for eq in valid_equations:
            try:
                left, right = eq.split('=')
                sympy_eq = sympify(f"{left}-({right})")
                sympy_eqs.append(sympy_eq)
            except Exception as e:
                return {"error": f"方程转换错误: {str(e)}"}
                
        if not sympy_eqs:
            return {"error": "求解错误: 无法转换方程"}
            
        # 求解方程组
        solution = solve(sympy_eqs, dict=True)
        
        if not solution:
            return {"error": "求解错误: 方程组无解"}
            
        # 筛选正数解
        positive_solutions = []
        for sol in solution:
            if all(v > 0 for v in sol.values()):
                positive_solutions.append(sol)
        
        # 返回结果
        result = {
            "equations": valid_equations,
            "all_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in solution],
            "positive_solutions": [{str(k): float(v) for k, v in sol.items()} for sol in positive_solutions]
        }
        
        if target_var:
            target_var = str(symbols(target_var))
            if positive_solutions:
                result["target_value"] = float(positive_solutions[0][target_var])
            else:
                result["target_value"] = float(solution[0][target_var])
                
        return result
    
    except Exception as e:
        return {"error": f"求解错误: {str(e)}"} 