from swarm import Swarm, Agent
from swarm.types import Result
from sympy import solve, symbols, sympify
import re
from math import gcd
from functools import reduce

# 工具函数定义
def extract_equations(text):
    """
    从文本中提取数学公式
    """
    equations = []
    # 使用正则表达式匹配等式
    pattern = r'([^=]+=[^,]+)'
    matches = re.finditer(pattern, text)
    for match in matches:
        eq = match.group(1).strip()
        equations.append(eq)
    return equations

def solve_equations(equations, target_var=None):
    """
    使用 SymPy 解方程组
    
    Args:
        equations: 方程组列表
        target_var: 目标求解变量
    """
    try:
        # 将字符串方程转换为 SymPy 表达式
        sympy_eqs = []
        for eq in equations:
            left, right = eq.split('=')
            sympy_eqs.append(sympify(f"{left}-({right})"))
        
        # 获取方程中的所有符号
        all_symbols = set()
        for eq in sympy_eqs:
            all_symbols.update(eq.free_symbols)
            
        # 求解方程组
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

# 定义智能体

problem_analyzer = Agent(
    name="ProblemAnalyzer",
    model="gpt-4o-mini",
    instructions="""你是一个专业的数学问题分析专家。你的任务是：
1. 仔细阅读数学问题
2. 提取所有关键信息，包括：
   - 已知变量和它们的值
   - 未知变量
   - 问题要求求解的目标
3. 使用结构化的格式输出分析结果，格式如下：
   已知条件：
   - 变量1 = 值1
   - 变量2 = 值2
   未知变量：
   - 变量3
   - 变量4
   求解目标：
   - 需要求解的变量或表达式
   
请确保你的分析准确、完整，不遗漏任何重要信息。
"""
)

strategy_analyzer = Agent(
    name="StrategyAnalyzer",
    model="gpt-4o-mini",
    instructions="""你是一个数学解题策略专家。基于问题分析结果：
1. 确定解题方法和步骤
2. 列出所需的数学公式
3. 将公式转换为标准的代数方程形式（使用等号 = 连接）
4. 确保方程组是完整且可解的

输出格式：
解题策略：
1. 步骤1
2. 步骤2

方程组：
1. equation1: var1 = expression1
2. equation2: var2 = expression2

最终目标：
target_var = expression
"""
)

calculation_agent = Agent(
    name="CalculationAgent",
    model="gpt-4o-mini",
    instructions="""你是一个数学计算执行专家。你的任务是：
1. 使用 calculate_gcd 函数计算最大公约数
2. 使用 verify_gcd 函数验证结果
3. 展示详细的计算步骤
4. 确保结果的准确性

你可以使用以下工具：
- calculate_gcd: 计算最大公约数
- verify_gcd: 验证GCD结果
- solve_equations: 求解方程组
""",
    functions=[calculate_gcd, verify_gcd, solve_equations]
)

verification_agent = Agent(
    name="VerificationAgent",
    model="gpt-4o-mini",
    instructions="""你是一个数学结果验证专家。你的任务是：
1. 验证计算结果的合理性
2. 检查是否满足原始问题的所有条件
3. 代入原方程验证结果
4. 提供详细的验证步骤和结论

如果发现问题，请明确指出问题所在。
""",
    functions=[solve_equations]  # 用于验证计算
)

def solve_math_problem(problem_text: str):
    """
    使用多智能体系统解决数学问题
    """
    swarm = Swarm()
    context = {}
    
    # 1. 问题分析
    response = swarm.run(
        agent=problem_analyzer,
        messages=[{"role": "user", "content": problem_text}],
        context_variables=context
    )
    problem_analysis = response.messages[-1]["content"]
    
    # 2. 策略分析
    response = swarm.run(
        agent=strategy_analyzer,
        messages=[
            {"role": "user", "content": f"""
基于以下问题分析结果，请提供解题策略和方程组：
{problem_analysis}
"""}
        ],
        context_variables=context
    )
    strategy = response.messages[-1]["content"]
    
    # 3. 计算执行
    response = swarm.run(
        agent=calculation_agent,
        messages=[
            {"role": "user", "content": f"""
请根据以下策略和方程组进行计算：
{strategy}
"""}
        ],
        context_variables=context
    )
    calculation = response.messages[-1]["content"]
    
    # 4. 结果验证
    response = swarm.run(
        agent=verification_agent,
        messages=[
            {"role": "user", "content": f"""
请验证以下解题过程和结果：
原始问题：
{problem_text}

问题分析：
{problem_analysis}

解题策略和方程：
{strategy}

计算结果：
{calculation}
"""}
        ],
        context_variables=context
    )
    verification = response.messages[-1]["content"]
    
    return {
        "problem_analysis": problem_analysis,
        "strategy": strategy,
        "calculation": calculation,
        "verification": verification
    }

# 使用示例
if __name__ == "__main__":
    problem = """
    Find the smallest positive integer $n$ such that for every integer $m$ with $0 < m < 1993$, there exists an integer $k$ for which \[ \frac{m}{1993} < \frac{k}{n} < \frac{m+1}{1994}. \]
    """
    
    result = solve_math_problem(problem)
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content) 