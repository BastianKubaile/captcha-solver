import os
import pytest

if __name__ == "__main__":
    os.chdir("testing")
    pytest.main([
        "TestCaptchaSolver.py",
        "TestDifferenceCalculator.py",
        "TestImageReader.py",
        "TestLetterStore.py"
    ])

