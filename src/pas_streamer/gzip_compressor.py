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

from struct import pack
from zlib import compressobj, crc32, MAX_WBITS, Z_FINISH

from dpt_runtime.binary import Binary
from dpt_runtime.io_exception import IOException

class GzipCompressor(object):
    """
"GzipCompressor" creates a Gzip compressed stream similar to the
"zlib.compressobj" object.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, level = 6):
        """
Constructor __init__(GzipCompressor)

:since: v1.0.0
        """

        self.compressor = None
        """
Deflate compressor instance
        """
        self.crc32 = None
        """
CRC32 from previous run
        """
        self.header = None
        """
Gzip header
        """
        self.size = None
        """
Total size of compressed data
        """

        # Use the zlib magic +16 to generate the GZip header and trailer on flush() if supported
        try: self.compressor = compressobj(level, wbits = 16 + MAX_WBITS)
        except TypeError:
            self.compressor = compressobj(level)

            if (level == 9): deflate_flag = 2
            elif (level == 1): deflate_flag = 4
            else: deflate_flag = 0

            self.header = pack("<8s2B", Binary.bytes("\x1f\x8b" + ("\x00" if (level == 0) else "\x08") + "\x00\x00\x00\x00\x00"), deflate_flag, 255)
            self.size = 0
        #
    #

    def compress(self, string):
        """
python.org: Compress string, returning a string containing compressed data
for at least part of the data in string.

:param string: Original string

:return: (bytes) Compressed string
:since:  v1.0.0
        """

        if (self.compressor is None): raise IOException("Gzip compressor already flushed and closed")
        data = Binary.bytes(string)

        if (self.size is None): compressed_data = self.compressor.compress(data)
        else:
            self.crc32 = (crc32(data) if (self.crc32 is None) else crc32(data, self.crc32))
            self.size += len(data)

            compressed_data = (self.compressor.compress(data) if (self.header is None) else self.compressor.compress(data)[2:])
        #

        if (self.header is None): _return = compressed_data
        else:
            _return = self.header + compressed_data
            self.header = None
        #

        return _return
    #

    def flush(self, mode = Z_FINISH):
        """
python.org: All pending input is processed, and a string containing the
remaining compressed output is returned.

:param mode: Flush mode

:since: v1.0.0
        """

        if (mode != Z_FINISH): raise IOException("Gzip flush only supports Z_FINISH")
        if (self.compressor is None): raise IOException("Gzip compressor already flushed and closed")

        if (self.size is None): _return = self.compressor.flush(Z_FINISH)
        else:
            _return = (Binary.BYTES_TYPE()
                       if (self.size < 1) else
                       (self.compressor.flush(Z_FINISH)[:-4]
                        + pack("<2I", (self.crc32 & 0xffffffff), int(self.size % 4294967296))
                       )
                      )
        #

        self.compressor = None

        return _return
    #
#
