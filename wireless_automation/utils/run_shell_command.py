#!/usr/bin/python
# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# From : http://stackoverflow.com/questions/1191374/subprocess-with-timeout

"""
Runs a shell command with a timeout.
"""

import subprocess
import threading
from wireless_automation.aspects import wireless_automation_logging


# pylint: disable=too-few-public-methods
class Command(object):
    """
    Run a shell command with a timeout.
    >>>command = Command('sleep 10')
    >>>command.run(timeout=3)

    """
    def __init__(self, cmd, logger=None):
        """
        :param cmd:  String.
        :param logger:
        :return:
        """
        self.cmd = cmd
        self.process = None
        self.output = None
        self.error = None
        self.timeout = None
        if logger:
            self.logger = logger
        else:
            self.logger = wireless_automation_logging.setup_logging('shell')

    def run(self, timeout, shell=True):
        """
        Run the command.
        :param timeout: Seconds to wait before killing the command
        :param shell: Use a shell to run it.
        """
        def target():
            """
            Internal function used to hold the subprocess work
            """
            self.logger.debug('Thread started')
            self.process = subprocess.Popen(self.cmd, shell=shell,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            (self.output, self.error) = self.process.communicate()
            self.logger.debug('stdout: %s' % self.output.replace('\n', ' '))
            self.logger.debug('Thread finished')

        self.timeout = timeout
        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.logger.error("Process '%s' took longer then %s seconds" %
                              (self.cmd, self.timeout))
            self.logger.error('Killing it')
            self.process.terminate()
            self.process.kill()
            thread.join()

        self.logger.debug('return code: %s ' % self.process.returncode)


if __name__ == '__main__':
    #pylint: disable=invalid-name
    command = Command("echo 'Process started'; "
                      "sleep 2; echo 'Process finished'")
    command.run(timeout=3)
    command.run(timeout=1)
