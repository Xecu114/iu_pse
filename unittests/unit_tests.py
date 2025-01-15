import unittest
# from tests.timemanagement_test import TestTimeManagement

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='./unittests', pattern='*_test.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)