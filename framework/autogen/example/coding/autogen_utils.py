import os
import sys
from contextlib import redirect_stdout
from contextlib import contextmanager

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # Ensure real-time writing

    def flush(self):
        for f in self.files:
            f.flush()

@contextmanager
def redirect_stdout_to_file_and_terminal(file):
    original_stdout = sys.stdout
    sys.stdout = file
    try:
        yield
    finally:
        sys.stdout = original_stdout