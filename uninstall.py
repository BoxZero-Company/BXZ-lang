#!/usr/bin/env python3
# uninstall.py - Complete BXZ Language Uninstaller
# Professional uninstaller with full cleanup

import sys
import os
import subprocess
import platform
import shutil
import json
import time
import ctypes
from pathlib import Path
from datetime import datetime

# ANSI color codes for beautiful output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def print_color(text, color=Colors.CYAN):
    """Print colored text"""
    if platform.system().lower() == "windows":
        print(text)
    else:
        print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Print section header"""
    print()
    print_color("=" * 60, Colors.BLUE)
    print_color(f" {text}", Colors.BOLD + Colors.CYAN)
    print_color("=" * 60, Colors.BLUE)

def print_success(text):
    print_color(f"✅ {text}", Colors.GREEN)

def print_error(text):
    print_color(f"❌ {text}", Colors.RED)

def print_warning(text):
    print_color(f"⚠️  {text}", Colors.YELLOW)

def print_info(text):
    print_color(f"ℹ️  {text}", Colors.CYAN)

def print_progress(text):
    print_color(f"   {text}", Colors.DIM)

def run_as_admin():
    """Request administrator privileges on Windows"""
    if platform.system().lower() == "windows":
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                return True
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        except:
            return False
    return True

class BXZUninstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.user_home = Path.home()
        self.bxz_paths = []
        self.removed_count = 0
        self.failed_count = 0
        self.start_time = datetime.now()
        
    def find_all_bxz_files(self):
        """Find all BXZ related files and directories"""
        print_progress("Scanning for BXZ files...")
        
        # Common BXZ paths
        paths_to_check = [
            Path.cwd(),
            self.user_home / ".bxz-ide",
            self.user_home / "AppData/Roaming/bxz" if self.system == "windows" else self.user_home / ".config/bxz",
            self.user_home / "Desktop",
            self.user_home / "Documents",
            Path(sys.prefix) / "Scripts" if self.system == "windows" else Path(sys.prefix) / "bin",
        ]
        
        # Add Python site packages
        try:
            import site
            for site_dir in site.getsitepackages():
                paths_to_check.append(Path(site_dir))
        except:
            pass
        
        # Patterns to search
        patterns = [
            "*.bxz", "bxz*", "*.bxz-ide", "BXZ IDE*", "bxz_lang*",
            "bxz.py", "bxz.exe", "bxz.bat", "bxz.cmd", "bxz.sh"
        ]
        
        for path in paths_to_check:
            if path.exists():
                for pattern in patterns:
                    try:
                        self.bxz_paths.extend(path.glob(pattern))
                    except:
                        pass
        
        # Remove duplicates
        self.bxz_paths = list(set(self.bxz_paths))
        print_success(f"Found {len(self.bxz_paths)} BXZ-related items")
        
    def uninstall_pip_package(self):
        """Remove pip package"""
        print_progress("Removing pip package...")
        try:
            # Try multiple package names
            packages = ["bxz-lang", "bxz-advanced", "bxz-language", "bxz-ide"]
            for package in packages:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "uninstall", package, "-y"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print_success(f"Removed pip package: {package}")
                    return True
            return True
        except Exception as e:
            print_error(f"Could not remove pip package: {e}")
            return False
    
    def remove_executables(self):
        """Remove BXZ executables and scripts"""
        print_progress("Removing executables...")
        
        executables = ["bxz.bat", "bxz.cmd", "bxz", "bxz.exe", "bxz.sh"]
        for exe in executables:
            # Check current directory
            if Path(exe).exists():
                try:
                    Path(exe).unlink()
                    print_success(f"Removed {exe}")
                except:
                    pass
            
            # Check system directories
            system_paths = [
                Path(sys.prefix) / "Scripts" / exe,
                Path(sys.prefix) / "bin" / exe,
                Path("/usr/local/bin") / exe,
                Path("/usr/bin") / exe,
            ]
            
            for path in system_paths:
                try:
                    if path.exists():
                        path.unlink()
                        print_success(f"Removed {path}")
                except PermissionError:
                    print_warning(f"Permission denied: {path} (run as admin)")
                except:
                    pass
    
    def remove_registry_entries(self):
        """Remove Windows registry entries"""
        if self.system != "windows":
            return True
        
        print_progress("Removing registry entries...")
        
        registry_keys = [
            "HKCU\\Software\\Classes\\.bxz",
            "HKCU\\Software\\Classes\\BXZFile",
            "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\.bxz",
            "HKCR\\.bxz",
            "HKCR\\BXZFile",
            "HKCU\\Software\\BXZ Language",
            "HKLM\\Software\\BXZ Language",
        ]
        
        for key in registry_keys:
            try:
                subprocess.run(f'reg delete "{key}" /f', shell=True, capture_output=True)
                print_success(f"Removed registry key: {key}")
            except:
                pass
        
        # Refresh icon cache
        try:
            subprocess.run('ie4uinit.exe -show', shell=True, capture_output=True)
            subprocess.run('taskkill /f /im explorer.exe', shell=True, capture_output=True)
            subprocess.run('start explorer.exe', shell=True, capture_output=True)
            print_success("Refreshed icon cache")
        except:
            pass
        
        return True
    
    def remove_extensions(self):
        """Remove BXZ extensions"""
        print_progress("Removing extensions...")
        
        ext_paths = [
            self.user_home / ".bxz-ide/extensions",
            self.user_home / ".bxz/extensions",
            self.user_home / "AppData/Roaming/bxz/extensions" if self.system == "windows" else self.user_home / ".config/bxz/extensions",
        ]
        
        removed = 0
        for path in ext_paths:
            if path.exists():
                try:
                    shutil.rmtree(path)
                    removed += 1
                    print_success(f"Removed extensions: {path}")
                except Exception as e:
                    print_error(f"Could not remove {path}: {e}")
        
        return removed > 0
    
    def remove_cache(self):
        """Remove cache files"""
        print_progress("Removing cache files...")
        
        cache_paths = [
            Path(tempfile.gettempdir()) / "bxz_cache",
            self.user_home / ".cache/bxz",
            self.user_home / "AppData/Local/bxz" if self.system == "windows" else self.user_home / ".local/share/bxz",
            Path(sys.prefix) / "bxz_cache",
        ]
        
        removed = 0
        for path in cache_paths:
            if path.exists():
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    removed += 1
                    print_success(f"Removed cache: {path}")
                except:
                    pass
        
        return removed > 0
    
    def remove_projects(self, ask=True):
        """Remove BXZ projects"""
        projects_path = Path.cwd() / "projects"
        
        if not projects_path.exists():
            return True
        
        if ask:
            response = input(f"\n📁 Remove projects directory? ({projects_path}) [y/N]: ")
            if response.lower() != 'y':
                print_info("Keeping projects directory")
                return True
        
        try:
            shutil.rmtree(projects_path)
            print_success("Removed projects directory")
            return True
        except Exception as e:
            print_error(f"Could not remove projects: {e}")
            return False
    
    def remove_config(self):
        """Remove configuration files"""
        print_progress("Removing config files...")
        
        config_paths = [
            self.user_home / ".bxzrc",
            self.user_home / ".bxz/config.json",
            self.user_home / "AppData/Roaming/bxz/config.json" if self.system == "windows" else self.user_home / ".config/bxz/config.json",
            Path.cwd() / ".bxzconfig",
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    path.unlink()
                    print_success(f"Removed config: {path}")
                except:
                    pass
    
    def remove_path_from_environment(self):
        """Remove BXZ from PATH environment variable"""
        if self.system != "windows":
            return
        
        print_progress("Removing from PATH...")
        
        try:
            import winreg
            
            # Get current PATH
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ)
            try:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
            except:
                current_path = ""
            winreg.CloseKey(key)
            
            # Remove BXZ paths
            install_dir = str(Path.cwd())
            paths = current_path.split(";")
            new_paths = [p for p in paths if p and install_dir not in p and "bxz" not in p.lower()]
            new_path = ";".join(new_paths)
            
            if new_path != current_path:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                winreg.CloseKey(key)
                print_success("Removed BXZ from PATH")
            else:
                print_info("BXZ not found in PATH")
                
        except Exception as e:
            print_error(f"Could not remove from PATH: {e}")
    
    def clean_pycache(self):
        """Remove Python cache files"""
        print_progress("Cleaning Python cache...")
        
        cache_dirs = ["__pycache__", ".pytest_cache", ".mypy_cache"]
        for cache_dir in cache_dirs:
            for path in Path.cwd().glob(f"**/{cache_dir}"):
                try:
                    shutil.rmtree(path)
                    print_progress(f"Removed {path}")
                except:
                    pass
        
        # Remove .pyc files
        for pyc in Path.cwd().glob("**/*.pyc"):
            try:
                pyc.unlink()
            except:
                pass
    
    def show_summary(self):
        """Show uninstall summary"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        print()
        print_header("UNINSTALL SUMMARY")
        print_color(f"  Files removed: {self.removed_count}", Colors.GREEN)
        print_color(f"  Failed: {self.failed_count}", Colors.RED if self.failed_count > 0 else Colors.GREEN)
        print_color(f"  Time: {elapsed:.2f} seconds", Colors.CYAN)
        
    def create_backup(self):
        """Create backup before uninstall"""
        print_progress("Creating backup...")
        
        backup_dir = self.user_home / f"bxz_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        items_to_backup = []
        for path in self.bxz_paths:
            if path.exists() and path.is_file():
                items_to_backup.append(path)
        
        if items_to_backup:
            try:
                backup_dir.mkdir(parents=True, exist_ok=True)
                for item in items_to_backup:
                    shutil.copy2(item, backup_dir / item.name)
                print_success(f"Backup created: {backup_dir}")
                return backup_dir
            except Exception as e:
                print_error(f"Backup failed: {e}")
        
        return None
    
    def restore_backup(self, backup_dir):
        """Restore from backup"""
        if not backup_dir or not backup_dir.exists():
            return
        
        response = input(f"\n🔄 Restore from backup? ({backup_dir}) [y/N]: ")
        if response.lower() == 'y':
            for backup_file in backup_dir.iterdir():
                try:
                    shutil.copy2(backup_file, Path.cwd() / backup_file.name)
                    print_success(f"Restored: {backup_file.name}")
                except:
                    pass
    
    def uninstall(self):
        """Main uninstall process"""
        print_header("🗑️  BXZ LANGUAGE UNINSTALLER v3.0")
        print_color(f"Platform: {platform.system()} {platform.release()}", Colors.DIM)
        print_color(f"Python: {sys.version}", Colors.DIM)
        print()
        
        # Warning
        print_warning("This will completely remove BXZ Language and all its components!")
        print_warning("This includes: packages, executables, extensions, configs, and caches")
        print()
        
        confirm = input("Are you sure you want to uninstall BXZ? (yes/NO): ")
        if confirm.lower() != 'yes':
            print_info("Uninstall cancelled.")
            return False
        
        # Create backup
        backup_dir = None
        backup_choice = input("\n📦 Create backup before uninstall? (y/N): ")
        if backup_choice.lower() == 'y':
            backup_dir = self.create_backup()
        
        print_header("UNINSTALLING BXZ")
        
        # Run uninstall steps
        steps = [
            ("Removing pip packages", self.uninstall_pip_package),
            ("Removing executables", self.remove_executables),
            ("Removing registry entries", self.remove_registry_entries),
            ("Removing extensions", self.remove_extensions),
            ("Removing cache", self.remove_cache),
            ("Removing config files", self.remove_config),
            ("Cleaning Python cache", self.clean_pycache),
            ("Removing from PATH", self.remove_path_from_environment),
        ]
        
        for step_name, step_func in steps:
            print_info(step_name + "...")
            try:
                step_func()
            except Exception as e:
                print_error(f"  Failed: {e}")
                self.failed_count += 1
        
        # Remove projects (ask separately)
        self.remove_projects(ask=True)
        
        # Find and show remaining files
        self.find_all_bxz_files()
        if self.bxz_paths:
            print_header("REMAINING FILES")
            for path in self.bxz_paths[:20]:  # Show first 20
                print_progress(str(path))
            if len(self.bxz_paths) > 20:
                print_progress(f"... and {len(self.bxz_paths) - 20} more")
            
            remove_remaining = input("\n🗑️  Remove remaining files? (y/N): ")
            if remove_remaining.lower() == 'y':
                for path in self.bxz_paths:
                    try:
                        if path.is_dir():
                            shutil.rmtree(path)
                        else:
                            path.unlink()
                        self.removed_count += 1
                    except:
                        self.failed_count += 1
                print_success(f"Removed {self.removed_count} additional files")
        
        self.show_summary()
        
        # Ask about restore
        if backup_dir:
            self.restore_backup(backup_dir)
        
        print_header("UNINSTALL COMPLETE")
        print_success("BXZ Language has been completely removed from your system!")
        print()
        print_color("Thank you for using BXZ Language! 🚀", Colors.GREEN + Colors.BOLD)
        
        # Ask for restart (Windows)
        if self.system == "windows":
            restart = input("\n🔄 Restart explorer to complete cleanup? (y/N): ")
            if restart.lower() == 'y':
                subprocess.run('taskkill /f /im explorer.exe && start explorer.exe', shell=True)
        
        return True

def main():
    # Check for admin on Windows
    if platform.system().lower() == "windows":
        try:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print_warning("Administrator privileges recommended for complete cleanup")
                print_info("Restarting with admin privileges...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()
        except:
            pass
    
    uninstaller = BXZUninstaller()
    success = uninstaller.uninstall()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    # Import tempfile here to avoid circular imports
    import tempfile
    main()