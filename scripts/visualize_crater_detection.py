#!/usr/bin/env python3
"""
visualize_crater_detection.py
Demonstrates deterministic integer radial ray casting for crater circle parameter extraction.
"""

import os
import tarfile
import math
from PIL import Image, ImageDraw, ImageFont

def detect_crater_circles(img_bytes, width=1020, height=1020, altitude_m=11800.0):
    """
    Deterministic Integer Radial Ray-Casting Crater Detector.
    Calibrated for Hera AFC dynamic range (Dark: 3-8, Regolith: 50-94).
    """
    step = 16
    craters = []
    
    # 1. Grid search across asteroid body (where pixel brightness > 25)
    for cy in range(step * 4, height - step * 4, step):
        for cx in range(step * 4, width - step * 4, step):
            p_center = img_bytes[cy * width + cx]
            
            # Skip dark space background
            if p_center < 25:
                continue
            
            # 8 radial ray directions: (dx, dy)
            dirs = [
                (1, 0), (1, 1), (0, 1), (-1, 1),
                (-1, 0), (-1, -1), (0, -1), (1, -1)
            ]
            
            radii = []
            grad_sum = 0
            
            for dx, dy in dirs:
                best_r = 0
                max_g = 0
                for r in range(6, 40, 2):
                    px = cx + dx * r
                    py = cy + dy * r
                    if 0 <= px < width and 0 <= py < height:
                        px_next = cx + dx * (r + 2)
                        py_next = cy + dy * (r + 2)
                        if 0 <= px_next < width and 0 <= py_next < height:
                            val1 = img_bytes[py * width + px]
                            val2 = img_bytes[py_next * width + px_next]
                            g = abs(int(val2) - int(val1))
                            if g > max_g:
                                max_g = g
                                best_r = r
                if max_g >= 6 and best_r > 0:
                    radii.append(best_r)
                    grad_sum += max_g
            
            # If at least 5 out of 8 radial rays detected rim boundary
            if len(radii) >= 5:
                mean_r = sum(radii) / len(radii)
                variance = sum((r - mean_r) ** 2 for r in radii) / len(radii)
                std_dev = math.sqrt(variance)
                
                # Circularity criterion
                if std_dev < (mean_r * 0.40) and mean_r >= 8:
                    confidence = min(99, int((grad_sum / len(radii)) * 6.5))
                    if confidence >= 45:
                        # Metric scaling via PALT altitude: D = 2 * R * alt * (14um / 106.6mm)
                        metric_diam_m = 2.0 * mean_r * altitude_m * 0.00013133
                        craters.append({
                            'cx': cx,
                            'cy': cy,
                            'radius': int(mean_r),
                            'confidence': confidence,
                            'diam_m': metric_diam_m
                        })
    
    # 3. Non-maximum suppression (NMS)
    filtered = []
    craters.sort(key=lambda c: c['confidence'], reverse=True)
    for c in craters:
        overlap = False
        for f in filtered:
            dist = math.hypot(c['cx'] - f['cx'], c['cy'] - f['cy'])
            if dist < (c['radius'] + f['radius']) * 0.75:
                overlap = True
                break
        if not overlap:
            filtered.append(c)
        if len(filtered) >= 12:
            break
            
    return filtered

def run():
    print("[CRATER DETECTION VISUALIZATION]")
    tar_path = "podklady/AFC_images.tar.gz"
    if not os.path.exists(tar_path):
        tar_path = r"c:\Users\vikto\Disk Google\Radixal\Zakázky\2026_026 Hera Space Probe Code Contest\podklady\AFC_images.tar.gz"
    if not os.path.exists(tar_path):
        print(f"Error: {tar_path} not found.")
        return

    tf = tarfile.open(tar_path, 'r:gz')
    valid_members = [m for m in tf.getmembers() if m.name.endswith('.png') and not os.path.basename(m.name).startswith('._')]
    
    # Take a frame with clear surface morphology
    sample_member = valid_members[3]
    f = tf.extractfile(sample_member)
    img = Image.open(f).convert('RGB')
    gray = img.convert('L')
    w, h = gray.size
    raw_bytes = gray.tobytes()

    print(f"Processing frame: {sample_member.name} ({w}x{h} px)...")
    simulated_altitude_m = 11800.0 # 11.8 km from Didymos surface
    craters = detect_crater_circles(raw_bytes, w, h, simulated_altitude_m)

    print(f"\nSuccessfully identified {len(craters)} crater circles on asteroid surface:")
    print("-" * 75)
    print(f" {'ID':<4} | {'Center (X, Y)':<16} | {'Radius':<8} | {'Metric Diameter':<18} | {'Confidence':<10}")
    print("-" * 75)

    draw = ImageDraw.Draw(img)

    for idx, c in enumerate(craters):
        cx, cy, r = c['cx'], c['cy'], c['radius']
        diam_m = c['diam_m']
        conf = c['confidence']
        print(f" #{idx+1:<3} | ({cx:>4}, {cy:>4}) px    | {r:>3} px    | {diam_m:>6.1f} meters     | {conf:>3}%")

        # Draw green circle overlay
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 255, 100), width=3)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 50, 50), outline=(255, 255, 255))
        draw.text((cx + r + 4, cy - 8), f"#{idx+1} D={diam_m:.1f}m ({conf}%)", fill=(0, 255, 100))

    out_path = "media/detected_craters_sample.jpg"
    img.save(out_path, "JPEG", quality=90)
    print("-" * 75)
    print(f"Overlay visualization saved to: {out_path}")

if __name__ == "__main__":
    run()
