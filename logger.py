""" logger.py - Dan Turkel
    a class for basic logging functionality """

import time
import os
import sys

class Logger(object):
    priorities = {'debug': 1,
                  'info': 2,
                  'warning': 3,
                  'error': 4,
                  'critical': 5 }
                  
    spacer = "    "
    
    def __init__(self, filename, priority = 'debug', datetime = False, scriptname = False):
        self.filename = filename 
        
        if not isinstance(priority, str):
            raise TypeError("priority must be a string")
        if priority.lower() in Logger.priorities:
            self.priority = Logger.priorities[priority.lower()]
        else:
            raise ValueError("priority must be 'debug', 'info', 'warning', 'error', or 'critical'")

        self.datetime = datetime
        self.scriptname = scriptname

    def _log(self, priority_level, string):
        """ internal method which returns the proper string to write to the file
            expects: priority level (int), string to write (str) 
            returns: None if the priority level is too low, otherwise the string to write to file """
        if priority_level < self.priority:
            return None
        write_string = ""
        if self.datetime:
            write_string += time.ctime()
            write_string += Logger.spacer
        if self.scriptname:
            script = os.path.basename(sys.argv[0]) if sys.argv[0] else "[console]"
            write_string += script
            write_string += Logger.spacer
        write_string += string
        write_string += "\n"
        return write_string

    def _write(self, write_string):
        """ internal method which simply writes the string created by _log to the file 
            expects: string to write to file
            returns: None """
        # no need to throw an IOError because if the file doesn't exist, this just makes it
        if write_string:
            with open(self.filename, "a") as thefile:
                thefile.write(write_string)

    """ these methods simply pass the string they are given to _log, and give the appropriate priority level
        they return nothing """
    def debug(self, string):
        self._write(self._log(1, string))

    def info(self, string):
        self._write(self._log(2, string))

    def warning(self, string):
        self._write(self._log(3, string))

    def error(self, string):
        self._write(self._log(4, string))

    def critical(self, string):
        self._write(self._log(5, string))

