import os
import pandas as pd
import re
from swarm import Swarm
from swarm.types import Agent
import time
from tqdm import tqdm

# 获取当前文件所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建CoT代理
cot_agent = Agent(
    name="cot_agent",
    instructions="请解决这个数学问题。先一步一步思考，然后给出最终答案。在最后，请用'最终答案：X'的格式明确标出你的答案，其中X是你计算得到的数值。",
    model="gpt-4o-mini"
)

# 从大模型回答中提取最终答案
def extract_answer(response_text):
    """从大模型的回答中提取最终答案"""
    # 尝试匹配"最终答案：X"格式
    final_answer_match = re.search(r'最终答案[:：]\s*([\d\.\-]+)', response_text)
    if final_answer_match:
        return final_answer_match.group(1)
    
    # 尝试匹配"答案是X"格式
    answer_is_match = re.search(r'答案是\s*([\d\.\-]+)', response_text)
    if answer_is_match:
        return answer_is_match.group(1)
    
    # 尝试匹配"= X"格式（通常在计算的最后一步）
    equals_match = re.search(r'=\s*([\d\.\-]+)(?!\d*\s*[+\-*/])', response_text)
    if equals_match:
        return equals_match.group(1)
    
    # 尝试匹配任何数字（最后的手段）
    numbers = re.findall(r'([\d\.\-]+)', response_text)
    if numbers:
        return numbers[-1]  # 返回最后一个数字
    
    return "无法提取答案"

# 评估模型答案是否正确
def evaluate_model_answer(model_answer, true_answer, tolerance=1e-6):
    """评估模型答案是否正确"""
    try:
        model_num = float(model_answer)
        true_num = float(true_answer)
        return abs(model_num - true_num) <= tolerance
    except:
        return model_answer.strip() == true_answer.strip()

def main():
    # 加载测试数据
    test_csv_path = os.path.join(current_dir, "test_problems.csv")
    test_df = pd.read_csv(test_csv_path)
    
    # 使用全部100个问题
    print(f"开始测试全部 {len(test_df)} 个问题...")
    
    # 初始化Swarm客户端
    client = Swarm()
    
    # 存储结果
    results = []
    
    # 使用tqdm显示进度条
    for idx, row in tqdm(test_df.iterrows(), total=len(test_df), desc="测试进度"):
        question = row['question']
        true_answer = row['answer']
        question_id = row['question_id']
        
        try:
            # 调用大模型
            response = client.run(
                agent=cot_agent,
                messages=[{"role": "user", "content": question}]
            )
            
            # 获取模型回答
            model_response = response.messages[-1]["content"]
            
            # 提取答案
            extracted_answer = extract_answer(model_response)
            
            # 评估答案
            is_correct = evaluate_model_answer(extracted_answer, true_answer)
            
            # 存储结果
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'model_response': model_response,
                'extracted_answer': extracted_answer,
                'is_correct': is_correct
            })
            
            # 简短打印结果
            print(f"问题 {question_id}: {'✓' if is_correct else '✗'} (预测: {extracted_answer}, 正确: {true_answer})")
            
            # 添加短暂延迟，避免API限制
            time.sleep(0.5)
            
        except Exception as e:
            print(f"处理问题 {question_id} 时出错: {str(e)}")
            # 记录错误情况
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'model_response': f"错误: {str(e)}",
                'extracted_answer': "错误",
                'is_correct': False
            })
            time.sleep(1)  # 出错时等待时间更长
    
    # 计算准确率
    correct_count = sum(result['is_correct'] for result in results)
    accuracy = correct_count / len(results)
    print(f"\n总体准确率: {accuracy:.2%} ({correct_count}/{len(results)})")
    
    # 保存详细结果
    results_df = pd.DataFrame(results)
    results_path = os.path.join(current_dir, "full_evaluation_results.csv")
    results_df.to_csv(results_path, index=False)
    print(f"详细结果已保存到: {results_path}")
    
    # 保存简化版结果（不包含完整的模型回答）
    simplified_results = results_df[['question_id', 'question', 'true_answer', 'extracted_answer', 'is_correct']]
    simplified_path = os.path.join(current_dir, "simplified_results.csv")
    simplified_results.to_csv(simplified_path, index=False)
    print(f"简化结果已保存到: {simplified_path}")
    
    # 创建结果摘要
    summary = {
        '总问题数': len(results),
        '正确数量': correct_count,
        '准确率': accuracy,
        '测试模型': cot_agent.model,
        '测试时间': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 保存摘要
    summary_df = pd.DataFrame([summary])
    summary_path = os.path.join(current_dir, "evaluation_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"评估摘要已保存到: {summary_path}")

if __name__ == "__main__":
    main()


