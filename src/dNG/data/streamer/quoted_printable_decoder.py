# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.data.binary import Binary

from .abstract_encapsulated import AbstractEncapsulated

class QuotedPrintableDecoder(AbstractEncapsulated):
#
	"""
Decodes a quoted-printable encoded, encapsulated streamer while being read.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	BINARY_EQUAL_SIGN = Binary.bytes("=")
	"""
Binary equal sign representation used to identify encoded bytes.
	"""

	def __init__(self, streamer):
	#
		"""
Constructor __init__(QuotedPrintableDecoder)

:param streamer: Encapsulated streamer instance

:since: v0.2.00
		"""

		AbstractEncapsulated.__init__(self, streamer)

		self.decoded_data = None
		"""
Already decoded data buffer
		"""

		self.supported_features['raw_reader'] = True
	#

	def raw_read(self, _bytes = None):
	#
		"""
Reads from the current streamer session without decoding it transparently.

:param _bytes: How many bytes to read from the current position (0 means
               until EOF)

:return: (bytes) Data; None if EOF
:since:  v0.2.00
		"""

		return AbstractEncapsulated.read(self, _bytes)
	#

	def read(self, n = None):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.2.00
		"""

		raw_data = self.raw_read(n)

		decoded_data = (Binary.BYTES_TYPE() if (self.decoded_data is None) else self.decoded_data)

		if (raw_data is not None):
		#
			if (raw_data[-1:] == QuotedPrintableDecoder.BINARY_EQUAL_SIGN):
			#
				additional_raw_data = self.raw_read(3)
				if (additional_raw_data is not None): raw_data += additional_raw_data
			#

			decoded_data += decodestring(raw_data)
		#

		if (len(decoded_data) > n): self.decoded_data = decoded_data[n:]
		return decoded_data[:n]
	#
#

##j## EOF