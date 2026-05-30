# polyglot/csharp_bridge.py
import subprocess
import os

class CSharpBridge:
    @staticmethod
    def compile_and_run(code: str):
        """Compile and run C# code"""
        temp_file = "temp.cs"
        with open(temp_file, 'w') as f:
            f.write(code)
        
        try:
            # Compile with csc (Windows) or mcs (Linux/Mac)
            compiler = "csc" if os.name == 'nt' else "mcs"
            compile_result = subprocess.run(
                [compiler, temp_file],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode == 0:
                # Run the compiled executable
                exe_name = temp_file.replace('.cs', '.exe')
                run_result = subprocess.run(
                    [exe_name],
                    capture_output=True,
                    text=True
                )
                return True, run_result.stdout
            else:
                return False, compile_result.stderr
        except Exception as e:
            return False, str(e)
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)