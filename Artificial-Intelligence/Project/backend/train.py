"""
Training Script for Breast Tumor Classifier
This script demonstrates how to fine-tune the CNN model on your dataset.
"""

import os
import argparse
from pathlib import Path
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from src.ml.cnn_classifier import BreastTumorClassifier, TumorClassifierTrainer


def get_transforms():
    """Get train and validation transforms."""
    train_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    return train_transform, val_transform


def train(args):
    """Main training function."""
    print("=" * 60)
    print("Breast Tumor Classifier Training")
    print("=" * 60)
    
    # Check dataset path
    train_dir = Path(args.data_dir) / "train"
    val_dir = Path(args.data_dir) / "val"
    
    if not train_dir.exists():
        print(f"Error: Training directory not found: {train_dir}")
        print("\nPlease organize your data as follows:")
        print(f"  {args.data_dir}/")
        print("  ├── train/")
        print("  │   ├── benign/")
        print("  │   └── malignant/")
        print("  └── val/")
        print("      ├── benign/")
        print("      └── malignant/")
        return
    
    # Get transforms
    train_transform, val_transform = get_transforms()
    
    # Create datasets
    print(f"\nLoading data from: {args.data_dir}")
    train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Classes: {train_dataset.classes}")
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=True
    )
    
    val_loader = None
    if val_dir.exists():
        val_dataset = datasets.ImageFolder(val_dir, transform=val_transform)
        val_loader = DataLoader(
            val_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=True
        )
        print(f"Validation samples: {len(val_dataset)}")
    
    # Initialize model
    print(f"\nInitializing {args.model_type} model...")
    classifier = BreastTumorClassifier(model_type=args.model_type)
    trainer = TumorClassifierTrainer(
        classifier,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay
    )
    
    # Training loop
    print(f"\nStarting training for {args.epochs} epochs...")
    print("-" * 60)
    
    best_val_acc = 0.0
    
    for epoch in range(1, args.epochs + 1):
        # Train
        train_loss, train_acc = trainer.train_epoch(train_loader)
        
        # Validate
        if val_loader:
            val_loss, val_acc = trainer.validate(val_loader)
            print(f"Epoch {epoch:3d}/{args.epochs} | "
                  f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | "
                  f"Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")
            
            # Save best model
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                save_path = Path(args.output_dir) / "best_model.pth"
                classifier.save_model(str(save_path))
                print(f"  -> New best model saved! (Acc: {val_acc:.4f})")
        else:
            print(f"Epoch {epoch:3d}/{args.epochs} | "
                  f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f}")
    
    # Save final model
    final_path = Path(args.output_dir) / "final_model.pth"
    classifier.save_model(str(final_path))
    print(f"\nTraining complete! Final model saved to: {final_path}")
    
    if val_loader:
        print(f"Best validation accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Breast Tumor Classifier")
    
    parser.add_argument(
        "--data-dir",
        type=str,
        default="../datasets/mammograms",
        help="Path to dataset directory"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="models",
        help="Path to save trained models"
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="resnet50",
        choices=["resnet50", "mobilenet", "efficientnet"],
        help="Model architecture to use"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for training"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.001,
        help="Learning rate"
    )
    parser.add_argument(
        "--weight-decay",
        type=float,
        default=0.01,
        help="Weight decay for regularization"
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of data loading workers"
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    train(args)

