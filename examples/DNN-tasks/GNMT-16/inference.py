import torch
from transformers import MarianMTModel, MarianTokenizer
from flask import Flask, request, jsonify

# Flask 应用
app = Flask(__name__)

# 加载模型和分词器
model_name = "gnmt16_model"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

@app.route('/translate', methods=['POST'])
def translate():
    if 'text' not in request.json:
        return jsonify({"error": "No text provided"}), 400

    text = request.json['text']
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        translated = model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
    result = tokenizer.decode(translated[0], skip_special_tokens=True)

    return jsonify({"translated_text": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
