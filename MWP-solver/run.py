from swarm import Swarm
from swarm.types import Result
from agents import (
    problem_analyzer,
    strategy_analyzer,
    calculation_agent,
    verification_agent
)
from tools import solve_equations

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
        messages=[{"role": "user", "content": f"""
基于以下问题分析结果，请提供解题策略和方程组：
{problem_analysis}
"""}],
        context_variables=context
    )
    strategy = response.messages[-1]["content"]


    response = swarm.run(
        agent=calculation_agent,
        messages=[{"role": "user", "content": f"""
请根据以下策略和方程组进行计算：
{strategy}
"""}],
        context_variables=context
    )
    calculation = response.messages[-1]["content"]

    response = swarm.run(
        agent=verification_agent,
        messages=[{"role": "user", "content": f"""
请验证以下解题过程和结果：
原始问题：
{problem_text}

问题分析：
{problem_analysis}

解题策略和方程：
{strategy}

计算结果：
{calculation}
"""}],
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
    The largest and smallest of three consecutive terms in an arithmetic sequence differ by 14. Half of the smallest term is added to each term and the sum of the resulting three numbers is 120. What is the value of the original smallest term?
    """
    result = solve_math_problem(problem)
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content)
