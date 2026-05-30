# polyglot/python_bridge.py
import subprocess
import sys
import json

class PythonBridge:
    @staticmethod
    def run_python(code: str):
        """Execute Python code"""
        try:
            exec(code, {})
            return True, "Python code executed successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def run_python_file(filename: str):
        """Execute Python file"""
        try:
            result = subprocess.run(
                [sys.executable, filename],
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)