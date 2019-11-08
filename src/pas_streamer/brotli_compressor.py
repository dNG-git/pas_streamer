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

import brotli

from dpt_runtime.binary import Binary
from dpt_runtime.io_exception import IOException

class BrotliCompressor(object):
    """
"BrotliCompressor" creates a brotli compressed stream similar to the
"zlib.compressobj" object.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "compressor", "_is_compressor_process_defined" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, quality = 11, **kwargs):
        """
Constructor __init__(BrotliCompressor)

:since: v1.0.0
        """

        kwargs['quality'] = quality

        self.compressor = brotli.Compressor(**kwargs)
        """
brotli compressor instance
        """
        self._is_compressor_process_defined = hasattr(self.compressor, "process")
        """
True if brotli compressor instance defines "process()" instead of
"compress()" for compression
        """
    #

    def compress(self, string):
        """
python.org: Compress string, returning a string containing compressed data
for at least part of the data in string.

:param string: Original string

:return: (bytes) Compressed string
:since:  v1.0.0
        """

        if (self.compressor is None): raise IOException("brotli compressor already flushed and closed")
        data = Binary.bytes(string)

        return (self.compressor.process(data)
                if (self._is_compressor_process_defined) else
                self.compressor.compress(data)
               )
    #

    def flush(self, mode = None):
        """
python.org: All pending input is processed, and a string containing the
remaining compressed output is returned.

:param mode: Flush mode

:since: v1.0.0
        """

        if (mode is not None): raise IOException("brotli flush does not support any modes")
        if (self.compressor is None): raise IOException("brotli compressor already flushed and closed")

        _return = self.compressor.finish()
        self.compressor = None

        return _return
    #
#
