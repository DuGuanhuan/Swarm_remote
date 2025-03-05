from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "如何做同时调用多个 openai 接口",
        }
    ],
    model="gpt-4o-mini",
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")