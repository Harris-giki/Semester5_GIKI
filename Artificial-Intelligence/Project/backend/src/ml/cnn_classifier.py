"""
Breast Tumor Classifier using Transfer Learning (ResNet50)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import numpy as np
import io
from typing import Tuple, Dict, Optional
import cv2


class TransferLearningCNN(nn.Module):
    """ResNet50-based classifier for breast tumor detection."""
    
    def __init__(self, num_classes: int = 2, dropout_rate: float = 0.5):
        super().__init__()
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
        num_features = self.backbone.fc.in_features
        
        self.backbone.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(num_features, 512),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(512),
            nn.Dropout(dropout_rate * 0.6),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        return self.backbone(x)


class BreastTumorClassifier:
    """CNN Classifier for breast tumor detection."""
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        model_type: str = "transfer",
        backbone: str = "resnet50",
        device: str = "auto"
    ):
        self.device = self._get_device(device)
        self.model_type = model_type
        
        self.model = TransferLearningCNN(num_classes=2)
        
        if model_path:
            print(f"Loading model from {model_path}")
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
        
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.classes = ["benign", "malignant"]
        print(f"Model initialized on: {self.device}")
    
    def _get_device(self, device: str) -> torch.device:
        if device == "auto":
            if torch.cuda.is_available():
                return torch.device("cuda")
            elif torch.backends.mps.is_available():
                return torch.device("mps")
            return torch.device("cpu")
        return torch.device(device)
    
    def predict(self, image_bytes: bytes) -> Dict:
        """Classify a mammogram image."""
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
        
        probs = probabilities.cpu().numpy()[0]
        predicted_class = int(np.argmax(probs))
        confidence = float(probs[predicted_class])
        
        return {
            "predicted_class": self.classes[predicted_class],
            "confidence": confidence,
            "probabilities": {
                "benign": float(probs[0]),
                "malignant": float(probs[1])
            },
            "severity_score": float(probs[1]) * 100
        }
    
    def generate_gradcam(self, image_bytes: bytes) -> Tuple[np.ndarray, Dict]:
        """Generate Grad-CAM heatmap for model explainability."""
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        original_image = np.array(image)
        
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        input_tensor.requires_grad_(True)
        
        target_layer = self.model.backbone.layer4[-1]
        
        gradients = []
        activations = []
        
        def backward_hook(module, grad_input, grad_output):
            gradients.append(grad_output[0])
        
        def forward_hook(module, input, output):
            activations.append(output)
        
        backward_handle = target_layer.register_full_backward_hook(backward_hook)
        forward_handle = target_layer.register_forward_hook(forward_hook)
        
        outputs = self.model(input_tensor)
        probabilities = F.softmax(outputs, dim=1)
        probs = probabilities.cpu().detach().numpy()[0]
        predicted_class = int(np.argmax(probs))
        
        self.model.zero_grad()
        outputs[0, predicted_class].backward()
        
        backward_handle.remove()
        forward_handle.remove()
        
        grads = gradients[0].cpu().data.numpy()[0]
        acts = activations[0].cpu().data.numpy()[0]
        
        weights = np.mean(grads, axis=(1, 2))
        cam = np.zeros(acts.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * acts[i]
        
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (original_image.shape[1], original_image.shape[0]))
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        overlay = np.uint8(0.6 * original_image + 0.4 * heatmap)
        
        prediction = {
            "predicted_class": self.classes[predicted_class],
            "confidence": float(probs[predicted_class]),
            "probabilities": {"benign": float(probs[0]), "malignant": float(probs[1])},
            "severity_score": float(probs[1]) * 100
        }
        
        return overlay, prediction
