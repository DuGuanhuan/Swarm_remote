import os
import pandas as pd
import re
import time
from tqdm import tqdm
from swarm import Swarm
from run import solve_math_problem

# 获取当前文件所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 从验证结果中提取最终答案
def extract_answer(verification_text):
    """从验证结果中提取最终答案"""
    # 尝试匹配"最终答案：X"格式
    final_answer_match = re.search(r'最终答案[:：]\s*([\d\.\-]+)', verification_text)
    if final_answer_match:
        return final_answer_match.group(1)
    
    # 尝试匹配"结论"部分中的数字
    if "结论:" in verification_text:
        conclusion = verification_text.split("结论:")[-1].strip()
        # 从结论中提取数字
        numbers = re.findall(r'([\d\.\-]+)', conclusion)
        if numbers:
            return numbers[0]
    
    # 尝试其他格式
    patterns = [
        r'答案是\s*([\d\.\-]+)',
        r'答案[:：]\s*([\d\.\-]+)',
        r'=\s*([\d\.\-]+)(?!\d*\s*[+\-*/])'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, verification_text)
        if match:
            return match.group(1)
    
    # 尝试匹配任何数字（最后的手段）
    numbers = re.findall(r'([\d\.\-]+)', verification_text)
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
    
    # 可以选择测试部分问题以加快测试速度
    sample_size = 20  # 可以调整为需要的数量
    test_sample = test_df.sample(sample_size) if sample_size < len(test_df) else test_df
    
    print(f"开始测试 {len(test_sample)} 个问题...")
    
    # 存储结果
    results = []
    
    # 使用tqdm显示进度条
    for idx, row in tqdm(test_sample.iterrows(), total=len(test_sample), desc="测试进度"):
        question = row['question']
        true_answer = row['answer']
        question_id = row['question_id']
        
        try:
            # 调用多智能体系统
            start_time = time.time()
            solution = solve_math_problem(question, debug=False)
            elapsed_time = time.time() - start_time
            
            # 获取验证结果
            verification = solution.get("verification", "")
            
            # 提取答案
            extracted_answer = extract_answer(verification)
            
            # 评估答案
            is_correct = evaluate_model_answer(extracted_answer, true_answer)
            
            # 存储结果
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'extracted_answer': extracted_answer,
                'is_correct': is_correct,
                'time_taken': elapsed_time
            })
            
            # 简短打印结果
            print(f"问题 {question_id}: {'✓' if is_correct else '✗'} (预测: {extracted_answer}, 正确: {true_answer}, 耗时: {elapsed_time:.2f}秒)")
            
            # 添加短暂延迟，避免API限制
            time.sleep(0.5)
            
        except Exception as e:
            print(f"处理问题 {question_id} 时出错: {str(e)}")
            # 记录错误情况
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'extracted_answer': "错误",
                'is_correct': False,
                'time_taken': -1,
                'error': str(e)
            })
            time.sleep(1)  # 出错时等待时间更长
    
    # 计算准确率
    correct_count = sum(result['is_correct'] for result in results)
    accuracy = correct_count / len(results)
    avg_time = sum(r['time_taken'] for r in results if r['time_taken'] > 0) / len([r for r in results if r['time_taken'] > 0])
    
    print(f"\n总体准确率: {accuracy:.2%} ({correct_count}/{len(results)})")
    print(f"平均耗时: {avg_time:.2f}秒/题")
    
    # 保存详细结果
    results_df = pd.DataFrame(results)
    results_path = os.path.join(current_dir, "swarm_evaluation_results.csv")
    results_df.to_csv(results_path, index=False)
    print(f"详细结果已保存到: {results_path}")
    
    # 创建结果摘要
    summary = {
        '总问题数': len(results),
        '正确数量': correct_count,
        '准确率': accuracy,
        '平均耗时': avg_time,
        '测试时间': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 保存摘要
    summary_df = pd.DataFrame([summary])
    summary_path = os.path.join(current_dir, "swarm_evaluation_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"评估摘要已保存到: {summary_path}")

if __name__ == "__main__":
    main() 