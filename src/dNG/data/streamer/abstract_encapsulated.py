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

from dNG.runtime.value_exception import ValueException

from .abstract import Abstract

class AbstractEncapsulated(Abstract):
#
	"""
The abstract streamer encapsulates another streamer for transforming it.

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
Constructor __init__(AbstractEncapsulated)

:param streamer: Encapsulated streamer instance

:since: v0.2.00
		"""

		if (not isinstance(streamer, Abstract)): raise ValueException("Given streamer is not supported")

		Abstract.__init__(self)

		self.streamer = streamer
		"""
Encapsulated streamer instance
		"""
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v0.2.00
		"""

		data = self.read()

		if (data is None):
		#
			self.close()
			raise StopIteration()
		#

		return data
	#

	def close(self):
	#
		"""
python.org: Flush and close this stream.

:since: v0.2.00
		"""

		self.streamer.close()
	#

	def get_io_chunk_size(self):
	#
		"""
Returns the IO chunk size to be used for reading.

:return: (int) IO chunk size
:since:  v0.2.00
		"""

		return self.streamer.get_io_chunk_size()
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v0.2.00
		"""

		return self.streamer.get_size()
	#

	def is_eof(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v0.2.00
		"""

		return self.streamer.is_eof()
	#

	def is_resource_valid(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.2.00
		"""

		return self.streamer.is_resource_valid()
	#

	def is_supported(self, feature):
	#
		"""
Returns true if the feature requested is supported by this instance.

:param feature: Feature name string

:return: (bool) True if supported
:since:  v0.2.01
		"""

		_return = self.streamer.is_supported(feature)
		if (not _return): _return = self.is_supported(feature)

		return _return
	#

	def is_url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.2.00
		"""

		return self.streamer.is_url_supported(url)
	#

	def open_url(self, url, exclusive_id = None):
	#
		"""
Opens a streamer session for the given URL.

:param url: URL to be streamed
:param exclusive_id: Closes all other streamers with them same exclusive ID.

:return: (bool) True on success
:since:  v0.2.00
		"""

		return self.streamer.open_url(url, exclusive_id)
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

		return self.streamer.read(n)
	#

	def seek(self, offset):
	#
		"""
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v0.2.00
		"""

		return self.streamer.seek(offset)
	#

	def set_io_chunk_size(self, chunk_size):
	#
		"""
Sets the IO chunk size to be used for reading.

:param chunk_size: IO chunk size

:since: v0.2.00
		"""

		return self.streamer.set_io_chunk_size(chunk_size)
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

		return self.streamer.set_range(range_start, range_end)
	#

	def tell(self):
	#
		"""
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v0.2.00
		"""

		return self.streamer.tell()
	#
#

##j## EOF