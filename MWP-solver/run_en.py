from swarm import Swarm
from swarm.types import Result
from agents import (
    problem_analyzer_en,
    strategy_analyzer_en,
    calculation_agent_en,
    verification_agent_en
)
from tools.math_tools_en import solve_equations
import time

def solve_math_problem(problem_text: str, debug: bool = True):
    """
    Use multi-agent system to solve math problems
    
    Args:
        problem_text: Math problem text
        debug: Whether to display debug info and progress
    """
    swarm = Swarm()
    context = {}
    results = {}

    def print_step(step: str, content: str = None):
        """Print step information"""
        if not debug:
            return
        print(f"\n{'='*50}")
        print(f"Step: {step}")
        if content:
            print(f"\nOutput:\n{content}")

    try:
        # 1. Problem Analysis
        if debug:
            print_step("Problem Analysis", "Starting problem analysis...")
            start_time = time.time()
        
        response = swarm.run(
            agent=problem_analyzer_en,
            messages=[{"role": "user", "content": problem_text}],
            context_variables=context
        )
        problem_analysis = response.messages[-1]["content"]
        
        if debug:
            print_step("Problem Analysis Complete", problem_analysis)
            print(f"Time taken: {time.time() - start_time:.2f}s")
        
        results["problem_analysis"] = problem_analysis

        # 2. Strategy Analysis
        if debug:
            print_step("Strategy Analysis", "Generating solution strategy...")
            start_time = time.time()
        
        response = swarm.run(
            agent=strategy_analyzer_en,
            messages=[{"role": "user", "content": f"""
Based on the following problem analysis, please provide solution strategy and equations:
{problem_analysis}
"""}],
            context_variables=context
        )
        strategy = response.messages[-1]["content"]
        
        if debug:
            print_step("Strategy Analysis Complete", strategy)
            print(f"Time taken: {time.time() - start_time:.2f}s")
        
        results["strategy"] = strategy

        # 3. Calculation
        if debug:
            print_step("Calculation", "Executing calculations...")
            start_time = time.time()
        
        response = swarm.run(
            agent=calculation_agent_en,
            messages=[{"role": "user", "content": f"""
Please calculate based on the following strategy and equations:
{strategy}
"""}],
            context_variables=context
        )
        calculation = response.messages[-1]["content"]
        
        if debug:
            print_step("Calculation Complete", calculation)
            print(f"Time taken: {time.time() - start_time:.2f}s")
        
        results["calculation"] = calculation

        # 4. Verification
        if debug:
            print_step("Verification", "Verifying results...")
            start_time = time.time()
        
        response = swarm.run(
            agent=verification_agent_en,
            messages=[{"role": "user", "content": f"""
Please verify the following solution process and results:
Original Problem:
{problem_text}

Problem Analysis:
{problem_analysis}

Solution Strategy and Equations:
{strategy}

Calculation Results:
{calculation}
"""}],
            context_variables=context
        )
        verification = response.messages[-1]["content"]
        
        if debug:
            print_step("Verification Complete", verification)
            print(f"Time taken: {time.time() - start_time:.2f}s")
        
        results["verification"] = verification
        
    except Exception as e:
        error_msg = f"Error occurred during solution process: {str(e)}"
        if debug:
            print(f"\n{'='*50}\n{error_msg}\n{'='*50}")
        results["error"] = error_msg

    return results

# Usage example
if __name__ == "__main__":
    problem = """
The owner of a Turkish restaurant wanted to prepare traditional dishes for an upcoming celebration. She ordered ground beef, in four-pound packages, from three different butchers. The following morning, the first butcher delivered 10 packages. A couple of hours later, 7 packages arrived from the second butcher. Finally, the third butcher's delivery arrived at dusk. If all the ground beef delivered by the three butchers weighed 100 pounds, how many packages did the third butcher deliver?
   """
    
    print("\nStarting solution...\n")
    print("Problem:")
    print(problem)
    
    result = solve_math_problem(problem, debug=True)
    
    print("\nComplete solution process:")
    for step, content in result.items():
        print(f"\n=== {step} ===")
        print(content) 