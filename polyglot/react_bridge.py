# polyglot/react_bridge.py
import subprocess
import os
import shutil

class ReactBridge:
    @staticmethod
    def create_react_app(name: str, path: str = '.'):
        """Create a new React application"""
        try:
            result = subprocess.run(
                ['npx', 'create-react-app', name],
                cwd=path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, f"React app '{name}' created"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def build_react_component(component_code: str):
        """Build a React component"""
        full_code = f"""
        import React from 'react';
        {component_code}
        export default {component_code.split('=')[0].strip()};
        """
        return full_code