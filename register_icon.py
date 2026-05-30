# register_icon.py - Register .bxz file icon in Windows

import os
import sys
import subprocess

def register_bxz_icon():
    """Register .bxz file icon in Windows registry"""
    
    if sys.platform != 'win32':
        print("This script is for Windows only")
        return False
    
    icon_path = os.path.abspath("bxz.ico")
    
    if not os.path.exists(icon_path):
        print(f"Icon not found: {icon_path}")
        print("Run create_icon.py first")
        return False
    
    # Registry commands
    commands = [
        # Create file association
        f'reg add "HKCU\\Software\\Classes\\.bxz" /ve /d "BXZFile" /f',
        f'reg add "HKCU\\Software\\Classes\\.bxz" /v "Content Type" /d "text/plain" /f',
        
        # Create shell command
        f'reg add "HKCU\\Software\\Classes\\BXZFile\\DefaultIcon" /ve /d "{icon_path}" /f',
        f'reg add "HKCU\\Software\\Classes\\BXZFile\\shell\\open\\command" /ve /d "\\"{sys.executable}\\" \\"%1\\"" /f',
        f'reg add "HKCU\\Software\\Classes\\BXZFile\\shell\\edit\\command" /ve /d "notepad.exe \\"%1\\"" /f',
        
        # Add to Open With list
        f'reg add "HKCU\\Software\\Classes\\Applications\\bxz.exe\\SupportedTypes" /v ".bxz" /d "" /f',
        f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.bxz" /v "Progid" /d "BXZFile" /f',
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, capture_output=True)
            print(f"✓ {cmd[:50]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Refresh icon cache
    subprocess.run('ie4uinit.exe -show', shell=True)
    subprocess.run('taskkill /f /im explorer.exe', shell=True)
    subprocess.run('start explorer.exe', shell=True)
    
    print("\n✅ .bxz file association registered!")
    print("Icon registered. You may need to restart Windows Explorer.")
    return True

if __name__ == "__main__":
    register_bxz_icon()