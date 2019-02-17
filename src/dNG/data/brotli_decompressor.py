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

from dNG.runtime.io_exception import IOException

from dNG.data.binary import Binary

class BrotliDecompressor(object):
    """
"BrotliDecompressor" creates a brotli compressed stream similar to the
"zlib.decompressobj" object.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(BrotliDecompressor)

:since: v1.0.0
        """

        self.decompressor = brotli.Decompressor()
        """
brotli decompressor instance
        """
        self._is_decompressor_process_defined = hasattr(self.decompressor, "process")
        """
True if brotli decompressor instance defines "process()" instead of
"compress()" for compression
        """
    #

    def decompress(self, data):
        """
python.org: Decompress data, returning a bytes object containing the
uncompressed data corresponding to at least part of the data in string.

:param data: Original string

:return: (bytes) Decompressed string
:since:  v1.0.0
        """

        if (self.decompressor is None): raise IOException("brotli decompressor already flushed and closed")

        return (self.decompressor.process(data)
                if (self._is_decompressor_process_defined) else
                self.decompressor.decompress(data)
               )
    #

    def flush(self, length = None):
        """
python.org: All pending input is processed, and a bytes object containing
the remaining uncompressed output is returned.

:param mode: Flush mode

:since: v1.0.0
        """

        if (self.decompressor is None): raise IOException("brotli decompressor already flushed and closed")

        _return = (self.decompressor.finish()
                   if (hasattr(self.decompressor, "finish")) else
                   Binary.BYTES_TYPE()
                  )

        self.decompressor = None

        return _return
    #
#
