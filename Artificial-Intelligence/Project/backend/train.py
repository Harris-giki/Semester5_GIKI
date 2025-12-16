"""
Training Script for Breast Tumor Classifier
============================================

Uses Transfer Learning with ResNet50 pretrained on ImageNet.
Best for small datasets (<5000 images) - achieves 80-90% accuracy.

Usage:
    python3 train.py --data-dir ../datasets/mammograms --epochs 30
"""

import os
import argparse

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from src.ml.cnn_classifier import TransferLearningCNN


def get_device():
    """Get the best available device."""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Using CUDA: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using Apple Silicon GPU (MPS)")
    else:
        device = torch.device("cpu")
        print("Using CPU")
    return device


def get_transforms():
    """Get data augmentation transforms for transfer learning."""
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform


def train(args):
    """Main training function."""
    print("=" * 60)
    print("Breast Tumor Classifier Training")
    print("=" * 60)
    
    device = get_device()
    print(f"PyTorch version: {torch.__version__}")
    print(f"Using Transfer Learning with ResNet50")
    print()
    
    # Get transforms
    train_transform, val_transform = get_transforms()
    
    # Load datasets
    print("Loading datasets...")
    train_dir = os.path.join(args.data_dir, 'train')
    val_dir = os.path.join(args.data_dir, 'val')
    test_dir = os.path.join(args.data_dir, 'test')
    
    train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
    val_dataset = datasets.ImageFolder(val_dir, transform=val_transform)
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    print(f"Classes: {train_dataset.classes}")
    
    # Class weights for imbalanced data
    class_counts = [0, 0]
    for _, label in train_dataset:
        class_counts[label] += 1
    
    total = sum(class_counts)
    class_weights = torch.tensor([
        total / (2 * class_counts[0]) if class_counts[0] > 0 else 1.0,
        total / (2 * class_counts[1]) if class_counts[1] > 0 else 1.0
    ], dtype=torch.float32).to(device)
    
    print(f"Class distribution: benign={class_counts[0]}, malignant={class_counts[1]}")
    
    # Data loaders
    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True,
        num_workers=0, pin_memory=False
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False,
        num_workers=0, pin_memory=False
    )
    
    # Create model
    print(f"\nCreating model...")
    model = TransferLearningCNN(num_classes=2, dropout_rate=args.dropout)
    model = model.to(device)
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    
    # Lower learning rate for transfer learning (pretrained weights are already good)
    lr = args.learning_rate * 0.1
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    
    print(f"Learning rate: {lr}")
    
    # Create model directory
    os.makedirs(args.model_dir, exist_ok=True)
    
    # Training loop
    print(f"\nStarting training for {args.epochs} epochs...")
    print("-" * 60)
    
    best_val_acc = 0.0
    patience_counter = 0
    
    for epoch in range(args.epochs):
        # Training
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            
            # Gradient clipping for stability
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
        
        train_loss /= len(train_loader)
        train_acc = train_correct / train_total
        
        # Validation
        model.eval()
        val_loss, val_correct, val_total = 0.0, 0, 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
        
        val_loss /= len(val_loader)
        val_acc = val_correct / val_total
        
        scheduler.step()
        
        # Print progress
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Epoch {epoch+1:3d}/{args.epochs} | "
              f"Train: {train_acc:.4f} | Val: {val_acc:.4f} | "
              f"LR: {current_lr:.2e}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), os.path.join(args.model_dir, 'best_model.pth'))
            patience_counter = 0
            print(f"  ↳ New best model saved! (val_acc: {val_acc:.4f})")
        else:
            patience_counter += 1
        
        # Early stopping
        if patience_counter >= args.patience:
            print(f"\nEarly stopping at epoch {epoch+1}")
            break
    
    # Save final model
    torch.save(model.state_dict(), os.path.join(args.model_dir, 'final_model.pth'))
    
    print(f"\n" + "=" * 60)
    print(f"Training complete!")
    print(f"Best validation accuracy: {best_val_acc:.4f}")
    print(f"Models saved to: {args.model_dir}/")
    
    # Test evaluation
    if os.path.exists(test_dir):
        print(f"\n" + "=" * 60)
        print("Evaluating on Test Set")
        print("=" * 60)
        
        test_dataset = datasets.ImageFolder(test_dir, transform=val_transform)
        test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
        
        # Load best model
        model.load_state_dict(torch.load(os.path.join(args.model_dir, 'best_model.pth')))
        model.eval()
        
        test_correct, test_total = 0, 0
        all_preds, all_labels = [], []
        
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = outputs.max(1)
                test_total += labels.size(0)
                test_correct += predicted.eq(labels).sum().item()
                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        test_acc = test_correct / test_total
        print(f"Test Accuracy: {test_acc:.4f}")
        
        # Per-class accuracy
        from collections import defaultdict
        class_correct = defaultdict(int)
        class_total = defaultdict(int)
        for pred, label in zip(all_preds, all_labels):
            class_total[label] += 1
            if pred == label:
                class_correct[label] += 1
        
        for cls_idx, cls_name in enumerate(test_dataset.classes):
            acc = class_correct[cls_idx] / class_total[cls_idx] if class_total[cls_idx] > 0 else 0
            print(f"  {cls_name}: {acc:.4f} ({class_correct[cls_idx]}/{class_total[cls_idx]})")
    
    return best_val_acc


def main():
    parser = argparse.ArgumentParser(description='Train Breast Tumor Classifier')
    parser.add_argument('--data-dir', type=str, default='../datasets/mammograms')
    parser.add_argument('--model-dir', type=str, default='models')
    parser.add_argument('--epochs', type=int, default=30)
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--learning-rate', type=float, default=0.001)
    parser.add_argument('--dropout', type=float, default=0.5)
    parser.add_argument('--patience', type=int, default=10)
    
    args = parser.parse_args()
    
    if not os.path.isabs(args.data_dir):
        args.data_dir = os.path.join(os.path.dirname(__file__), args.data_dir)
    if not os.path.isabs(args.model_dir):
        args.model_dir = os.path.join(os.path.dirname(__file__), args.model_dir)
    
    if not os.path.exists(args.data_dir):
        print(f"Error: Data directory not found: {args.data_dir}")
        return 1
    
    train(args)
    return 0


if __name__ == '__main__':
    exit(main())
