import subprocess
import sys
import time 

class ErrorHandler:


    @staticmethod
    def handle_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
                ErrorHandler.with_error_terminate()
            except PermissionError as e:
                print(f"Permission error: {e}")
                ErrorHandler.with_error_terminate()
            except RuntimeError as e:
                print(f"Runtime error: {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command: {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                ErrorHandler.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                ErrorHandler.with_error_terminate()
        return wrapper
    

    @staticmethod
    def with_error_terminate():
        time.sleep(5)
        sys.exit(1)
    
    
    @staticmethod
    def no_error_terminate():
        time.sleep(5)
        sys.exit(0)