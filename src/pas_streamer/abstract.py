# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;streamer

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasStreamerVersion)#
#echo(__FILEPATH__)#
"""

from dpt_module_loader import NamedClassLoader
from dpt_runtime.iterator import Iterator
from dpt_runtime.not_implemented_exception import NotImplementedException
from dpt_runtime.supports_mixin import SupportsMixin
from dpt_threading.thread_lock import ThreadLock

class Abstract(Iterator, SupportsMixin):
    """
The abstract streamer defines the to be implemented interface. A streamer
interface is similar to a file one.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=invalid-name, unused-argument

    __slots__ = [ "__weakref__",
                  "_io_chunk_size",
                  "_lock",
                  "_log_handler",
                  "stream_size",
                  "timeout_retries"
                ] + SupportsMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout_retries = 5):
        """
Constructor __init__(Abstract)

:param timeout_retries: Retries before timing out

:since: v1.0.0
        """

        SupportsMixin.__init__(self)

        self._io_chunk_size = 65536
        """
IO chunk size
        """
        self._lock = ThreadLock()
        """
Thread safety lock
        """
        self._log_handler = NamedClassLoader.get_singleton("dpt_logging.LogHandler", False)
        """
Retries before timing out
        """
        self.stream_size = -1
        """
Requested stream size
        """
        self.timeout_retries = (5 if (timeout_retries is None) else timeout_retries)
        """
Retries before timing out
        """
    #

    def __del__(self):
        """
Destructor __del__(Abstract)

:since: v1.0.0
        """

        self.close()
    #

    def __next__(self):
        """
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v1.0.0
        """

        try:
            with self._lock:
                if (self.is_eof):
                    self.close()
                    raise StopIteration()
                #

                return self.read()
            #
        except StopIteration: raise
        except Exception as handled_exception:
            if (self._log_handler is not None): self._log_handler.debug(handled_exception, context = "pas_streamer")
            raise StopIteration()
        #
    #

    @property
    def io_chunk_size(self):
        """
Returns the IO chunk size to be used for reading.

:return: (int) IO chunk size
:since:  v1.0.0
        """

        return self._io_chunk_size
    #

    @io_chunk_size.setter
    def io_chunk_size(self, chunk_size):
        """
Sets the IO chunk size to be used for reading.

:param chunk_size: IO chunk size

:since: v1.0.0
        """

        self._io_chunk_size = chunk_size
    #

    @property
    def is_eof(self):
        """
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def is_resource_valid(self):
        """
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        return False
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def is_url_supported(self, url):
        """
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v1.0.0
        """

        return False
    #

    def open_url(self, url):
        """
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v1.0.0
        """

        return False
    #

    def read(self, n = None):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def seek(self, offset):
        """
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v1.0.0
        """

        return -1
    #

    def set_range(self, range_start, range_end):
        """
Define a range to be streamed.

:param range_start: First byte of range
:param range_end: Last byte of range

:return: (bool) True if valid
:since:  v1.0.0
        """

        # pylint: disable=redefined-variable-type

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_range({1:d}, {2:d})- (#echo(__LINE__)#)", self, range_start, range_end, context = "pas_streamer")
        _return = False

        with self._lock:
            if (range_start >= 0 and range_start <= range_end):
                position = self.tell()

                if (position == range_start): _return = True
                elif (self.is_supported("seeking")): _return = self.seek(range_start)
            #

            if (_return): self.stream_size = 1 + (range_end - range_start)
        #

        return _return
    #

    def tell(self):
        """
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v1.0.0
        """

        raise NotImplementedException()
    #
#
