import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from PIL import Image
from torchvision import datasets, models, transforms

# 1. Config
DATA_DIR = "data"
MODEL_SAVE_PATH = "model_weights.pth"
BATCH_SIZE = 2
EPOCHS = 25  # Increased for better convergence
LEARNING_RATE = 0.0005

# 2. Preprocessing with Binarization Logic (The "Base Points" approach)
class AdaptiveThresholdTransform:
    def __call__(self, img):
        img_np = np.array(img.convert('L'))
        _, thresh = cv2.threshold(img_np, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        img_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
        return Image.fromarray(img_rgb)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    AdaptiveThresholdTransform(),
    transforms.RandomRotation(10), # Less rotation needed since binarization is robust
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def train():
    # 3. Load Dataset
    dataset = datasets.ImageFolder(DATA_DIR, transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    num_classes = len(dataset.classes)
    
    print(f"Detected classes: {dataset.classes}")
    print(f"Total images: {len(dataset)}")

    # 4. Initialize Model (EfficientNetV2-S)
    model = models.efficientnet_v2_s(weights='DEFAULT')
    
    # Freeze all layers first
    for param in model.parameters():
        param.requires_grad = False
        
    # Unfreeze the last block of features for specialized learning
    # EfficientNetV2-S has 7 blocks. Block 6 and 7 are often safe to unfreeze for fine-tuning.
    for param in model.features[6:].parameters():
        param.requires_grad = True
        
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, num_classes)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # 5. Loss and Optimizer (With Class Weights)
    class_counts = [0] * num_classes
    for _, label in dataset:
        class_counts[label] += 1
    
    print(f"Class counts: {class_counts}")
    weights = [len(dataset) / (num_classes * count) if count > 0 else 1.0 for count in class_counts]
    class_weights = torch.FloatTensor(weights).to(device)
    print(f"Calculated class weights: {class_weights}")

    criterion = nn.CrossEntropyLoss(weight=class_weights)
    # Optimize both the unfrozen features and the classifier
    optimizer = optim.Adam([
        {'params': model.features[6:].parameters(), 'lr': LEARNING_RATE * 0.1},
        {'params': model.classifier[1].parameters(), 'lr': LEARNING_RATE}
    ])
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

    # 6. Training Loop
    print("Starting training...")
    model.train()
    for epoch in range(EPOCHS):
        running_loss = 0.0
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            
        epoch_loss = running_loss / len(dataset)
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {epoch_loss:.4f}")
        scheduler.step(epoch_loss)

    # 7. Save Weights
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Trained weights saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    train()
