from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

client = OpenAI()

def call_model(prompt, model_name):
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model_name,
            temperature=0.7
        )
        return {
            "model": model_name,
            "content": completion.choices[0].message.content
        }
    except Exception as e:
        return {
            "model": model_name,
            "error": str(e)
        }

def main():
    prompt = "如何提高代码质量？"
    models = ["gemini-2.0-flash-001", "gpt-3.5-turbo", "gpt-4o-mini"]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(call_model, prompt, model)
            for model in models
        ]
        
        results = []
        for future in futures:
            result = future.result()
            results.append(result)
            if "content" in result:
                print(f"\n=== {result['model']} 响应 ===")
                print(result["content"])
            else:
                print(f"\n!!! {result['model']} 调用失败: {result['error']}")

if __name__ == "__main__":
    main()