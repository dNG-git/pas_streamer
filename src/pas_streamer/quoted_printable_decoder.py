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

from quopri import decodestring

from dpt_runtime.binary import Binary

from .abstract_encapsulated import AbstractEncapsulated

class QuotedPrintableDecoder(AbstractEncapsulated):
    """
Decodes a quoted-printable encoded, encapsulated streamer while being read.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    BINARY_EQUAL_SIGN = Binary.bytes("=")
    """
Binary equal sign representation used to identify encoded bytes.
    """
    _FILE_WRAPPED_METHODS = ( "close",
                              "is_url_supported",
                              "open_url",
                              "seek",
                              "set_range",
                              "tell"
                            )
    """
File IO methods implemented by an wrapped resource.
    """

    __slots__ = [ "_decoded_data" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, streamer):
        """
Constructor __init__(QuotedPrintableDecoder)

:param streamer: Encapsulated streamer instance

:since: v1.0.0
        """

        AbstractEncapsulated.__init__(self, streamer)

        self._decoded_data = None
        """
Already decoded data buffer
        """

        self.supported_features['raw_reader'] = True
    #

    def raw_read(self, _bytes = None):
        """
Reads from the current streamer session without decoding it transparently.

:param _bytes: How many bytes to read from the current position (0 means
               until EOF)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        return self._wrapped_resource.read(self, _bytes)
    #

    def read(self, n = None):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        raw_data = self.raw_read(n)

        decoded_data = (Binary.BYTES_TYPE() if (self._decoded_data is None) else self._decoded_data)

        if (raw_data is not None):
            if (raw_data[-1:] == QuotedPrintableDecoder.BINARY_EQUAL_SIGN):
                additional_raw_data = self.raw_read(3)
                if (additional_raw_data is not None): raw_data += additional_raw_data
            #

            decoded_data += decodestring(raw_data)
        #

        if (len(decoded_data) > n): self._decoded_data = decoded_data[n:]
        return decoded_data[:n]
    #
#
