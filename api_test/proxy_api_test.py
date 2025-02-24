from openai import OpenAI
client = OpenAI(
    base_url='https://api.nuwaapi.com/v1',
    # sk-xxx替换为自己的key
    api_key='sk-EOH2SFHd0dn8lU9ocrJaFjBRzqE2kBu0GkaAiXusvZ0P7hgs'
)
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "用于测试：仅需回答我你的模型型号"}
  ]
)
# print(completion.choices[0].message)
print(completion)
