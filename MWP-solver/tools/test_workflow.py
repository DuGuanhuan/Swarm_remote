import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from swarm import Swarm
from agents.math_agents import strategy_analyzer, calculation_agent

def test_strategy_calculation_workflow():
    """测试策略分析和计算执行的工作流"""
    swarm = Swarm()
    
    # 测试用例
    test_case = {
        "name": "等差数列问题",
        "analysis": """
原始问题：
三个连续项的等差数列，最大项与最小项差14，每项加上最小项的一半后三数之和为120，求原始最小项。

问题分析：
这是一个涉及等差数列的应用题。

已知信息：
- 三项构成等差数列
- 最大项与最小项差14
- 每项加上最小项的一半后三数之和为120

求解目标：
- 求原始最小项的值

解题建议：
- 利用等差数列性质
- 设最小项为a，建立方程
"""
    }
    
    print(f"\n{'='*50}")
    print(f"测试案例: {test_case['name']}")
    
    # 1. 获取策略
    strategy_response = swarm.run(
        agent=strategy_analyzer,
        messages=[{
            "role": "user", 
            "content": f"基于以下问题分析结果，请提供解题策略和方程组：\n{test_case['analysis']}"
        }]
    )
    strategy = strategy_response.messages[-1]["content"]
    print("\n--- 策略分析结果 ---")
    print(strategy)
    
    # 2. 执行计算
    calculation_response = swarm.run(
        agent=calculation_agent,
        messages=[{
            "role": "user",
            "content": f"请根据以下策略和方程组进行计算：\n{strategy}"
        }]
    )
    calculation = calculation_response.messages[-1]["content"]
    print("\n--- 计算执行结果 ---")
    print(calculation)

if __name__ == "__main__":
    test_strategy_calculation_workflow() 