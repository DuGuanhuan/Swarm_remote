import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from swarm import Agent, Swarm
from tools.math_tools import solve_equations

test_agent = Agent(
    name="TestSolver",
    model="gpt-4o-mini",
    instructions="""你是一个简单的方程求解测试智能体。你的任务是测试 solve_equations 函数。

请按照以下格式输出：
---
测试用例：
[描述测试的方程]

调用过程：
- 输入方程：[具体输入的方程]
- 调用结果：[solve_equations 返回的结果]
- 结果分析：[分析返回结果是否符合预期]
---

你可以使用以下工具：
{- solve_equations: 用于求解方程组，返回包含多种解的结果字典}
""",
    functions=[solve_equations]
)

def run_test():
    """运行简单的测试用例"""
    swarm = Swarm()  # 创建 Swarm 实例
    test_cases = [
        "求解方程：2*x + 3 = 7",
        "求解方程组：x + y = 5, 2*x - y = 3",
        "求解方程：4*a - 99 = 0"
    ]
    
    for case in test_cases:
        print("\n" + "="*50)
        print(f"测试案例: {case}")
        response = swarm.run(  # 使用 swarm.run 而不是直接调用 agent
            agent=test_agent,
            messages=[{"role": "user", "content": case}]
        )
        print(response.messages[-1]["content"])

if __name__ == "__main__":
    run_test() 