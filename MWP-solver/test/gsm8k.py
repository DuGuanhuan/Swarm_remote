from datasets import load_dataset
import random
import pandas as pd
import re
import os

# 设置随机种子确保可复现性
random.seed(42)

# 获取当前文件所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

def clean_answer(answer):
    """清理GSM8K答案格式，只保留最终数值"""
    # GSM8K的答案格式通常是: "Let's solve this step by step:\n1) First...\n2) Then...\n#### 答案"
    final_answer = answer.split('####')[-1].strip()
    # 提取数字（包括小数和负数）
    number = re.search(r'-?\d*\.?\d+', final_answer)
    return float(number.group()) if number else final_answer

def prepare_test_data(dataset, size=100):
    """准备测试数据集"""
    # 随机抽样
    sampled_indices = random.sample(range(len(dataset)), size)
    sampled_dataset = dataset.select(sampled_indices)
    
    # 构建DataFrame
    test_data = []
    for item in sampled_dataset:
        test_data.append({
            'question_id': len(test_data),
            'question': item['question'],
            'answer': clean_answer(item['answer']),
            'original_answer': item['answer']  # 保留原始答案供参考
        })
    
    return pd.DataFrame(test_data), sampled_indices

# 加载数据集
gsm8k_dataset = load_dataset("gsm8k", "main")
test_dataset = gsm8k_dataset['test']

# 准备测试数据
test_df, sampled_indices = prepare_test_data(test_dataset, size=100)

# 构建文件保存路径
test_csv_path = os.path.join(current_dir, "test_problems.csv")
indices_path = os.path.join(current_dir, "sampled_indices.txt")

# 保存数据
test_df.to_csv(test_csv_path, index=False)

# 保存采样索引以供复现
with open(indices_path, "w") as f:
    f.write(",".join(map(str, sampled_indices)))

print(f"测试数据集已保存到: {test_csv_path}")
print(f"采样索引已保存到: {indices_path}")
print(f"\n数据集示例:")
print(test_df.head())

# 示例：如何使用保存的数据集进行评估
def evaluate_model_answer(model_answer, true_answer, tolerance=1e-6):
    """评估模型答案是否正确"""
    try:
        model_num = float(model_answer)
        true_num = float(true_answer)
        return abs(model_num - true_num) <= tolerance
    except:
        return model_answer.strip() == true_answer.strip()

# 示例：计算准确率的函数
def calculate_accuracy(predictions, test_df):
    """计算模型预测的准确率
    
    Args:
        predictions: 模型预测结果的列表
        test_df: 测试数据集DataFrame
    
    Returns:
        float: 准确率
    """
    correct = 0
    total = len(test_df)
    
    for pred, true in zip(predictions, test_df['answer']):
        if evaluate_model_answer(pred, true):
            correct += 1
            
    return correct / total

# 使用示例
if __name__ == "__main__":
    # 模拟模型预测
    dummy_predictions = [1.0] * len(test_df)
    accuracy = calculate_accuracy(dummy_predictions, test_df)
    print(f"\n模拟评估准确率: {accuracy:.2%}")