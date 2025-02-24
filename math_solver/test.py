import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_solver.solver import solve_math_problem

def test_math_solver():
    problem = """
    Find the smallest positive integer $n$ such that for every integer $m$ with $0 < m < 1993$, there exists an integer $k$ for which \[ \frac{m}{1993} < \frac{k}{n} < \frac{m+1}{1994}. \]
    """
    
    result = solve_math_problem(problem)
    
    # 打印结果
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content)

if __name__ == "__main__":
    test_math_solver() 