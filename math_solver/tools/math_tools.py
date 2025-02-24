from sympy import solve, symbols, sympify
import re
from math import gcd
from functools import reduce

def extract_equations(text):
    """
    从文本中提取数学公式
    """
    equations = []
    pattern = r'([^=]+=[^,]+)'
    matches = re.finditer(pattern, text)
    for match in matches:
        eq = match.group(1).strip()
        equations.append(eq)
    return equations

def solve_equations(equations, target_var=None):
    """
    使用 SymPy 解方程组
    """
    try:
        sympy_eqs = []
        for eq in equations:
            left, right = eq.split('=')
            sympy_eqs.append(sympify(f"{left}-({right})"))
        
        all_symbols = set()
        for eq in sympy_eqs:
            all_symbols.update(eq.free_symbols)
            
        solution = solve(sympy_eqs, dict=True)
        
        if target_var:
            target_var = symbols(target_var)
            return {str(target_var): solution[0][target_var]}
        return {str(k): v for k, v in solution[0].items()}
    except Exception as e:
        return f"求解错误: {str(e)}"

def calculate_gcd(*numbers):
    """
    计算多个数的最大公约数
    """
    return reduce(gcd, numbers)

def verify_gcd(gcd_value, *numbers):
    """
    验证GCD结果
    """
    for num in numbers:
        if num % gcd_value != 0:
            return False
    return True 