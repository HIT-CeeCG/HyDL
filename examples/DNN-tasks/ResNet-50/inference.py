import torch
import torchvision.models as models
import torchvision.transforms as transforms
from flask import Flask, request, jsonify
from PIL import Image

# Flask 应用
app = Flask(__name__)

# 加载模型
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet50(pretrained=False)
model.fc = torch.nn.Linear(2048, 10)  # 确保与训练时一致
model.load_state_dict(torch.load("resnet50_cifar10.pth", map_location=device))
model = model.to(device)
model.eval()

# 数据预处理
transform = transforms.Compose([
    transforms.Resize(224),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image = Image.open(file.stream).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs, 1)
    
    return jsonify({"predicted_class": int(predicted.item())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
