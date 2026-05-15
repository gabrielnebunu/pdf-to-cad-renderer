"""Step 2: Clean the raster image — denoise, deskew, binarize."""
import cv2
import numpy as np
import os
from loguru import logger


def deskew(image: np.ndarray) -> np.ndarray:
    """Detect and correct skew using Hough line transform."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)
    if lines is None:
        return image
    angles = []
    for rho, theta in lines[:, 0]:
        angle = (theta - np.pi / 2) * (180 / np.pi)
        if abs(angle) < 10:  # only small rotations
            angles.append(angle)
    if not angles:
        return image
    median_angle = float(np.median(angles))
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), median_angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def preprocess_image(img_path: str, output_dir: str) -> str:
    """
    Pipeline: grayscale → denoise → deskew → adaptive threshold → morphological cleanup.
    Returns path to processed image.
    """
    img = cv2.imread(img_path)
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
    # Deskew
    deskewed = deskew(denoised)
    # Adaptive threshold (binarize)
    binary = cv2.adaptiveThreshold(
        deskewed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=15, C=8
    )
    # Morphological cleanup — remove small noise
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    out_path = os.path.join(output_dir, "preprocessed.png")
    cv2.imwrite(out_path, cleaned)
    logger.info(f"Preprocessed → {out_path}")
    return out_path
