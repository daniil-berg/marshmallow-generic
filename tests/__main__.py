import sys
import unittest

if __name__ == "__main__":
    try:
        pattern = sys.argv[1]
    except IndexError:
        pattern = "test*.py"
    test_suite = unittest.defaultTestLoader.discover(".", pattern=pattern)
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = test_runner.run(test_suite)
    sys.exit(not result.wasSuccessful())
