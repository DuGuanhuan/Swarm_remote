from swarm import Swarm, Agent, Response
from swarm.types import Result

# --------------------- 工具函数 --------------------

def debate_argument_1() -> str:
    """
    Agent A 提出的论点
    假设 Agent A 支持观点："科技发展有助于人类进步"
    """
    return "科技发展促进了医疗、教育等领域的进步，帮助人类更好地解决全球性问题。"

def debate_argument_2() -> str:
    """
    Agent B 提出的论点
    假设 Agent B 持相反观点："科技发展也带来了一些负面影响"
    """
    return "虽然科技带来了许多好处，但过度依赖科技也导致了隐私问题、失业等问题，必须警惕这些负面影响。"

def debate_rebuttal_1() -> str:
    """
    Agent A 对 Agent B 观点的反驳
    """
    return "虽然科技有些负面影响，但其总体利益超过这些问题。比如，科技进步能创造更多的就业机会，发展自动化有助于提高生产效率。"

def debate_rebuttal_2() -> str:
    """
    Agent B 对 Agent A 观点的反驳
    """
    return "科技进步确实推动了效率，但忽视了对人类生活质量和社会结构的深远影响，过快的发展会加剧贫富差距。"

# --------------------- Agent 定义 --------------------

def agent_a_argument() -> Result:
    # Agent A 提出正方观点
    argument = debate_argument_1()
    return Result(value=argument)

def agent_b_argument() -> Result:
    # Agent B 提出反方观点
    argument = debate_argument_2()
    return Result(value=argument)

def agent_a_rebuttal() -> Result:
    # Agent A 对反方的反驳
    rebuttal = debate_rebuttal_1()
    return Result(value=rebuttal)

def agent_b_rebuttal() -> Result:
    # Agent B 对正方的反驳
    rebuttal = debate_rebuttal_2()
    return Result(value=rebuttal)

# --------------------- 主程序 ---------------------

# 创建两个 Agent：一个支持科技进步的正方观点，另一个持反方观点
agent_a = Agent(
    name="Agent A",
    model="gpt-4o-mini",
    instructions="你是一位支持科技发展的专家，请提出你支持的论点。",
    functions=[agent_a_argument, agent_a_rebuttal],  # 正方论点和反驳
)

agent_b = Agent(
    name="Agent B",
    model="gpt-4o-mini",
    instructions="你是一位关注科技负面影响的专家，请提出你反对科技发展的论点。",
    functions=[agent_b_argument, agent_b_rebuttal],  # 反方论点和反驳
)

def main():
    # 实例化 Swarm 客户端
    swarm = Swarm()

    # 初步问题定义：科技发展是否有益于人类？
    user_question = "科技发展是否有益于人类？"

    # 与 Agent A 进行首次对话，提出正方观点
    messages = [{"role": "user", "content": user_question}]
    print("==== [与 Agent A 交互] ====")
    response_a: Response = swarm.run(
        agent=agent_a,
        messages=messages,
        context_variables={},
        debug=True
    )

    # 查看 Agent A 输出的观点
    print("\n==== Agent A 输出 ====")
    for i, msg in enumerate(response_a.messages, start=1):
        print(f"Message {i} | role: {msg.get('role')} | content: {msg.get('content')}")

    # 与 Agent B 进行对话，提出反方观点
    print("\n==== [与 Agent B 交互] ====")
    response_b: Response = swarm.run(
        agent=agent_b,
        messages=response_a.messages,
        context_variables={},
        debug=True
    )

    # 查看 Agent B 输出的反方观点
    for i, msg in enumerate(response_b.messages, start=1):
        print(f"Message {i} | role: {msg.get('role')} | content: {msg.get('content')}")

    # Agent A 进行反驳
    print("\n==== [Agent A 反驳] ====")
    response_a_rebuttal: Response = swarm.run(
        agent=agent_a,
        messages=response_b.messages,
        context_variables={},
        debug=True
    )

    # 查看 Agent A 的反驳
    for i, msg in enumerate(response_a_rebuttal.messages, start=1):
        print(f"Message {i} | role: {msg.get('role')} | content: {msg.get('content')}")

    # Agent B 进行反驳
    print("\n==== [Agent B 反驳] ====")
    response_b_rebuttal: Response = swarm.run(
        agent=agent_b,
        messages=response_a_rebuttal.messages,
        context_variables={},
        debug=True
    )

    # 查看 Agent B 的反驳
    for i, msg in enumerate(response_b_rebuttal.messages, start=1):
        print(f"Message {i} | role: {msg.get('role')} | content: {msg.get('content')}")

    # 最终结论：结合双方论点，得出结论
    print("\n==== [最终结论] ====")
    conclusion = "经过双方的辩论，科技发展带来了一些负面影响，但总体来看，它推动了社会进步，带来了更高的生产效率和更好的生活质量。因此，应该有选择地管理科技发展，避免其带来的负面效应。"
    print(conclusion)

if __name__ == "__main__":
    main()
