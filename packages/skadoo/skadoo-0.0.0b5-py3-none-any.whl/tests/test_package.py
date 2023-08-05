import os
import sys
import logging
import subprocess

import skadoo
from . import test_dir


def test_root():
    python = sys.executable

    result = subprocess.check_output(
        [python, os.path.join(test_dir, "examples.py"), "a"]
    ).decode(sys.stdout.encoding)

    assert "a" in str(result)
    assert "Commands not recognized" not in str(result)


def test_flag():
    python = sys.executable

    result = subprocess.check_output(
        [python, os.path.join(test_dir, "examples.py"), "a", "-y=1", "--z", "2"]
    ).decode(sys.stdout.encoding)

    print(result)

    assert "a x= y=1 z=2" in str(result)
    assert "Commands not recognized" not in str(result)
