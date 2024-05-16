import subprocess
from version import __version__

def call_cpp_program():
    result = subprocess.run(["/app/hello_cpp"], capture_output=True, text=True)
    print(result.stdout)
    print(f"Python Version: {__version__}")

if __name__ == "__main__":
    call_cpp_program()