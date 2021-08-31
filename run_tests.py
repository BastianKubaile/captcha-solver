import os
import pytest

if __name__ == "__main__":
    pytest.main([
        "testing/TestCaptchaSolver.py",
        "testing/TestDifferenceCalculator.py",
        "testing/TestImageReader.py",
        "testing/TestLetterStore.py"
    ])

