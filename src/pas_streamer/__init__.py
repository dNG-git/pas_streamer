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

from .abstract import Abstract
from .abstract_encapsulated import AbstractEncapsulated
from .base64_decoder import Base64Decoder
from .file import File
from .file_like import FileLike
from .gzip_compressor import GzipCompressor
from .quoted_printable_decoder import QuotedPrintableDecoder
from .vfs_based import VfsBased

try:
    from .brotli_compressor import BrotliCompressor
    from .brotli_decompressor import BrotliDecompressor
except ImportError:
    from dpt_runtime.not_implemented_class import NotImplementedClass

    BrotliCompressor = NotImplementedClass
    BrotliDecompressor = NotImplementedClass
#
