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

# pylint: disable=import-error, no-name-in-module

from dNG.runtime.value_exception import ValueException
from dNG.vfs.file_like_wrapper_mixin import FileLikeWrapperMixin

from .abstract import Abstract

class AbstractEncapsulated(FileLikeWrapperMixin, Abstract):
    """
The abstract streamer encapsulates another streamer for transforming it.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    _FILE_WRAPPED_METHODS = ( "close",
                              "is_url_supported",
                              "open_url",
                              "read",
                              "seek",
                              "set_range",
                              "tell"
                            )

    def __init__(self, streamer):
        """
Constructor __init__(AbstractEncapsulated)

:param streamer: Encapsulated streamer instance

:since: v1.0.0
        """

        if (not isinstance(streamer, Abstract)): raise ValueException("Given streamer is not supported")

        Abstract.__init__(self)
        FileLikeWrapperMixin.__init__(self)

        self._set_wrapped_resource(streamer)
    #

    def __next__(self):
        """
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v1.0.0
        """

        try:
            data = self.read()

            if (data is None):
                self.close()
                raise StopIteration()
            #
        except StopIteration: raise
        except Exception as handled_exception:
            if (self._log_handler is not None): self._log_handler.debug(handled_exception, context = "pas_streamer")
            raise StopIteration()
        #

        return data
    #

    @property
    def io_chunk_size(self):
        """
Returns the IO chunk size to be used for reading.

:return: (int) IO chunk size
:since:  v1.0.0
        """

        return self._wrapped_resource.io_chunk_size
    #

    @io_chunk_size.setter
    def io_chunk_size(self, chunk_size):
        """
Sets the IO chunk size to be used for reading.

:param chunk_size: IO chunk size

:since: v1.0.0
        """

        self._wrapped_resource.io_chunk_size = chunk_size
    #

    @property
    def is_eof(self):
        """
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v1.0.0
        """

        return self._wrapped_resource.is_eof
    #

    @property
    def is_resource_valid(self):
        """
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        return self._wrapped_resource.is_resource_valid
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        return self._wrapped_resource.size
    #

    def is_supported(self, feature):
        """
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v0.2.01
        """

        _return = self._wrapped_resource.is_supported(feature)
        if (not _return): _return = self.is_supported(feature)

        return _return
    #
#
