""" test_logger.py -- Dan Turkel 
    a series of tests for the logger.py Logger class """

from logger import Logger
import time
import os
import sys
import pytest

class TestLogger(object):

    def setup_class(self):
        # make sure there's no "test.txt" so we can test creating it
        if os.path.isfile("test.txt"):
            os.remove("test.txt")
        # we don't rely on the existence of any base data

    def teardown_class(self):
        # get rid of what we made
        os.remove("test.txt")
        # note, "_.txt" never gets written to, so we don't have to delete it because it doesn't exist

    def test_init_priority_type(self):
        # __init__ should throw type error for non-string priority
        with pytest.raises(TypeError):
            example = Logger("_.txt", priority = 2)

    def test_init_priority_set(self):
        # __init__, when given a valid priority, should downcase it before storing its Logger.priorities value
        example = Logger("_.txt", priority = "DeBuG")
        assert example.priority == Logger.priorities["debug"]

    def test_init_priority_value(self):
        # __init__ should throw a ValueError for invalid priority strings
        with pytest.raises(ValueError):
            example = Logger("_.txt", priority = "testing")

    def test_log_priority_value(self):
        # _log should return None if and only if priority_level argument is less than instance priority
        warning_ex = Logger("_.txt", priority = "warning") # Logger.priorities["warning"] = 3
        assert warning_ex._log(1, "") is None
        assert warning_ex._log(2, "") is None
        assert warning_ex._log(3, "") is not None
        assert warning_ex._log(4, "") is not None
        assert warning_ex._log(5, "") is not None

    def test_log_value(self):
        # _log's non-None return value should respect its arguments
        test_string = "hello"

        # with datetime = False, scriptname = False, we should just append "\n"
        plain_string = Logger("_.txt", priority = "debug", datetime = False, scriptname = False)
        assert plain_string._log(1, test_string) == test_string + "\n"

        # with datetime = True, scriptname = False, we should also prepend datetime followed by a spacer
        datetime = Logger("_.txt", priority = "debug", datetime = True, scriptname = False)
        assert datetime._log(1, test_string) == time.ctime() + Logger.spacer + test_string + "\n"

        # with datetime = False, scriptname = True, we should prepend scriptname followed by a spacer
        scriptname = Logger("_.txt", priority = "debug", datetime = False, scriptname = True)
        # to get full testing, you have to run pytest and run this method from the console, i suppose
        if sys.argv[0]:
            assert scriptname._log(1, test_string) == (os.path.basename(sys.argv[0]) + Logger.spacer
                                                       + test_string + "\n")
        else:
            assert scriptname._log(1, test_string) == "[console]" + Logger.spacer + test_string + "\n"

        # with datetime = True, scriptname = True, we should prepend datetime, spacer, scriptname, spacer
        both = Logger("_.txt", priority = "debug", datetime = True, scriptname = True)
        if sys.argv[0]:
            assert both._log(1, test_string) == (time.ctime() + Logger.spacer + os.path.basename(sys.argv[0]) 
                                                 + Logger.spacer + test_string + "\n") 
        else:
            assert both._log(1, test_string) == (time.ctime() + Logger.spacer  + "[console]" + Logger.spacer 
                                                 + test_string + "\n")

    def test_write(self):
        # _write should create a file if there is none
        # note that in setup_class we made sure there was no test.txt
        create_file = Logger("test.txt")
        create_file._write("this will create the file\n")
        assert os.path.isfile("./test.txt")
        # and once we've created the file, writing again should simply append the new text
        create_file._write("this is a second line")
        thefile = open(create_file.filename).readlines()
        assert thefile[0] == "this will create the file\n"
        assert thefile[1] == "this is a second line"

    """ there's nothing to test for debug/warning/info etc because they just use hard-coded valid parameters
        to run methods which we've already tested """

    """ if user is using only the methods intended for public use (init/debug/info/warning/error/critical), i'm 
        not aware of any possible python errors they could encounter. they could provide non-bools for 
        datetime or scriptname, but they'd just be coerced into bools later """
