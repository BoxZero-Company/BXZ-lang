# polyglot/node_bridge.py
import subprocess
import os
import json

class NodeBridge:
    @staticmethod
    def run_node_script(script: str):
        """Run Node.js script"""
        temp_file = "temp.js"
        with open(temp_file, 'w') as f:
            f.write(script)
        
        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    @staticmethod
    def install_npm_package(package: str):
        """Install npm package"""
        result = subprocess.run(
            ['npm', 'install', '-g', package],
            capture_output=True,
            text=True
        )
        return result.returncode == 0