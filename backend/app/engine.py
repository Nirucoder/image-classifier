import torch
import os
from torchvision import models, transforms
from PIL import Image
import io
import cv2
import numpy as np
import torch.nn.functional as F


# Labels ordered alphabetically to match datasets.ImageFolder
LABELS = ["Handwritten Prescription", "Medical Scans (X-Ray-MRI)", "Printed Lab Report", "Printed Prescription"]

# Configure PyTorch for single-threaded CPU execution to minimize memory footprint
torch.set_num_threads(1)
torch.set_num_interop_threads(1)

# Initialize model without default weights to save memory
model = models.mobilenet_v2(weights=None)
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(LABELS))

# Load trained weights if available
WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "..", "model_weights.pth")
if os.path.exists(WEIGHTS_PATH):
    print(f"Loading trained weights from {WEIGHTS_PATH}")
    state_dict = torch.load(WEIGHTS_PATH, map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    del state_dict
    import gc
    gc.collect()
    
model.eval()

class AdaptiveThresholdTransform:
    def __call__(self, img):
        # 1. Pilot to OpenCV
        img_np = np.array(img.convert('L'))
        # 2. Adaptive Threshold (Otsu)
        _, thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # 3. Convert back to RGB format for EfficientNet
        img_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(img_rgb)

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    AdaptiveThresholdTransform(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        input_tensor = preprocess(img).unsqueeze(0)
        
        with torch.no_grad():
            output = model(input_tensor)
            # Apply Softmax to get probabilities
            probabilities = F.softmax(output, dim=1)
            conf, index = torch.max(probabilities, dim=1)
            
        return LABELS[index.item()], conf.item()
    except Exception:
        return "Classification Failed", 0.0