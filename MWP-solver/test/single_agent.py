from swarm import Swarm


from swarm.types import Agent

cot_agent = Agent(
    name = "cot_agent",
    instructions = "请一步一步回答问题",
    model = "gpt-4o-mini"
)



client = Swarm()

response = client.run(
    agent=cot_agent,
    messages=[{"role": "user", "content": "请问，如何逐步解决一个方程？"}]
)

print(response.messages[-1]["content"])


