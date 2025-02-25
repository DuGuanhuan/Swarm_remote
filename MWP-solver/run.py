from swarm import Swarm
from swarm.types import Result
from agents import (
    problem_analyzer,
    strategy_analyzer,
    calculation_agent,
    verification_agent
)
from tools import solve_equations
import time

def solve_math_problem(problem_text: str, debug: bool = True):
    """
    使用多智能体系统解决数学问题
    
    Args:
        problem_text: 数学问题文本
        debug: 是否显示调试信息和进度
    """
    swarm = Swarm()
    context = {}
    results = {}

    def print_step(step: str, content: str = None):
        """打印步骤信息"""
        if not debug:
            return
        print(f"\n{'='*50}")
        print(f"Step: {step}")
        if content:
            print(f"\nOutput:\n{content}")

    # 1. 问题分析
    print_step("Problem Analysis", "开始分析问题...")
    start_time = time.time()
    response = swarm.run(
        agent=problem_analyzer,
        messages=[{"role": "user", "content": problem_text}],
        context_variables=context
    )
    problem_analysis = response.messages[-1]["content"]
    print_step("Problem Analysis Complete", problem_analysis)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    results["problem_analysis"] = problem_analysis

    # 2. 策略分析
    print_step("Strategy Analysis", "正在生成解题策略...")
    start_time = time.time()
    response = swarm.run(
        agent=strategy_analyzer,
        messages=[{"role": "user", "content": f"""
基于以下问题分析结果，请提供解题策略和方程组：
{problem_analysis}
"""}],
        context_variables=context
    )
    strategy = response.messages[-1]["content"]
    print_step("Strategy Analysis Complete", strategy)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    results["strategy"] = strategy

    # 3. 计算执行
    print_step("Calculation", "正在执行计算...")
    start_time = time.time()
    response = swarm.run(
        agent=calculation_agent,
        messages=[{"role": "user", "content": f"""
请根据以下策略和方程组进行计算：
{strategy}
"""}],
        context_variables=context
    )
    calculation = response.messages[-1]["content"]
    print_step("Calculation Complete", calculation)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    results["calculation"] = calculation

    # 4. 验证
    print_step("Verification", "正在验证结果...")
    start_time = time.time()
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
    print_step("Verification Complete", verification)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    results["verification"] = verification

    return results

# 使用示例
if __name__ == "__main__":
    problem = """
The owner of a Turkish restaurant wanted to prepare traditional dishes for an upcoming celebration. She ordered ground beef, in four-pound packages, from three different butchers. The following morning, the first butcher delivered 10 packages. A couple of hours later, 7 packages arrived from the second butcher. Finally, the third butcher’s delivery arrived at dusk. If all the ground beef delivered by the three butchers weighed 100 pounds, how many packages did the third butcher deliver?
   """
    
    print("\n开始解题...\n")
    print("问题：")
    print(problem)
    
    result = solve_math_problem(problem, debug=True)
    
    print("\n完整解题过程：")
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content)
