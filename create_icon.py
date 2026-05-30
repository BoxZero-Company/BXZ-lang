# create_icon.py - ساخت آیکون برای BXZ Language

from PIL import Image, ImageDraw, ImageFont
import os

def create_bxz_icon():
    """Create professional icon for .bxz files"""
    
    # Create a 256x256 image with transparent background
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Create image
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        primary_color = (102, 126, 234)  # #667eea
        secondary_color = (118, 75, 162)  # #764ba2
        text_color = (255, 255, 255)
        
        # Draw gradient background (simulated with rectangle)
        for i in range(size):
            ratio = i / size
            r = int(primary_color[0] * (1 - ratio) + secondary_color[0] * ratio)
            g = int(primary_color[1] * (1 - ratio) + secondary_color[1] * ratio)
            b = int(primary_color[2] * (1 - ratio) + secondary_color[2] * ratio)
            draw.rectangle([(0, i), (size, i+1)], fill=(r, g, b, 255))
        
        # Draw border
        border_width = max(2, size // 64)
        draw.rectangle([(border_width, border_width), 
                       (size - border_width, size - border_width)], 
                       outline=(255, 255, 255, 200), width=border_width)
        
        # Draw "<>" symbol for code
        if size >= 32:
            # Draw angle brackets
            bracket_size = size // 3
            bracket_pos = size // 2
            
            # Left bracket <
            points_left = [
                (bracket_pos - bracket_size//2, bracket_pos - bracket_size//2),
                (bracket_pos - bracket_size//4, bracket_pos),
                (bracket_pos - bracket_size//2, bracket_pos + bracket_size//2)
            ]
            draw.line(points_left, fill=text_color, width=max(2, size//32))
            
            # Right bracket >
            points_right = [
                (bracket_pos + bracket_size//2, bracket_pos - bracket_size//2),
                (bracket_pos + bracket_size//4, bracket_pos),
                (bracket_pos + bracket_size//2, bracket_pos + bracket_size//2)
            ]
            draw.line(points_right, fill=text_color, width=max(2, size//32))
        
        # Draw "BXZ" text for larger sizes
        if size >= 64:
            try:
                font = ImageFont.truetype("arial.ttf", size // 4)
            except:
                font = ImageFont.load_default()
            
            text = "BXZ"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size - text_width) // 2
            text_y = size - text_height - size // 6
            draw.text((text_x, text_y), text, fill=text_color, font=font)
        
        images.append(img)
    
    # Save as ICO (Windows)
    if images:
        # Save multi-size ICO
        images[0].save('bxz.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
        print("✅ Created bxz.ico")
    
    # Save as PNG for other uses
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for i in range(256):
        ratio = i / 256
        r = int(primary_color[0] * (1 - ratio) + secondary_color[0] * ratio)
        g = int(primary_color[1] * (1 - ratio) + secondary_color[1] * ratio)
        b = int(primary_color[2] * (1 - ratio) + secondary_color[2] * ratio)
        draw.rectangle([(0, i), (256, i+1)], fill=(r, g, b, 255))
    
    # Draw border
    draw.rectangle([(2, 2), (254, 254)], outline=(255, 255, 255, 200), width=3)
    
    # Draw brackets
    bracket_size = 80
    center = 128
    
    points_left = [(center - bracket_size//2, center - bracket_size//2),
                   (center - bracket_size//4, center),
                   (center - bracket_size//2, center + bracket_size//2)]
    draw.line(points_left, fill=text_color, width=5)
    
    points_right = [(center + bracket_size//2, center - bracket_size//2),
                    (center + bracket_size//4, center),
                    (center + bracket_size//2, center + bracket_size//2)]
    draw.line(points_right, fill=text_color, width=5)
    
    # Draw text
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((center - 60, center + 60), "BXZ", fill=text_color, font=font)
    
    img.save('bxz.png')
    print("✅ Created bxz.png")
    
    return True

if __name__ == "__main__":
    # Install Pillow if not installed
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_bxz_icon()
    except ImportError:
        print("Installing Pillow...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
        create_bxz_icon()