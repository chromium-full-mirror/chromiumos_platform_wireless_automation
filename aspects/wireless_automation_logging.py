# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import logging


def setup_logging(logger_name, format_string=None,
                  output_stream=None, level=None):
    """
    This returns the loggers used across wireless_automation. A new logger
    can be specified by passing in an unused logger_name. This provides us
    a single place to customize our logger's behavior.

    @param logger_name: The name of the logger. This name can be used
        across files to access the same logger.
    @param format_string: The format of the log message this logger prints.
    @param output_stream: The stream to write logs message to
    @return: a log object that may be used :
        log.debug('Print this at the debug level ')
    """
    if format_string is None:
        format_string = ' %(name)s - %(filename)s - %(lineno)d- %(message)s'
    log = logging.getLogger(logger_name)

    if level is None:
        level = logging.DEBUG   # =0, so we catch ALL logging levels.
    log.setLevel(level)

    stream_handler = logging.StreamHandler(output_stream)
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format_string)
    stream_handler.setFormatter(formatter)
    # Don't append to the list, replace it. Otherwise we get one more
    # output stream for every call to this function.
    log.handlers = [stream_handler]
    log.propagate = False
    return log
