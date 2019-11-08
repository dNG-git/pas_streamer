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

from dpt_runtime.io_exception import IOException
from dpt_vfs import Implementation

from .abstract import Abstract

class VfsBased(Abstract):
    """
The "VfsBased" streamer integrates VFS implementations with data streaming
capabilities.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "_wrapped_resource" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout_retries = 5):
        """
Constructor __init__(File)

:param timeout_retries: Retries before timing out

:since: v1.0.0
        """

        Abstract.__init__(self, timeout_retries)

        self._wrapped_resource = None
        """
Active file resource
        """
    #

    @property
    def is_eof(self):
        """
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v1.0.0
        """

        with self._lock:
            return (True if (self._wrapped_resource is None) else self._wrapped_resource.is_eof)
        #
    #

    @property
    def is_resource_valid(self):
        """
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        with self._lock: return (self._wrapped_resource is not None)
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        with self._lock:
            return self._wrapped_resource.size
        #
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        with self._lock:
            if (self._wrapped_resource is not None):
                if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.close()- (#echo(__LINE__)#)", self, context = "pas_streamer")

                try: self._wrapped_resource.close()
                finally:
                    self._wrapped_resource = None
                    self.supported_features['seeking'] = False
                #
            #
        #
    #

    def is_url_supported(self, url):
        """
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v1.0.0
        """

        return Implementation.load_vfs_url(url).is_valid
    #

    def open_url(self, url):
        """
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v1.0.0
        """

        _return = False

        vfs_object = Implementation.load_vfs_url(url, True)

        if (vfs_object.is_valid):
            self._wrapped_resource = vfs_object
            self.supported_features['seeking'] = vfs_object.is_supported("seek")

            _return = True
        #

        return _return
    #

    def read(self, n = None):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        _return = None

        if (n is None): n = self.io_chunk_size

        if (self._wrapped_resource is None): raise IOException("Streamer resource is invalid")
        elif (self.stream_size != 0 and (not self._wrapped_resource.is_eof)):
            with self._lock:
                # Thread safety
                is_size_limited = (self.stream_size > 0)

                if (self._wrapped_resource is None): raise IOException("Streamer resource is invalid")
                elif ((self.stream_size < 0 or is_size_limited) and (not self._wrapped_resource.is_eof)):
                    if (is_size_limited):
                        if (n < 1): self.stream_size = 0
                        elif (n > self.stream_size): n = self.stream_size
                        else: self.stream_size -= n
                    #

                    _return = (self._wrapped_resource.read(n) if (n > 0) else self._wrapped_resource.read())
                #
            #
        #

        return _return
    #

    def seek(self, offset):
        """
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.seek({1:d})- (#echo(__LINE__)#)", self, offset, context = "pas_streamer")

        with self._lock:
            return (-1 if (self._wrapped_resource is None) else self._wrapped_resource.seek(offset))
        #
    #

    def tell(self):
        """
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v1.0.0
        """

        with self._lock:
            if (self._wrapped_resource is None): raise IOException("Streamer resource is invalid")
            return self._wrapped_resource.tell()
        #
    #
#
