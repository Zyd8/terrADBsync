import time 
import sys
import subprocess

class ErrorHandler:

    @staticmethod
    def handle_setupclass(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                ErrorHandler.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                ErrorHandler.with_error_terminate()
        return wrapper
    
    @staticmethod
    def handle_pathclass(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (FileNotFoundError) as e:
                print(f"File not found error: {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                ErrorHandler.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                ErrorHandler.with_error_terminate()
        return wrapper
    
    @staticmethod
    def handle_backupclass(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                print(f"File not found error: {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                ErrorHandler.with_error_terminate()
            except OSError as e:
                print(f"Failed to create folder: {e}")
                ErrorHandler.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                ErrorHandler.with_error_terminate()
        return wrapper
    
    @staticmethod
    def handle_sync(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute adb command {e}")
                ErrorHandler.with_error_terminate()
            except subprocess.TimeoutExpired:
                print(f"adb command timed out")
                ErrorHandler.with_error_terminate()
            except FileNotFoundError as e:
                print(f"[Sync]File not found error: {e}")
                ErrorHandler.with_error_terminate()
            except OSError as e:
                print(f"Failed to create folder: {e}")
                ErrorHandler.with_error_terminate()
            except RuntimeError as e:
                print(f"Runtime error: {e}")
                ErrorHandler.with_error_terminate()
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                ErrorHandler.with_error_terminate()
        return wrapper
    
    @staticmethod
    def with_error_terminate():
        time.sleep(3)
        sys.exit(1)
    
    @staticmethod
    def no_error_terminate():
        sys.exit(0)