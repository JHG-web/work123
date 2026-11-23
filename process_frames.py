import os
from PIL import Image

frames_dir = r"c:\work123\video_data\frames"
output_dir = r"c:\work123\video_data\curated_frames"
os.makedirs(output_dir, exist_ok=True)

# Select key frames representing each geometric concept and step
key_frames = {
    "01_cube_flat": "frame_03.jpg",       # 평면 전개도 (직육면체)
    "02_cube_pulling": "frame_04.jpg",    # 당기는 과정 (직육면체)
    "03_cube_3d": "frame_06.jpg",         # 완성된 입체 (직육면체)
    "04_pyramid_flat": "frame_08.jpg",    # 평면 전개도 (삼각뿔)
    "05_pyramid_3d": "frame_09.jpg",      # 완성된 입체 (삼각뿔)
    "06_cylinder_flat": "frame_12.jpg",   # 원기둥 전개도와 실 꿰임
    "07_cylinder_3d": "frame_13.jpg",     # 완성된 원기둥
    "08_cylinder_detail": "frame_15.jpg", # 원기둥 실 통과 디테일
    "09_star_lacing": "frame_17.jpg",     # 오각뿔 실 꿰는 방법
    "10_star_flat": "frame_19.jpg",       # 오각뿔 펼친 상태 (별 모양)
    "11_star_3d": "frame_21.jpg"          # 오각뿔 완성 (당겼을 때)
}

for name, fname in key_frames.items():
    img_path = os.path.join(frames_dir, fname)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        w, h = img.size
        # Crop to focus on the geometric figure and hand action (crop plant on top and excess bottom)
        # 1080 x 1920: keep width, crop y from 280 to 1820
        box = (0, 280, 1080, 1820)
        cropped = img.crop(box)
        # Resize to standard height while preserving quality
        cropped.save(os.path.join(output_dir, f"{name}.jpg"), quality=95)
        print(f"Saved {name}.jpg ({cropped.size})")
