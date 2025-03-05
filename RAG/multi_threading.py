import threading
import time

def function1():
    print("Function 1 开始执行")
    for i in range(5):
        print(f"Function 1 正在处理任务 {i+1}")
        time.sleep(1)  # 模拟耗时操作
    print("Function 1 执行完成")

def function2():
    print("Function 2 开始执行")
    for i in range(3):
        print(f"Function 2 正在处理任务 {i+1}")
        time.sleep(1.5)  # 模拟耗时操作
    print("Function 2 执行完成")

def function3():
    print("Function 3 开始执行")
    for i in range(4):
        print(f"Function 3 正在处理任务 {i+1}")
        time.sleep(0.8)  # 模拟耗时操作
    print("Function 3 执行完成")

def function4():
    print("Function 4 开始执行")
    for i in range(6):
        print(f"Function 4 正在处理任务 {i+1}")
        time.sleep(0.5)  # 模拟耗时操作
    print("Function 4 执行完成")

# 创建线程
thread1 = threading.Thread(target=function1)
thread2 = threading.Thread(target=function2)
thread3 = threading.Thread(target=function3)
thread4 = threading.Thread(target=function4)

# 启动线程
print("开始启动所有线程")
thread1.start()
thread2.start()
thread3.start()
thread4.start()

# 等待线程结束
thread1.join()
thread2.join()
thread3.join()
thread4.join()

print("所有函数执行完成")
