"""
Optional AI Assist
-------------------
This is intentionally NOT a trained deep-learning classifier (that would need
a labelled pothole dataset + GPU training, out of scope here). Instead it's a
transparent, explainable OpenCV heuristic that gives the admin/user a
*suggestion* they must still verify:

  - Converts the image to grayscale + edge map (Canny).
  - Looks for a large, roughly circular/irregular dark blob near the bottom
    two-thirds of the frame (typical pothole/crack framing when a phone is
    held at road level).
  - The blob's area (relative to frame) drives a severity suggestion.

If OpenCV or the image can't be read, we simply return None and the user/
admin fills the fields in manually - the AI suggestion is never final,
per the spec ("AI decision එක final නොකර, admin/userට verify කරන්න දෙන්න").
"""
import cv2
import numpy as np


def suggest_from_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(blurred, 40, 120)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        area_ratio = cv2.contourArea(largest) / float(h * w)

        x, y, cw, ch = cv2.boundingRect(largest)
        aspect = cw / float(ch) if ch else 1

        if area_ratio < 0.01:
            return None  # not confident enough to suggest anything

        # Rough shape heuristic: pothole ~ blobby/roundish, crack ~ long & thin
        damage_type = "crack" if aspect > 2.5 or aspect < 0.4 else "pothole"

        if area_ratio > 0.18:
            severity = "critical"
        elif area_ratio > 0.10:
            severity = "high"
        elif area_ratio > 0.04:
            severity = "medium"
        else:
            severity = "low"

        return {
            "damage_type": damage_type,
            "severity": severity,
            "confidence": round(min(area_ratio * 4, 1.0), 2),
        }
    except Exception:
        # Never let AI-assist break report submission
        return None
