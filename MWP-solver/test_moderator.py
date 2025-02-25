from swarm import Agent, Swarm
from agents.math_agents import (
    problem_analyzer,
    strategy_analyzer, 
    calculation_agent,
    verification_agent
)

# 创建主持人智能体
moderator = Agent(
    name="Moderator",
    model="gpt-4o-mini",
    instructions="""你是一个数学问题解决的主持人。你需要评估问题并决定如何解决。

评估标准：
1. 简单问题：可以直接给出答案的基础计算或问题
2. 标准问题：需要分析和计算，但步骤明确
3. 复杂问题：需要多个智能体配合解决

可用的智能体：
- analyzer: 问题分析专家，擅长提取关键信息
- strategist: 策略制定专家，擅长构建方程
- calculator: 计算执行专家，擅长解方程
- verifier: 结果验证专家，擅长检查答案

你的职责：
1. 评估问题复杂度并选择合适的解题路径
2. 协调智能体工作，及时处理错误
3. 在需要时组织智能体讨论或辩论
4. 决定是否需要回溯或使用替代方案

特别注意：
1. 如果发现前序智能体的结果有问题，应立即组织相关智能体讨论
2. 在验证失败时，应该回溯到合适的步骤重新解决
3. 对于简单问题，可以直接给出答案或只调用必要的智能体
4. 保持对整个解题过程的把控，确保结果正确
"""
)

def solve_with_moderator(problem: str):
    """使用主持人模式解决数学问题"""
    swarm = Swarm()
    context = {
        "problem": problem,
        "history": [],
        "current_step": None,
        "retry_count": {}  # 记录每个步骤的重试次数
    }
    
    def run_debate(topic: str, participants: list):
        """组织智能体进行讨论"""
        print(f"\n=== 开始讨论：{topic} ===")
        messages = []
        for agent_name in participants:
            agent = globals()[f"{agent_name}"]
            response = swarm.run(
                agent=agent,
                messages=[{
                    "role": "user",
                    "content": f"请针对问题「{topic}」发表你的看法，参考历史记录：{context['history']}"
                }]
            )
            messages.append({"agent": agent_name, "content": response.messages[-1]["content"]})
            print(f"{agent_name}: {response.messages[-1]['content']}")
        
        # 让主持人总结讨论结果
        response = swarm.run(
            agent=moderator,
            messages=[{
                "role": "user",
                "content": f"请总结这次关于「{topic}」的讨论，并决定下一步行动"
            }],
            context_variables={"debate_messages": messages, **context}
        )
        return response.messages[-1]["content"]
    
    def handle_error(step: str, error: str):
        """处理错误，决定是否重试或回溯"""
        context["retry_count"][step] = context["retry_count"].get(step, 0) + 1
        
        if context["retry_count"][step] <= 2:  # 最多重试两次
            print(f"\n=== 处理错误：{step} - {error} ===")
            # 让主持人决定如何处理错误
            response = swarm.run(
                agent=moderator,
                messages=[{
                    "role": "user",
                    "content": f"在{step}步骤遇到错误：{error}，这是第{context['retry_count'][step]}次重试，请决定如何处理"
                }],
                context_variables=context
            )
            decision = response.messages[-1]["content"]
            
            if "讨论" in decision:
                # 组织相关智能体讨论
                participants = decision.split("讨论：")[1].split(",")
                result = run_debate(error, participants)
                return {"action": "retry", "new_context": result}
            elif "回溯" in decision:
                # 回溯到之前的步骤
                target_step = decision.split("回溯到")[1].split()[0]
                return {"action": "backtrack", "target": target_step}
            else:
                return {"action": "retry"}
        else:
            return {"action": "fail", "error": f"{step}步骤多次重试失败"}
    
    # 1. 让主持人评估问题
    response = swarm.run(
        agent=moderator,
        messages=[{"role": "user", "content": f"请评估这个问题：{problem}"}]
    )
    assessment = response.messages[-1]["content"]
    print("\n=== 问题评估 ===")
    print(assessment)
    
    # 2. 根据评估结果执行解题流程
    if "简单" in assessment:
        # 让主持人直接给出答案
        response = swarm.run(
            agent=moderator,
            messages=[{"role": "user", "content": "请直接解答这个问题"}]
        )
        return response.messages[-1]["content"]
        
    elif "标准" in assessment:
        while True:  # 允许回溯和重试
            try:
                # 让主持人制定解题计划
                response = swarm.run(
                    agent=moderator,
                    messages=[{"role": "user", "content": "请制定解题计划，说明需要调用哪些智能体"}]
                )
                plan = response.messages[-1]["content"]
                print("\n=== 解题计划 ===")
                print(plan)
                
                # 执行解题计划
                current_step = None
                for step in plan.split("\n"):
                    if not step.strip():
                        continue
                        
                    # 解析计划中的智能体
                    for agent_name in ["analyzer", "strategist", "calculator", "verifier"]:
                        if agent_name in step.lower():
                            current_step = agent_name
                            agent = globals()[f"{agent_name}"]
                            
                            print(f"\n=== 执行步骤：{agent_name} ===")
                            try:
                                # 调用智能体
                                response = swarm.run(
                                    agent=agent,
                                    messages=[{"role": "user", "content": step}],
                                    context_variables=context
                                )
                                result = response.messages[-1]["content"]
                                
                                # 让主持人评估结果
                                evaluation = swarm.run(
                                    agent=moderator,
                                    messages=[{
                                        "role": "user",
                                        "content": f"请评估{agent_name}的结果：{result}"
                                    }],
                                    context_variables=context
                                )
                                
                                if "错误" in evaluation.messages[-1]["content"]:
                                    error_handling = handle_error(current_step, evaluation.messages[-1]["content"])
                                    if error_handling["action"] == "fail":
                                        raise Exception(error_handling["error"])
                                    elif error_handling["action"] == "backtrack":
                                        # 清理历史记录到目标步骤
                                        while context["history"] and context["history"][-1]["agent"] != error_handling["target"]:
                                            context["history"].pop()
                                        break
                                    else:  # retry
                                        if "new_context" in error_handling:
                                            context.update(error_handling["new_context"])
                                        continue
                                
                                # 记录成功的结果
                                context["history"].append({
                                    "agent": agent_name,
                                    "result": result
                                })
                                print(result)
                                
                # 让主持人总结最终结果
                response = swarm.run(
                    agent=moderator,
                    messages=[{
                        "role": "user",
                        "content": "请总结解题过程，给出最终答案"
                    }],
                    context_variables=context
                )
                return response.messages[-1]["content"]
                
            except Exception as e:
                error_handling = handle_error(current_step or "unknown", str(e))
                if error_handling["action"] == "fail":
                    return f"解题失败：{error_handling['error']}"
                    
    else:  # 复杂问题
        # TODO: 实现完整的多智能体流程
        pass

# 测试用例
if __name__ == "__main__":
    # # 测试简单问题
    # simple_problem = "1加1等于多少？"
    # print("\n测试简单问题:", simple_problem)
    # result = solve_with_moderator(simple_problem)
    # print("结果:", result)
    
    # # 测试标准问题
    # standard_problem = "解方程：2x + 3 = 7"
    # print("\n测试标准问题:", standard_problem)
    # result = solve_with_moderator(standard_problem)
    # print("结果:", result)
    
    # 测试需要验证的问题
    verify_problem = "一个数加上它的两倍等于33，这个数是多少？"
    print("\n测试需要验证的问题:", verify_problem)
    result = solve_with_moderator(verify_problem)
    print("结果:", result) 