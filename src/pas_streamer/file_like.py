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

# pylint: disable=import-error,no-name-in-module

from dpt_runtime.io_exception import IOException
from dpt_settings import Settings
from dpt_vfs import FileLikeWrapperMixin

from .abstract import Abstract

class FileLike(FileLikeWrapperMixin, Abstract):
    """
"FileLike" takes an existing file-like instance to provide the streaming
interface.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _FILE_WRAPPED_METHODS = ( "seek",
                              "tell"
                            )

    def __init__(self, timeout_retries = 5):
        """
Constructor __init__(FileLike)

:param timeout_retries: Retries before timing out

:since: v1.0.0
        """

        Abstract.__init__(self, timeout_retries)
        FileLikeWrapperMixin.__init__(self)

        self._size = None
        """
File-like resource size
        """

        self.io_chunk_size = int(Settings.get("global_io_chunk_size_local", 524288))

        self.supported_features['external_io_chunk_size'] = True
        self.supported_features['external_size'] = True
        self.supported_features['seeking'] = self._supports_seeking
    #

    @property
    def file(self):
        """
Returns the file-like resource to be used.

:return: (object) File-like resource
:since:  v1.0.0
        """

        return self._wrapped_resource
    #

    @file.setter
    def file(self, resource):
        """
Sets the file-like resource to be used.

:param resource: File-like resource

:since: v1.0.0
        """

        with self._lock:
            self._set_wrapped_resource(resource)
            if (hasattr(resource, "size")): self.size = resource.size
        #
    #

    @property
    def is_eof(self):
        """
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v1.0.0
        """

        with self._lock:
            if (self._wrapped_resource is None): _return = True
            elif (hasattr(self._wrapped_resource, "is_eof")): _return = self._wrapped_resource.is_eof
            else: _return = (self.size == self.tell())
        #

        return _return
    #

    @property
    def is_resource_valid(self):
        """
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        return (self._wrapped_resource is not None)
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        with self._lock:
            if (self._size is None): raise IOException("Streamer resource size is not defined")
            return self._size
        #
    #

    @size.setter
    def size(self, size):
        """
Sets the size of the resource if calculated externally.

:param size: Resource size

:since: v1.0.0
        """

        if (size is None or size > -1): self._size = size
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        with self._lock: FileLikeWrapperMixin.close(self)
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

    def read(self, n = None):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        if (n is None): n = self.io_chunk_size

        if (self._wrapped_resource is None): raise IOException("Streamer resource is invalid")
        return (self._wrapped_resource.read() if (n < 1) else self._wrapped_resource.read(n))
    #

    def _supports_seeking(self):
        """
Returns false if the resource has no defined size or does not support
seeking.

:since: v1.0.0
        """

        return (self._size is not None)
    #
#
