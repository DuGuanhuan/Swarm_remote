import threading
import time

# 模拟调用不同大模型的函数
def call_model_a():
    print("开始调用模型 A")
    time.sleep(1.5)  # 模拟模型 A 的处理时间
    result = "模型 A 的结果"
    print("模型 A 调用完成")
    return result

def call_model_b():
    print("开始调用模型 B")
    time.sleep(2.0)  # 模拟模型 B 的处理时间
    result = "模型 B 的结果"
    print("模型 B 调用完成")
    return result

def call_model_c():
    print("开始调用模型 C")
    time.sleep(1.0)  # 模拟模型 C 的处理时间
    result = "模型 C 的结果"
    print("模型 C 调用完成")
    return result

# 使用线程池管理并发
from concurrent.futures import ThreadPoolExecutor

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务
        future_a = executor.submit(call_model_a)
        future_b = executor.submit(call_model_b)
        future_c = executor.submit(call_model_c)
        
        # 获取结果
        results = {
            "model_a": future_a.result(),
            "model_b": future_b.result(),
            "model_c": future_c.result()
        }
    
    print("所有模型调用完成，结果汇总：")
    print(results)

if __name__ == "__main__":
    main()