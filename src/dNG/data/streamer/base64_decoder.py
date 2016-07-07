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

from base64 import b64decode
from math import ceil

from dNG.data.binary import Binary
from dNG.runtime.io_exception import IOException

from .abstract_encapsulated import AbstractEncapsulated

class Base64Decoder(AbstractEncapsulated):
#
	"""
Decodes a base64 encoded, encapsulated streamer while being read.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, streamer):
	#
		"""
Constructor __init__(Base64Decoder)

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

		raw_data_size = ((ceil(4 * (n / 3))) if (n > 0) else self.get_size())
		raw_data = self.raw_read(raw_data_size)

		decoded_data = (Binary.BYTES_TYPE() if (self.decoded_data is None) else self.decoded_data)
		if (raw_data is not None): decoded_data += b64decode(raw_data)

		if (len(decoded_data) > n): self.decoded_data = decoded_data[n:]
		return decoded_data[:n]
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v0.2.00
		"""

		if (offset % 3 != 0): raise IOException("Resource can not be seeked to a non-boundary offset")
		return AbstractEncapsulated.seek(self, offset)
	#

	def set_range(self, range_start, range_end):
	#
		"""
Define a range to be streamed.

:param range_start: First byte of range
:param range_end: Last byte of range

:return: (bool) True if valid
:since:  v0.2.00
		"""

		if (range_start % 3 != 0): raise IOException("Resource range start at a non-boundary offset is not supported")
		if (range_end % 3 != 0): raise IOException("Resource range end at a non-boundary offset is not supported")

		return AbstractEncapsulated.set_range(range_start, range_end)
	#
#

##j## EOF