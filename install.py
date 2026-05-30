# install.py - Complete installer for BXZ

import sys
import os
import subprocess
import platform

def main():
    print("=" * 60)
    print("🚀 BXZ Language Installer v1.1.0")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required!")
        sys.exit(1)
    
    # Step 1: Install pip package
    print("\n📦 Installing BXZ package...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])
    
    # Step 2: Setup icon
    print("\n🖼️ Setting up BXZ icon...")
    if os.path.exists("setup_icon.py"):
        subprocess.run([sys.executable, "setup_icon.py"])
    else:
        print("⚠️ setup_icon.py not found, skipping icon setup")
    
    # Step 3: Create launcher
    print("\n🔧 Creating launcher...")
    if platform.system() == "Windows":
        with open("bxz.bat", "w") as f:
            f.write(f'@echo off\n{sys.executable} "%~dp0bxz.py" %*\n')
        print("✓ bxz.bat created")
    else:
        with open("bxz", "w") as f:
            f.write(f'#!/bin/bash\n{sys.executable} "$(dirname "$0")/bxz.py" "$@"\n')
        os.chmod("bxz", 0o755)
        print("✓ bxz executable created")
    
    # Step 4: Create sample file
    print("\n📄 Creating sample file...")
    sample = '''// Hello World in BXZ
print("Hello BXZ World!");

// Variables
let name = "Farhad";
let age = 25;
print("Name: " + name);
print("Age: " + age);

// Function
func greet(person) {
    return "Hello, " + person;
}

print(greet(name));

// Array
let numbers = [1, 2, 3, 4, 5];
print("Numbers: " + numbers);

// Loop
for (let i = 0; i < 5; i = i + 1) {
    print("Count: " + i);
}

// Conditional
let score = 85;
if (score >= 90) {
    print("Grade: A");
} else if (score >= 80) {
    print("Grade: B");
} else {
    print("Grade: C");
}
'''
    
    with open("sample.bxz", "w", encoding='utf-8') as f:
        f.write(sample)
    print("✓ sample.bxz created")
    
    print("\n" + "=" * 60)
    print("✅ BXZ Language installed successfully!")
    print("=" * 60)
    print("\n📖 Usage:")
    print("   bxz sample.bxz        - Run BXZ file")
    print("   bxz -i                - Interactive mode")
    print("   bxz -v                - Show version")
    print("\n📁 Files created:")
    print("   bxz.ico               - File icon")
    print("   bxz.png               - PNG icon")
    print("   sample.bxz            - Sample BXZ file")
    print("   template.bxz          - BXZ template")
    print("=" * 60)

if __name__ == "__main__":
    main()