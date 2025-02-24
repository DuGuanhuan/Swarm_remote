from swarm import Swarm, Agent
from swarm.types import Result

# 创建 Swarm 实例
client = Swarm()


# 定义智能体之间的转换函数
def transfer_to_writer():
    """转换到作家智能体"""
    return writer


def transfer_to_critic():
    """转换到评论家智能体"""
    return critic


def transfer_to_secretary():
    """转换到秘书智能体"""
    return secretary


def save_story(story: str, context_variables: dict = None) -> Result:
    """保存故事内容"""
    return Result(
        value=f"Story saved: {story[:50]}...",
        context_variables={"story": story}
    )


def review_story(feedback: str, context_variables: dict = None) -> Result:
    """保存评论反馈"""
    return Result(
        value=f"Feedback saved: {feedback[:50]}...",
        context_variables={"feedback": feedback}
    )


# 定义秘书智能体
secretary = Agent(
    name="Secretary",
    model="gpt-4o-mini",
    instructions="""你是一个专业的秘书。
    你的职责是：
    1. 理解用户的写作需求
    2. 将需求转达给作家
    3. 在合适的时候将作品交给评论家审阅
    4. 协调作家和评论家的工作

    请用专业、礼貌的语气与用户和其他智能体交流。""",
    functions=[transfer_to_writer, transfer_to_critic]
)

# 定义作家智能体
writer = Agent(
    name="Writer",
    model="gpt-4o-mini",
    instructions="""你是一个富有创造力的作家。
    你的职责是：
    1. 根据秘书转达的需求创作故事
    2. 接受评论家的反馈并改进作品

    请发挥你的创造力，创作出生动有趣的故事。
    使用 save_story 函数保存你的作品。""",
    functions=[save_story, transfer_to_secretary]
)

# 定义评论家智能体
critic = Agent(
    name="Critic",
    model="gpt-4o-mini",
    instructions="""你是一个专业的文学评论家。
    你的职责是：
    1. 仔细阅读作家的作品
    2. 提供专业、建设性的反馈
    3. 指出作品的优点和可以改进的地方

    请用专业的文学术语进行点评，并使用 review_story 函数保存你的反馈。""",
    functions=[review_story, transfer_to_secretary]
)

# 开始对话
messages = [
    {
        "role": "user",
        "content": "我需要一个关于'友谊'主题的短故事，大约300字。"
    }
]

# 运行对话
response = client.run(
    agent=secretary,
    messages=messages,
    context_variables={},
    stream=False,  # 启用流式输出
    debug=True  # 启用调试信息
)

# 打印最终结果
for message in response.messages:
    if message["role"] == "assistant":
        print(f"\n{message['sender']}:", message["content"])
    elif message["role"] == "user":
        print("\nUser:", message["content"])