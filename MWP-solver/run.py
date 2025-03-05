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
import logging
from typing import Dict, Any, Callable, List
import asyncio
from dataclasses import dataclass

@dataclass
class SolutionStep:
    name: str
    description: str
    agent: Callable
    message_template: str

class MathProblemSolver:
    def __init__(self, debug: bool = True):
        self.swarm = Swarm()
        self.debug = debug
        self.context = {}
        self.results = {}
        self.steps = [
            SolutionStep(
                name="Problem Analysis",
                description="开始分析问题...",
                agent=problem_analyzer,
                message_template="{problem_text}"
            ),
            SolutionStep(
                name="Strategy Analysis",
                description="正在生成解题策略...",
                agent=strategy_analyzer,
                message_template="基于以下问题分析结果，请提供解题策略和方程组：\n{problem_analysis}"
            ),
            # ... 其他步骤
        ]
    
    async def execute_step(self, step: SolutionStep, **kwargs) -> str:
        """执行单个解题步骤"""
        if self.debug:
            print_step(step.name, step.description)
            start_time = time.time()
        
        message = step.message_template.format(**kwargs)
        response = await self.swarm.run_async(
            agent=step.agent,
            messages=[{"role": "user", "content": message}],
            context_variables=self.context
        )
        result = response.messages[-1]["content"]
        
        if self.debug:
            print_step(f"{step.name} Complete", result)
            print(f"耗时: {time.time() - start_time:.2f}秒")
        
        return result

def solve_math_problem(problem_text: str, debug: bool = True) -> Dict[str, Any]:
    """
    使用多智能体系统解决数学问题
    
    Args:
        problem_text: 数学问题文本
        debug: 是否显示调试信息和进度
    
    Returns:
        Dict[str, Any]: 包含解题过程各步骤结果的字典
    """
    swarm = Swarm()
    context = {}
    results = {}
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    def print_step(step: str, content: str = None):
        """打印步骤信息"""
        if not debug:
            return
        logger.debug(f"\n{'='*50}")
        logger.debug(f"Step: {step}")
        if content:
            logger.debug(f"\nOutput:\n{content}")

    try:
        # 1. 问题分析
        if debug:
            print_step("Problem Analysis", "开始分析问题...")
            start_time = time.time()
        
        response = swarm.run(
            agent=problem_analyzer,
            messages=[{"role": "user", "content": problem_text}],
            context_variables=context
        )
        problem_analysis = response.messages[-1]["content"]
        
        if debug:
            print_step("Problem Analysis Complete", problem_analysis)
            print(f"耗时: {time.time() - start_time:.2f}秒")
        
        results["problem_analysis"] = problem_analysis

        # 2. 策略分析
        if debug:
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
        
        if debug:
            print_step("Strategy Analysis Complete", strategy)
            print(f"耗时: {time.time() - start_time:.2f}秒")
        
        results["strategy"] = strategy

        # 3. 计算执行
        if debug:
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
        
        if debug:
            print_step("Calculation Complete", calculation)
            print(f"耗时: {time.time() - start_time:.2f}秒")
        
        results["calculation"] = calculation

        # 4. 验证
        if debug:
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
        
        if debug:
            print_step("Verification Complete", verification)
            print(f"耗时: {time.time() - start_time:.2f}秒")
        
        results["verification"] = verification
        
    except Exception as e:
        error_msg = f"解题过程中发生错误: {str(e)}"
        if debug:
            print(f"\n{'='*50}\n{error_msg}\n{'='*50}")
        results["error"] = error_msg

    return results

async def solve_math_problem_async(problem_text: str, debug: bool = True) -> Dict[str, Any]:
    """异步版本的解题函数"""
    swarm = Swarm()
    context = {}
    results = {}
    
    try:
        # 1. 问题分析
        response = await swarm.run_async(
            agent=problem_analyzer,
            messages=[{"role": "user", "content": problem_text}],
            context_variables=context
        )
        problem_analysis = response.messages[-1]["content"]
        
        results["problem_analysis"] = problem_analysis

        # 2. 策略分析
        response = await swarm.run_async(
            agent=strategy_analyzer,
            messages=[{"role": "user", "content": f"""
基于以下问题分析结果，请提供解题策略和方程组：
{problem_analysis}
"""}],
            context_variables=context
        )
        strategy = response.messages[-1]["content"]
        
        results["strategy"] = strategy

        # 3. 计算执行
        response = await swarm.run_async(
            agent=calculation_agent,
            messages=[{"role": "user", "content": f"""
请根据以下策略和方程组进行计算：
{strategy}
"""}],
            context_variables=context
        )
        calculation = response.messages[-1]["content"]
        
        results["calculation"] = calculation

        # 4. 验证
        response = await swarm.run_async(
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
        
        results["verification"] = verification
        
    except Exception as e:
        logger.error(f"解题过程中发生错误: {str(e)}", exc_info=True)
        results["error"] = str(e)

    return results

def solve_math_problem(problem_text: str, debug: bool = True) -> Dict[str, Any]:
    """同步版本的解题函数"""
    return asyncio.run(solve_math_problem_async(problem_text, debug))

# 使用示例
if __name__ == "__main__":
    problem = """
Frederick is making popsicles to sell and to save money he is making his own popsicle sticks. He can get 200 sticks from a 2 x 4 piece of wood and 400 sticks from a 2 x 8 piece of wood. He has $24 to buy wood for sticks. A 2 x 4 costs $4. A 2 x 8 costs $6. What is the most popsicle sticks he can make if he buys the cheapest lumber?
   """
    
    print("\n开始解题...\n")
    print("问题：")
    print(problem)
    
    result = solve_math_problem(problem, debug=True)
    
    print("\n完整解题过程：")
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content)
