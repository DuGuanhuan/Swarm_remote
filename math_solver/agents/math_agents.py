from swarm import Agent
from tools.math_tools import solve_equations, calculate_gcd, verify_gcd

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
    functions=[solve_equations]
) 