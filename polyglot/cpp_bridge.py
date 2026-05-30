# polyglot/cpp_bridge.py
import subprocess
import os

class CPPBridge:
    @staticmethod
    def compile_and_run(code: str):
        """Compile and run C++ code"""
        temp_file = "temp.cpp"
        output_file = "temp.exe" if os.name == 'nt' else "temp.out"
        
        with open(temp_file, 'w') as f:
            f.write(code)
        
        try:
            # Compile with g++
            compile_result = subprocess.run(
                ['g++', temp_file, '-o', output_file],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode == 0:
                # Run the compiled executable
                run_result = subprocess.run(
                    ['./' + output_file] if os.name != 'nt' else [output_file],
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
            for f in [temp_file, output_file]:
                if os.path.exists(f):
                    os.remove(f)