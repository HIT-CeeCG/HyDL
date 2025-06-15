import torch
from transformers import MarianMTModel, MarianTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# 加载数据集
dataset = load_dataset("wmt16", "de-en")  # 示例：德语到英语的翻译任务

# 加载 Marian 分词器和模型
model_name = "Helsinki-NLP/opus-mt-de-en"  # GNMT 示例模型
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# 数据预处理
def preprocess_function(examples):
    inputs = [ex for ex in examples["translation"]["de"]]
    targets = [ex for ex in examples["translation"]["en"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)
tokenized_datasets.set_format("torch")

# 分割训练和测试集
train_dataset = tokenized_datasets["train"]
test_dataset = tokenized_datasets["test"]

# 设置训练参数
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=200,
)

# Trainer 实例
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
)

# 训练
trainer.train()

# 保存模型
model.save_pretrained("gnmt16_model")
tokenizer.save_pretrained("gnmt16_model")
print("Model and tokenizer saved to 'gnmt16_model'")
