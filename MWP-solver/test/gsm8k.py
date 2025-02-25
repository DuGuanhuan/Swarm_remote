from datasets import load_dataset

gsm8k_dataset = load_dataset("gsm8k","main")
print(gsm8k_dataset)

train_dataset = gsm8k_dataset['train']

test_dataset = gsm8k_dataset['test']

print(train_dataset[0])