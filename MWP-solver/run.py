from swarm import Swarm
from swarm.types import Result
from agents import (
    # 问题分析专家
    geometry_analyzer,
    pattern_analyzer,
    algebra_analyzer,
    # 策略专家
    equation_strategist,
    visual_strategist,
    pattern_strategist,
    # 分析和策略的整合者
    analysis_integrator,
    strategy_integrator,
    # 其他智能体
    calculation_agent,
    verification_agent
)
from tools import solve_equations
import time
from typing import List, Dict

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

    try:
        # 1. 问题分析 - 多专家分析
        analysis_experts = [
            ("几何专家", geometry_analyzer),
            ("规律专家", pattern_analyzer),
            ("代数专家", algebra_analyzer)
        ]
        
        expert_analyses = {}
        
        if debug:
            print_step("Problem Analysis", "开始多专家分析问题...")
            start_time = time.time()
        
        for expert_name, expert in analysis_experts:
            response = swarm.run(
                agent=expert,
                messages=[{"role": "user", "content": problem_text}],
                context_variables=context
            )
            expert_analyses[expert_name] = response.messages[-1]["content"]
            
            if debug:
                print_step(f"{expert_name}分析结果", expert_analyses[expert_name])
        
        # 整合多专家分析结果
        response = swarm.run(
            agent=analysis_integrator,
            messages=[{"role": "user", "content": f"""
请整合以下专家对问题的分析结果：
{expert_analyses}
"""}],
            context_variables=context
        )
        integrated_analysis = response.messages[-1]["content"]
        
        if debug:
            print_step("Integrated Analysis", integrated_analysis)
            print(f"问题分析阶段总耗时: {time.time() - start_time:.2f}秒")
        
        results["problem_analysis"] = integrated_analysis

        # 2. 策略分析 - 多专家策略
        strategy_experts = [
            ("方程策略专家", equation_strategist),
            ("可视化策略专家", visual_strategist),
            ("规律策略专家", pattern_strategist)
        ]
        
        expert_strategies = {}
        
        if debug:
            print_step("Strategy Analysis", "开始多专家策略分析...")
            start_time = time.time()
        
        for expert_name, expert in strategy_experts:
            response = swarm.run(
                agent=expert,
                messages=[{"role": "user", "content": f"""
基于以下整合后的问题分析结果，请提供解题策略：
{integrated_analysis}
"""}],
                context_variables=context
            )
            expert_strategies[expert_name] = response.messages[-1]["content"]
            
            if debug:
                print_step(f"{expert_name}策略", expert_strategies[expert_name])
        
        # 整合多专家策略
        response = swarm.run(
            agent=strategy_integrator,
            messages=[{"role": "user", "content": f"""
请整合以下专家提供的解题策略：
{expert_strategies}
"""}],
            context_variables=context
        )
        integrated_strategy = response.messages[-1]["content"]
        
        if debug:
            print_step("Integrated Strategy", integrated_strategy)
            print(f"策略分析阶段总耗时: {time.time() - start_time:.2f}秒")
        
        results["strategy"] = integrated_strategy

        # 3. 计算执行
        if debug:
            print_step("Calculation", "正在执行计算...")
            start_time = time.time()
        
        response = swarm.run(
            agent=calculation_agent,
            messages=[{"role": "user", "content": f"""
请根据以下整合后的策略进行计算：
{integrated_strategy}
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
请验证以下完整解题过程和结果：
原始问题：
{problem_text}

整合后的问题分析：
{integrated_analysis}

整合后的解题策略：
{integrated_strategy}

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
