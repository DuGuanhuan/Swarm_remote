import os
import pandas as pd
import re
import time
from tqdm import tqdm
import sys

# 添加项目根目录到路径，以便导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from run import solve_math_problem

# 获取当前文件所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
test_dir = os.path.dirname(current_dir)  # 获取test目录
data_dir = os.path.join(test_dir, 'data')  # 获取data目录

# 创建结果目录
results_dir = os.path.join(current_dir, "swarm_results")
os.makedirs(results_dir, exist_ok=True)

# 从验证结果中提取最终答案
def extract_answer(verification_text):
    """从验证结果中提取最终答案"""
    # 尝试匹配"最终答案：X"格式
    final_answer_match = re.search(r'最终答案[:：]\s*([\d\.\-]+)', verification_text)
    if final_answer_match:
        return final_answer_match.group(1)
    
    # 尝试匹配"结论"部分中的数字
    if "结论:" in verification_text or "结论：" in verification_text:
        conclusion_pattern = r'结论[:：].*?(\d+\.?\d*)'
        conclusion_match = re.search(conclusion_pattern, verification_text, re.DOTALL)
        if conclusion_match:
            return conclusion_match.group(1)
    
    # 尝试匹配"答案是X"格式
    answer_is_match = re.search(r'答案是\s*([\d\.\-]+)', verification_text)
    if answer_is_match:
        return answer_is_match.group(1)
    
    # 尝试匹配"= X"格式（通常在计算的最后一步）
    equals_match = re.search(r'=\s*([\d\.\-]+)(?!\d*\s*[+\-*/])', verification_text)
    if equals_match:
        return equals_match.group(1)
    
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
    # 尝试多个可能的位置查找测试数据
    possible_paths = [
        os.path.join(data_dir, "test_problems.csv"),     # 正确的data目录
        os.path.join(test_dir, "data", "test_problems.csv"),  # 另一种表示方式
        os.path.join(current_dir, "test_problems.csv"),  # 当前目录
        os.path.join(test_dir, "test_problems.csv"),     # test目录
        os.path.join(data_dir, "gsm8k_test.csv"),        # 可能的其他文件名
    ]
    
    test_csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            test_csv_path = path
            print(f"找到测试数据文件: {path}")
            break
    
    if not test_csv_path:
        print("错误: 找不到测试数据文件。请确保test_problems.csv文件存在。")
        print("请将测试数据文件放在以下位置之一:")
        for path in possible_paths:
            print(f"  - {path}")
        return
    
    # 加载测试数据
    test_df = pd.read_csv(test_csv_path)
    
    # 如果数据集没有question_id列，添加一个
    if 'question_id' not in test_df.columns:
        test_df['question_id'] = range(len(test_df))
    
    print(f"开始测试全部 {len(test_df)} 个问题...")
    
    # 存储结果
    results = []
    
    # 使用tqdm显示进度条
    for idx, row in tqdm(test_df.iterrows(), total=len(test_df), desc="测试进度"):
        question = row['question']
        true_answer = row['answer']
        question_id = row['question_id']
        
        try:
            start_time = time.time()
            
            # 调用多智能体系统解决问题
            swarm_result = solve_math_problem(question, debug=False)
            
            # 计算耗时
            time_taken = time.time() - start_time
            
            # 检查是否有错误
            if "error" in swarm_result:
                print(f"问题 {question_id} 处理出错: {swarm_result['error']}")
                results.append({
                    'question_id': question_id,
                    'question': question,
                    'true_answer': true_answer,
                    'swarm_response': swarm_result.get("error", "未知错误"),
                    'extracted_answer': "错误",
                    'is_correct': False,
                    'time_taken': time_taken
                })
                continue
            
            # 从验证结果中提取答案
            verification = swarm_result.get("verification", "")
            extracted_answer = extract_answer(verification)
            
            # 评估答案
            is_correct = evaluate_model_answer(extracted_answer, true_answer)
            
            # 存储结果
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'problem_analysis': swarm_result.get("problem_analysis", ""),
                'strategy': swarm_result.get("strategy", ""),
                'calculation': swarm_result.get("calculation", ""),
                'verification': verification,
                'extracted_answer': extracted_answer,
                'is_correct': is_correct,
                'time_taken': time_taken
            })
            
            # 简短打印结果
            print(f"问题 {question_id}: {'✓' if is_correct else '✗'} (预测: {extracted_answer}, 正确: {true_answer}, 耗时: {time_taken:.2f}秒)")
            
            # 添加短暂延迟，避免API限制
            time.sleep(0.5)
            
        except Exception as e:
            print(f"处理问题 {question_id} 时出错: {str(e)}")
            # 记录错误情况
            results.append({
                'question_id': question_id,
                'question': question,
                'true_answer': true_answer,
                'swarm_response': f"错误: {str(e)}",
                'extracted_answer': "错误",
                'is_correct': False,
                'time_taken': -1
            })
            time.sleep(1)  # 出错时等待时间更长
    
    # 计算准确率和平均耗时
    correct_count = sum(result['is_correct'] for result in results)
    accuracy = correct_count / len(results)
    valid_times = [r['time_taken'] for r in results if r['time_taken'] > 0]
    avg_time = sum(valid_times) / len(valid_times) if valid_times else 0
    
    print(f"\n总体准确率: {accuracy:.2%} ({correct_count}/{len(results)})")
    print(f"平均耗时: {avg_time:.2f}秒/题")
    
    # 保存详细结果
    results_df = pd.DataFrame(results)
    results_path = os.path.join(results_dir, "swarm_full_results.csv")
    results_df.to_csv(results_path, index=False)
    print(f"详细结果已保存到: {results_path}")
    
    # 保存简化版结果（不包含完整的模型回答）
    simplified_results = results_df[['question_id', 'question', 'true_answer', 'extracted_answer', 'is_correct', 'time_taken']]
    simplified_path = os.path.join(results_dir, "swarm_simplified_results.csv")
    simplified_results.to_csv(simplified_path, index=False)
    print(f"简化结果已保存到: {simplified_path}")
    
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
    summary_path = os.path.join(results_dir, "swarm_evaluation_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"评估摘要已保存到: {summary_path}")

if __name__ == "__main__":
    main() 