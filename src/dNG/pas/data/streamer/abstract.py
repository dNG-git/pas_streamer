# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;streamer

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasStreamerVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.data.supports_mixin import SupportsMixin
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.iterator import Iterator
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.thread_lock import ThreadLock

class Abstract(Iterator, SupportsMixin):
#
	"""
The abstract streamer defines the to be implemented interface. A streamer
interface is similar to a file one.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	def __init__(self, timeout_retries = 5):
	#
		"""
Constructor __init__(Abstract)

:param timeout_retries: Retries before timing out

:since: v0.1.00
		"""

		SupportsMixin.__init__(self)

		self.io_chunk_size = 65536
		"""
IO chunk size
		"""
		self._lock = ThreadLock()
		"""
Thread safety lock
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
Retries before timing out
		"""
		self.stream_size = -1
		"""
Requested stream size
		"""
		self.timeout_retries = (5 if (timeout_retries == None) else timeout_retries)
		"""
Retries before timing out
		"""
	#

	def __del__(self):
	#
		"""
Destructor __del__(Abstract)

:since: v0.1.00
		"""

		self.close()
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v0.1.00
		"""

		with self._lock:
		#
			if (self.is_eof()):
			#
				self.close()
				raise StopIteration()
			#

			return self.read()
		#
	#

	def close(self):
	#
		"""
Closes all related resource pointers for the active streamer session.

:return: (bool) True on success
:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	def get_io_chunk_size(self):
	#
		"""
Returns the IO chunk size to be used for reading.

:return: (int) IO chunk size
:since:  v0.1.00
		"""

		return self.io_chunk_size
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def is_eof(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def is_resource_valid(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	def is_url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.00
		"""

		return False
	#

	def read(self, _bytes = 4096):
	#
		"""
Reads from the current streamer session.

:param _bytes: How many bytes to read from the current position (0 means
               until EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def seek(self, offset):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	def set_io_chunk_size(self, chunk_size):
	#
		"""
Sets the IO chunk size to be used for reading.

:param chunk_size: IO chunk size

:since: v0.1.00
		"""

		self.io_chunk_size = chunk_size
	#

	def set_range(self, range_start, range_end):
	#
		"""
Define a range to be streamed.

:param range_start: First byte of range
:param range_end: Last byte of range

:return: (bool) True if valid
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_range({1:d}, {2:d})- (#echo(__LINE__)#)", self, range_start, range_end, context = "pas_streamer")
		_return = False

		with self._lock:
		#
			if (range_start >= 0 and range_start <= range_end):
			#
				position = self.get_position()

				if (position == range_start): _return = True
				elif (self.is_supported("seeking")): _return = self.seek(range_start)
			#

			if (_return): self.stream_size = 1 + (range_end - range_start)
		#

		return _return
	#

	def open_url(self, url):
	#
		"""
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#
#

##j## EOF