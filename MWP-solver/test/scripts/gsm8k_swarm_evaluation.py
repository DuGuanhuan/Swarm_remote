import random
import json
from datasets import load_dataset
from swarm import Swarm
from swarm.types import Agent

# 加载 gsm8k 数据集
gsm8k_dataset = load_dataset("gsm8k", "main")
test_dataset = gsm8k_dataset['test']

# 设置固定的随机种子
random.seed(42)

# 随机抽取 100 条数据
sampled_data = random.sample(test_dataset, 100)


# 保存抽取的数据到文件
def save_sampled_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# 从文件加载抽取的数据
def load_sampled_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# 保存抽取的数据
save_sampled_data(sampled_data, 'sampled_data.json')

# 初始化 cot_agent
cot_agent = Agent(
    name="cot_agent",
    instructions="请一步一步回答问题",
    model="gpt-4o-mini"
)

# 创建 Swarm 客户端
client = Swarm()

# 存储预测结果和真实答案
predictions = []
true_answers = []

# 对每条数据进行预测
for item in sampled_data:
    question = item['question']
    true_answer = item['answer'].split('#### ')[-1].strip()  # 提取答案中的数字部分

    response = client.run(
        agent=cot_agent,
        messages=[{"role": "user", "content": f"请问，{question}"}]
    )

    prediction = response.messages[-1]["content"]

    predictions.append(prediction)
    true_answers.append(true_answer)


# 计算准确率
def calculate_accuracy(predictions: List[str], true_answers: List[str]) -> float:
    correct = sum(1 for pred, true in zip(predictions, true_answers) if str(pred).strip() == str(true).strip())
    return correct / len(predictions)


accuracy = calculate_accuracy(predictions, true_answers)
print(f"Accuracy: {accuracy:.2%}")

# 打印一些预测结果和真实答案
for i in range(5):
    print(f"Question: {sampled_data[i]['question']}")
    print(f"True Answer: {true_answers[i]}")
    print(f"Predicted Answer: {predictions[i]}\n")

# 从文件加载数据并进行测试
loaded_data = load_sampled_data('sampled_data.json')
print("Loaded data sample:")
print(loaded_data[0])
