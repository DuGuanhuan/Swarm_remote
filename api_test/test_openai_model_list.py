from openai import OpenAI
client = OpenAI()
def list_openai_models():
    try:
        models = client.models.list()
        print(f"可用的 OpenAI 模型（共 {len(models.data)} 个）：")
        for i, model in enumerate(models.data, 1):
            print(f"{i}. {model.id}")
        return models.data
    except Exception as e:
        print(f"获取模型列表失败：{str(e)}")
        return []

if __name__ == "__main__":
    list_openai_models()