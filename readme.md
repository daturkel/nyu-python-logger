# logger and tests

For completeness, run the test file two different ways:

1. with pytest, using `test.py` in the directory where both of these files live
2. in python REPL: `from test_logger import TestLogger; a = TestLogger(); a.test_log_value()`

The reason for this is that the `Logger` class has a cool functionality: when `scriptname` is set to `True`, the logger will prepend the calling script's name in each log-line, but when `Logger` is used from the console, it'll just prepend "[console]". The only way to check that this secondary function works is by testing from the console. (The relevant test for that functionality is the `test_log_value()` method.)
