# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.streamer.abstract
"""
"""n// NOTE
----------------------------------------------------------------------------
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
----------------------------------------------------------------------------
NOTE_END //n"""

from collections import Iterator

from dNG.pas.data.traced_exception import TracedException
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.instance_lock import InstanceLock
from dNG.pas.runtime.thread_lock import ThreadLock

class Abstract(Iterator):
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

	exclusive_streamers = { }
	"""
Weak references to active and exclusive streamers.
	"""
	exclusive_lock = InstanceLock()
	"""
Thread safety lock
	"""

	def __init__(self, timeout_retries = 5):
	#
		"""
Constructor __init__(Abstract)

:param timeout_retries: Retries before timing out

:since: v0.1.00
		"""

		self.lock = ThreadLock()
		"""
Thread safety lock
		"""
		self.log_handler = NamedLoader.get_singleton("dNG.pas.data.logging.LogHandler", False)
		"""
Retries before timing out
		"""
		self.stream_size = 0
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

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		return self
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (str) Response data
:since:  v0.1.00
		"""

		with self.lock:
		#
			if (self.streamer.eof_check()):
			#
				self.close()
				raise StopIteration()
			#

			return self.read()
		#
	#
	next = __next__

	def close(self):
	#
		"""
Closes all related resource pointers for the active streamer session.

:return: (bool) True on success
:since: v0.1.00
		"""

		raise TracedException("Not implemented")
	#

	def eof_check(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True on success
:since:  v0.1.00
		"""

		raise TracedException("Not implemented")
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset; False on error
:since:  v0.1.00
		"""

		return False
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes; False on error
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

:return: (mixed) Data; None if EOF; False on error
:since:  v0.1.00
		"""

		raise TracedException("Not implemented")
	#

	def resource_check(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		raise TracedException("Not implemented")
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

	def set_range(self, range_start, range_end):
	#
		"""
Define a range to be streamed.

:param range_start: First byte of range
:param range_end: Last byte of range

:return: (bool) True if valid
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Streamer.set_range({0:d}, {1:d})- (#echo(__LINE__)#)".format(range_start, range_end))

		with self.lock:
		#
			_return = (self.seek(range_start) if (range_start >= 0 and range_start <= range_end and (range_start < 1 or self.supports_seeking())) else False)
			if (_return): self.stream_size = (1 + range_end - range_start)
		#

		return _return
	#

	def supports_seeking(self):
	#
		"""
Returns false if the streamer does not support seeking.

:return: (bool) True if the streamer supports seeking.
:since:  v0.1.00
		"""

		return False
	#

	def open_url(self, url, exclusive_id = None):
	#
		"""
Opens a streamer session for the given URL.

:param url: URL to be streamed
:param exclusive_id: Closes all other streamers with them same exclusive ID.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return False
	#

	def url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.00
		"""

		return False
	#
#

##j## EOF