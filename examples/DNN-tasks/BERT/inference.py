import torch
from transformers import BertTokenizer, BertForSequenceClassification
from flask import Flask, request, jsonify

# Flask 应用
app = Flask(__name__)

# 加载模型和分词器
model = BertForSequenceClassification.from_pretrained("bert_imdb_model")
tokenizer = BertTokenizer.from_pretrained("bert_imdb_model")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    if 'text' not in request.json:
        return jsonify({"error": "No text provided"}), 400

    text = request.json['text']
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, predicted_class].item()

    return jsonify({"predicted_class": predicted_class, "confidence": confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
