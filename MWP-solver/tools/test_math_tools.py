from math_tools import solve_equations

def test_solve_equations():
    """测试方程求解函数"""
    test_cases = [
        {
            "name": "简单一元方程",
            "equations": ["2*x + 3 = 7"],
            "expected": 2
        },
        {
            "name": "带小数的方程",
            "equations": ["4.5*a + 21 = 120"],
            "expected": 22
        },
        {
            "name": "二元方程组",
            "equations": ["x + y = 5", "2*x - y = 3"],
            "expected_x": 2.6,
            "expected_y": 2.4
        },
        {
            "name": "等差数列问题",
            "equations": ["4.5*a + 21 = 120"],
            "expected": 22
        }
    ]

    for case in test_cases:
        print(f"\n测试用例: {case['name']}")
        print(f"输入方程: {case['equations']}")
        
        result = solve_equations(case['equations'])
        print(f"返回结果: {result}")
        
        if "error" in result:
            print(f"错误: {result['error']}")
            continue
            
        if result["positive_solutions"]:
            print("正数解:", result["positive_solutions"])
        print("所有解:", result["all_solutions"])

def test_latex_equations():
    """测试 LaTeX 格式方程的处理"""
    test_cases = [
        {
            "name": "分数形式",
            "latex": r"\frac{3}{2}x + 7 = 10",
            "expected": "求解错误",
            "correct": "3/2*x + 7 = 10"
        },
        {
            "name": "幂运算",
            "latex": r"x^2 + 2x + 1 = 0",
            "expected": "求解错误",
            "correct": "x**2 + 2*x + 1 = 0"
        },
        {
            "name": "复杂表达式",
            "latex": r"\frac{3}{2}a + (\frac{3}{2}a + 7) + (\frac{3}{2}a + 14) = 120",
            "expected": "求解错误",
            "correct": "3/2*a + (3/2*a + 7) + (3/2*a + 14) = 120"
        },
        {
            "name": "隐式乘法",
            "latex": "2x + 3y = 10",
            "expected": "求解错误",
            "correct": "2*x + 3*y = 10"
        }
    ]

    print("\n=== 测试 LaTeX 格式方程 ===")
    for case in test_cases:
        print(f"\n测试用例: {case['name']}")
        print(f"LaTeX 格式: {case['latex']}")
        print(f"正确格式: {case['correct']}")
        
        # 测试错误格式
        result = solve_equations(case['latex'])
        print(f"错误格式结果: {result}")
        
        # 测试正确格式
        result = solve_equations(case['correct'])
        print(f"正确格式结果: {result}")

def test_complex_equations():
    """测试复杂方程的求解"""
    test_cases = [
        {
            "name": "带括号的复杂表达式",
            "equation": ["0.5*a + a + 0.5*a + (a + 7) + 0.5*a + (a + 14) = 120"],
            "expected": 22
        },
        {
            "name": "化简后的表达式",
            "equation": ["4.5*a + 21 = 120"],
            "expected": 22
        }
    ]
    
    for case in test_cases:
        print(f"\n测试用例: {case['name']}")
        print(f"输入方程: {case['equation']}")
        
        result = solve_equations(case['equation'])
        print(f"返回结果: {result}")
        
        if 'error' in result:
            print(f"错误信息: {result['error']}")
        else:
            solution = result['all_solutions'][0]['a']
            print(f"求解结果: a = {solution}")
            print(f"是否正确: {'✓' if abs(solution - case['expected']) < 0.0001 else '✗'}")

def main():
    # 测试单个方程
    print("=== 测试单个方程 ===")
    eq = "4.5*a + 21 = 120"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")
    
    # 测试方程组
    print("\n=== 测试方程组 ===")
    eqs = ["x + y = 5", "2*x - y = 3"]
    print(f"测试方程组: {eqs}")
    result = solve_equations(eqs)
    print(f"结果: {result}")
    
    # 测试带小数的方程
    print("\n=== 测试带小数的方程 ===")
    eq = "1.5*x = 3"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")
    
    # 测试分数系数的方程
    print("\n=== 测试分数系数的方程 ===")
    eq = "3/2*a + (3/2*a + 7) + (3/2*a + 14) = 120"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")

    # 测试错误格式的方程（这种格式会导致错误）
    print("\n=== 测试错误格式的方程 ===")
    eq = r"\frac{3}{2}a + 7 = 10"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")
    
    # 添加 LaTeX 测试
    test_latex_equations()

    # 测试复杂方程
    print("\n=== 测试复杂方程 ===")
    eq = "3/2*a + (3/2*a + 7) + (3/2*a + 14) = 120"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")

    # 测试正确的代数格式
    print("\n=== 测试正确的代数格式 ===")
    eq = "3/2*a + 7 = 10"
    print(f"测试方程: {eq}")
    result = solve_equations(eq)
    print(f"结果: {result}")

    # 运行所有测试用例
    print("\n=== 运行所有测试用例 ===")
    test_solve_equations()

    # 测试复杂方程的求解
    test_complex_equations()

if __name__ == "__main__":
    main() 