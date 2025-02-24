from swarm import Swarm
from agents.math_agents import (
    problem_analyzer,
    strategy_analyzer,
    calculation_agent,
    verification_agent
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