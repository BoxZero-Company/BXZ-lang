# polyglot/js_bridge.py
import subprocess
import json

class JSBridge:
    @staticmethod
    def run_javascript(code: str):
        """Execute JavaScript using Node.js"""
        try:
            result = subprocess.run(
                ['node', '-e', code],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0, result.stdout
        except subprocess.TimeoutExpired:
            return False, "JavaScript execution timeout"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def evaluate_expression(expr: str):
        """Evaluate JavaScript expression"""
        return JSBridge.run_javascript(f'console.log({expr})')