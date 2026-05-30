# setup_icon.py - Complete icon setup for BXZ

import os
import sys
import subprocess
from pathlib import Path

def setup_bxz_icon():
    """Complete setup for BXZ file icons"""
    
    print("=" * 50)
    print("BXZ File Icon Setup")
    print("=" * 50)
    
    # Step 1: Create icon
    print("\n📦 Step 1: Creating icon...")
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create ICO file
        sizes = [16, 24, 32, 48, 64, 96, 128, 256]
        images = []
        
        for size in sizes:
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Gradient background
            for i in range(size):
                ratio = i / size
                r = int(102 * (1 - ratio) + 118 * ratio)
                g = int(126 * (1 - ratio) + 75 * ratio)
                b = int(234 * (1 - ratio) + 162 * ratio)
                draw.rectangle([(0, i), (size, i+1)], fill=(r, g, b, 255))
            
            # Border
            border = max(1, size // 32)
            draw.rectangle([(border, border), (size - border, size - border)], 
                          outline=(255, 255, 255, 200), width=border)
            
            # Brackets
            if size >= 32:
                bracket = size // 3
                center = size // 2
                
                # Left bracket
                draw.line([(center - bracket//2, center - bracket//2),
                          (center - bracket//4, center),
                          (center - bracket//2, center + bracket//2)], 
                         fill=(255, 255, 255), width=max(2, size//32))
                
                # Right bracket
                draw.line([(center + bracket//2, center - bracket//2),
                          (center + bracket//4, center),
                          (center + bracket//2, center + bracket//2)], 
                         fill=(255, 255, 255), width=max(2, size//32))
            
            images.append(img)
        
        # Save ICO
        images[0].save('bxz.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
        print("✓ bxz.ico created")
        
        # Save PNG
        images[-1].save('bxz.png')
        print("✓ bxz.png created")
        
    except ImportError:
        print("Installing Pillow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
        # Retry icon creation
        
    # Step 2: Register in Windows
    print("\n📦 Step 2: Registering file association...")
    
    if sys.platform == 'win32':
        icon_path = os.path.abspath("bxz.ico")
        
        commands = [
            f'reg add "HKCU\\Software\\Classes\\.bxz" /ve /d "BXZFile" /f',
            f'reg add "HKCU\\Software\\Classes\\BXZFile\\DefaultIcon" /ve /d "{icon_path}" /f',
            f'reg add "HKCU\\Software\\Classes\\BXZFile\\shell\\open\\command" /ve /d "\\"{sys.executable}\\" \\"%1\\"" /f',
            f'reg add "HKCU\\Software\\Classes\\BXZFile\\shell\\edit\\command" /ve /d "notepad.exe \\"%1\\"" /f',
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True)
        
        print("✓ Registry entries added")
        
        # Refresh icon cache
        print("\n📦 Step 3: Refreshing icon cache...")
        subprocess.run('ie4uinit.exe -show', shell=True)
        print("✓ Icon cache refreshed")
        
    # Step 3: Create file template
    print("\n📦 Step 4: Creating BXZ file template...")
    
    template = '''// BXZ Program
// Created with BXZ IDE

print("Hello BXZ World!");

// Variables
let name = "Developer";
let version = "1.0.0";

print("Welcome " + name + " to BXZ v" + version);

// Your code here...
'''
    
    with open("template.bxz", "w", encoding='utf-8') as f:
        f.write(template)
    print("✓ template.bxz created")
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNow you can:")
    print("  • Double-click .bxz files to open with BXZ")
    print("  • .bxz files will show the custom icon")
    print("  • Use template.bxz as a starting point")
    print("=" * 50)

if __name__ == "__main__":
    setup_bxz_icon()