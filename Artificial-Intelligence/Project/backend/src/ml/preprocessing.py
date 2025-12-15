"""
Image Preprocessing Module for Mammogram Images
Handles resizing, normalization, contrast enhancement, and noise removal
"""

import numpy as np
from PIL import Image
import cv2
from typing import Tuple, Optional
import io


def preprocess_image(
    image_bytes: bytes,
    target_size: Tuple[int, int] = (224, 224),
    normalize: bool = True
) -> np.ndarray:
    """
    Preprocess mammogram image for CNN input.
    
    Args:
        image_bytes: Raw image bytes from upload
        target_size: Target dimensions (width, height)
        normalize: Whether to normalize pixel values
    
    Returns:
        Preprocessed image as numpy array
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if grayscale
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to target size
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)
    
    if normalize:
        # Normalize to [0, 1] range
        img_array = img_array / 255.0
        
        # Apply ImageNet normalization for transfer learning
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_array = (img_array - mean) / std
    
    return img_array


def enhance_contrast(image_bytes: bytes, clip_limit: float = 2.0) -> bytes:
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) 
    to enhance mammogram contrast.
    
    Args:
        image_bytes: Raw image bytes
        clip_limit: Threshold for contrast limiting
    
    Returns:
        Enhanced image as bytes
    """
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Encode back to bytes
    _, buffer = cv2.imencode('.png', enhanced)
    return buffer.tobytes()


def remove_noise(image_bytes: bytes, kernel_size: int = 5) -> bytes:
    """
    Apply Gaussian blur for noise removal.
    
    Args:
        image_bytes: Raw image bytes
        kernel_size: Size of Gaussian kernel
    
    Returns:
        Denoised image as bytes
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Apply bilateral filter (preserves edges while removing noise)
    denoised = cv2.bilateralFilter(img, kernel_size, 75, 75)
    
    _, buffer = cv2.imencode('.png', denoised)
    return buffer.tobytes()


def get_image_stats(image_bytes: bytes) -> dict:
    """
    Calculate basic image statistics for analysis.
    
    Args:
        image_bytes: Raw image bytes
    
    Returns:
        Dictionary with image statistics
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    return {
        "mean_intensity": float(np.mean(img)),
        "std_intensity": float(np.std(img)),
        "min_intensity": int(np.min(img)),
        "max_intensity": int(np.max(img)),
        "contrast_ratio": float(np.max(img) - np.min(img)) / 255.0,
        "width": img.shape[1],
        "height": img.shape[0]
    }

