# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.streamer.abstract_encapsulated
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

from .abstract import Abstract

class AbstractEncapsulated(Iterator):
#
	"""
The abstract streamer encapsulates another streamer for transforming it.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, streamer):
	#
		"""
Constructor __init__(AbstractEncapsulated)

:param streamer: Encapsulated streamer instance

:since: v0.1.00
		"""

		if (isinstance(streamer, Abstract)): self.streamer = streamer
		else: raise RuntimeError("Given streamer is not supported", 22)
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

		data = self.read()

		if (data == None or data == False):
		#
			self.close()
			raise StopIteration()
		#
		else: return data
	#
	next = __next__

	def close(self):
	#
		"""
Closes all related resource pointers for the active streamer session.

:return: (bool) True on success
:since: v0.1.00
		"""

		self.streamer.close()
	#

	def eof_check(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return self.streamer.eof_check()
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset; False on error
:since:  v0.1.00
		"""

		return self.streamer.get_position()
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes; False on error
:since:  v0.1.00
		"""

		return self.streamer.get_size()
	#

	def read(self, var_bytes = 4096):
	#
		"""
Reads from the current streamer session.

:param var_bytes: How many bytes to read from the current position (0 means
                  until EOF)

:return: (mixed) Data; None if EOF; False on error
:since:  v0.1.00
		"""

		return self.streamer.read(var_bytes)
	#

	def resource_check(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return self.streamer.resource_check()
	#

	def seek(self, offset):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		return self.streamer.seek(offset)
	#

	def set_range(self, range_start, range_end):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		return self.streamer.set_range(range_start, range_end)
	#

	def supports_seeking(self):
	#
		"""
Returns false if the streamer does not support seeking.

:return: (bool) True if the streamer supports seeking.
:since:  v0.1.00
		"""

		return self.streamer.supports_seeking()
	#

	def open_url(self, url):
	#
		"""
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v0.1.00
		"""

		return self.streamer.open_url(url)
	#

	def url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.00
		"""

		return self.streamer.url_supported(url)
	#
#

##j## EOF