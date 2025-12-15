"""
CNN-Based Breast Tumor Classifier
Uses Transfer Learning with ResNet50 for mammogram classification
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import io
from typing import Tuple, Dict, Optional
import cv2


class BreastTumorClassifier:
    """
    CNN Classifier for breast tumor detection using transfer learning.
    Supports ResNet50, MobileNetV2, and custom models.
    """
    
    def __init__(
        self,
        model_type: str = "resnet50",
        model_path: Optional[str] = None,
        device: str = "auto"
    ):
        """
        Initialize the classifier.
        
        Args:
            model_type: Type of model ('resnet50', 'mobilenet', 'efficientnet')
            model_path: Path to trained model weights (None for pretrained ImageNet)
            device: Device to use ('cpu', 'cuda', 'mps', or 'auto')
        """
        self.model_type = model_type
        self.device = self._get_device(device)
        self.model = self._build_model(model_type)
        
        if model_path:
            self._load_weights(model_path)
        
        self.model.to(self.device)
        self.model.eval()
        
        # Image transform for inference
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Class labels
        self.classes = ["benign", "malignant"]
    
    def _get_device(self, device: str) -> torch.device:
        """Determine the best available device."""
        if device == "auto":
            if torch.cuda.is_available():
                return torch.device("cuda")
            elif torch.backends.mps.is_available():
                return torch.device("mps")
            else:
                return torch.device("cpu")
        return torch.device(device)
    
    def _build_model(self, model_type: str) -> nn.Module:
        """Build the CNN model with transfer learning."""
        if model_type == "resnet50":
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
            # Replace final layer for binary classification
            num_features = model.fc.in_features
            model.fc = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 2)
            )
            
        elif model_type == "mobilenet":
            model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V2)
            num_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 2)
            )
            
        elif model_type == "efficientnet":
            model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
            num_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, 2)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return model
    
    def _load_weights(self, model_path: str):
        """Load trained model weights."""
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
    
    def predict(self, image_bytes: bytes) -> Dict:
        """
        Classify a mammogram image.
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            Dictionary with prediction results
        """
        # Load and preprocess image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Transform for model input
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Forward pass
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = F.softmax(outputs, dim=1)
        
        # Get prediction
        probs = probabilities.cpu().numpy()[0]
        predicted_class = int(np.argmax(probs))
        confidence = float(probs[predicted_class])
        
        # Calculate severity score (0-100 scale)
        malignant_prob = float(probs[1])
        severity_score = malignant_prob * 100
        
        return {
            "predicted_class": self.classes[predicted_class],
            "confidence": confidence,
            "probabilities": {
                "benign": float(probs[0]),
                "malignant": float(probs[1])
            },
            "severity_score": severity_score,
            "model_type": self.model_type
        }
    
    def generate_gradcam(self, image_bytes: bytes) -> Tuple[np.ndarray, Dict]:
        """
        Generate Grad-CAM heatmap for model explainability.
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            Tuple of (heatmap overlay, prediction dict)
        """
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        original_image = np.array(image)
        
        # Transform for model input
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        input_tensor.requires_grad_(True)
        
        # Get the target layer for Grad-CAM
        if self.model_type == "resnet50":
            target_layer = self.model.layer4[-1]
        elif self.model_type == "mobilenet":
            target_layer = self.model.features[-1]
        elif self.model_type == "efficientnet":
            target_layer = self.model.features[-1]
        
        # Hook for gradients and activations
        gradients = []
        activations = []
        
        def backward_hook(module, grad_input, grad_output):
            gradients.append(grad_output[0])
        
        def forward_hook(module, input, output):
            activations.append(output)
        
        backward_handle = target_layer.register_full_backward_hook(backward_hook)
        forward_handle = target_layer.register_forward_hook(forward_hook)
        
        # Forward pass
        outputs = self.model(input_tensor)
        probabilities = F.softmax(outputs, dim=1)
        probs = probabilities.cpu().detach().numpy()[0]
        predicted_class = int(np.argmax(probs))
        
        # Backward pass for predicted class
        self.model.zero_grad()
        outputs[0, predicted_class].backward()
        
        # Remove hooks
        backward_handle.remove()
        forward_handle.remove()
        
        # Generate Grad-CAM
        grads = gradients[0].cpu().data.numpy()[0]
        acts = activations[0].cpu().data.numpy()[0]
        
        # Global average pooling of gradients
        weights = np.mean(grads, axis=(1, 2))
        
        # Weighted combination of activation maps
        cam = np.zeros(acts.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * acts[i]
        
        # ReLU and normalize
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam, (original_image.shape[1], original_image.shape[0]))
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        # Create heatmap overlay
        heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # Overlay on original image
        overlay = np.uint8(0.6 * original_image + 0.4 * heatmap)
        
        prediction = {
            "predicted_class": self.classes[predicted_class],
            "confidence": float(probs[predicted_class]),
            "probabilities": {
                "benign": float(probs[0]),
                "malignant": float(probs[1])
            },
            "severity_score": float(probs[1]) * 100
        }
        
        return overlay, prediction
    
    def save_model(self, path: str):
        """Save model weights."""
        torch.save(self.model.state_dict(), path)


class TumorClassifierTrainer:
    """
    Trainer class for fine-tuning the tumor classifier on custom datasets.
    """
    
    def __init__(
        self,
        model: BreastTumorClassifier,
        learning_rate: float = 0.001,
        weight_decay: float = 0.01
    ):
        self.model = model
        self.device = model.device
        
        # Loss function with class weights for imbalanced data
        self.criterion = nn.CrossEntropyLoss()
        
        # Optimizer with weight decay for regularization
        self.optimizer = torch.optim.AdamW(
            model.model.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='max', patience=3, factor=0.5
        )
        
        # Data augmentation for training
        self.train_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def train_epoch(self, dataloader) -> Tuple[float, float]:
        """Train for one epoch."""
        self.model.model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for images, labels in dataloader:
            images = images.to(self.device)
            labels = labels.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
        
        accuracy = correct / total
        avg_loss = total_loss / len(dataloader)
        return avg_loss, accuracy
    
    def validate(self, dataloader) -> Tuple[float, float]:
        """Validate the model."""
        self.model.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in dataloader:
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model.model(images)
                loss = self.criterion(outputs, labels)
                
                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()
        
        accuracy = correct / total
        avg_loss = total_loss / len(dataloader)
        self.scheduler.step(accuracy)
        return avg_loss, accuracy

