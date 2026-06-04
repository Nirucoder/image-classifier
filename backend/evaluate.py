import os
import torch
from torchvision import datasets, models, transforms
from PIL import Image
import numpy as np
import cv2

LABELS = ["Handwritten Prescription", "Medical Scans (X-Ray-MRI)", "Printed Lab Report", "Printed Prescription"]

class AdaptiveThresholdTransform:
    def __call__(self, img):
        img_np = np.array(img.convert('L'))
        _, thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        img_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(img_rgb)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    AdaptiveThresholdTransform(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def evaluate():
    model = models.mobilenet_v2()
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(LABELS))
    
    weights_path = "model_weights.pth"
    if os.path.exists(weights_path):
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
        print(f"Loaded weights from {weights_path}")
    else:
        print("No weights found!")
        return

    model.eval()
    
    dataset = datasets.ImageFolder("data", transform=transform)
    print(f"Dataset classes: {dataset.classes}")
    
    correct = 0
    total = len(dataset)
    
    for idx in range(total):
        img, label_idx = dataset[idx]
        img_path, _ = dataset.samples[idx]
        
        with torch.no_grad():
            output = model(img.unsqueeze(0))
            probabilities = torch.softmax(output, dim=1)
            conf, pred_idx = torch.max(probabilities, dim=1)
            
        pred_label = LABELS[pred_idx.item()]
        actual_label = dataset.classes[label_idx]
        is_correct = pred_label == actual_label
        if is_correct:
            correct += 1
            
        print(f"File: {os.path.basename(img_path):<15} | Actual: {actual_label:<25} | Pred: {pred_label:<25} | Conf: {conf.item():.2f} | {'[OK]' if is_correct else '[FAIL]'}")
        
    print(f"\nAccuracy: {correct}/{total} ({correct/total*100:.1f}%)")

if __name__ == "__main__":
    evaluate()
