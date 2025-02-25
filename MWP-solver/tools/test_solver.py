import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from swarm import Agent, Swarm
from tools import solve_equations

test_agent = Agent(
    name="TestSolver",
    model="gpt-4o-mini",
    instructions="""你是一个简单的方程求解测试智能体。你的任务是测试 solve_equations 函数。

注意：方程格式要求
1. 必须使用 * 表示乘法
2. 等号两边必须是表达式
3. 所有方程必须放在列表中传入，即使是单个方程

请按照以下格式输出：
---
测试用例：
[描述测试的方程]

调用过程：
- 输入方程：[将方程放入列表中]
- 函数调用：solve_equations([具体的调用代码])
- 调用结果：[solve_equations 返回的结果]
- 结果分析：[分析返回结果是否符合预期]
---

示例：
1. 单个方程：solve_equations(["2*x + 3 = 7"])
2. 方程组：solve_equations(["x + y = 5", "2*x - y = 3"])

注意：即使是单个方程也要用列表形式，如 ["2*x + 3 = 7"]
""",
    functions=[solve_equations]
)

def run_test():
    """运行简单的测试用例"""
    swarm = Swarm()
    test_cases = [
        "求解方程：2*x + 3 = 7",
        "求解方程组：x + y = 5, 2*x - y = 3",
        "求解方程：4*a - 99 = 0"
    ]
    
    for case in test_cases:
        print("\n" + "="*50)
        print(f"测试案例: {case}")
        response = swarm.run(
            agent=test_agent,
            messages=[{
                "role": "user", 
                "content": f"""请使用正确的列表格式调用 solve_equations 函数求解以下方程：
{case}
记住：所有方程都必须放在列表中，即使是单个方程。"""
            }]
        )
        print(response.messages[-1]["content"])

if __name__ == "__main__":
    run_test() 