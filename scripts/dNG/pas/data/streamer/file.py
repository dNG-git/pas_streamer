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

from os import path
import os

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dNG.pas.data.binary import Binary
from dNG.pas.data.mime_type import MimeType
from .abstract import Abstract
import dNG.data.file

class File(Abstract):
#
	"""
"File" provides a streamer for local files.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, timeout_retries = 5):
	#
		"""
Constructor __init__(File)

:param timeout_retries: Retries before timing out

:since: v0.1.00
		"""

		Abstract.__init__(self, timeout_retries)

		self.file_pathname = None
		self.resource = None
		"""
Active file resource
		"""
	#

	def close(self):
	#
		"""
Closes all related resource pointers for the active streamer session.

:return: (bool) True on success
:since: v0.1.00
		"""

		if (self.resource == None): var_return = False
		else:
		#
			var_return = self.resource.close()
			self.resource = None
		#

		return var_return
	#

	def eof_check(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return (True if (self.resource == None) else self.resource.eof_check())
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset; False on error
:since:  v0.1.00
		"""

		return (False if (self.resource == None) else self.resource.get_position())
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes; False on error
:since:  v0.1.00
		"""

		return (False if (self.file_pathname == None) else os.stat(self.file_pathname).st_size)
	#

	def read(self, var_bytes = 65536):
	#
		"""
Reads from the current streamer session.

:param bytes: How many bytes to read from the current position (0 means
              until EOF)

:return: (mixed) Data; None if EOF; False on error
:since:  v0.1.00
		"""

		if (self.resource == None): var_return = False
		elif (self.resource.eof_check()): var_return = None
		else:
		#
			if (self.stream_size > 0):
			#
				if (var_bytes > self.stream_size): var_bytes = self.stream_size
				self.stream_size -= var_bytes
			#

			var_return = (self.resource.read(var_bytes) if (var_bytes > 0) else None)
		#

		return var_return
	#

	def resource_check(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		return (False if (self.resource == None) else True)
	#

	def seek(self, offset):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -fileStreamer.seek({0:d})- (#echo(__LINE__)#)".format(offset))
		return (False if (self.resource == None) else self.resource.seek(offset))
	#

	def supports_seeking(self):
	#
		"""
Returns false if the streamer does not support seeking.

:return: (bool) True if the streamer supports seeking.
:since:  v0.1.00
		"""

		return True
	#

	def open(self, file_pathname):
	#
		"""
Opens a file session.

:param file_pathname: Path to the requested file

:return: (bool) True on success
:since:  v0.1.00
		"""

		file_pathname = Binary.str(file_pathname)
		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -fileStreamer.open({0})- (#echo(__LINE__)#)".format(file_pathname))

		if (self.resource == None):
		#
			url_ext = path.splitext(file_pathname)[1]
			mimetype_definition = MimeType.get_instance().get(url_ext[1:])

			self.resource = dNG.data.file.File(timeout_retries = self.timeout_retries)
			var_return = self.resource.open(file_pathname, True, ("r" if (mimetype_definition['type'] == "text") else "rb"))
		#
		else: var_return = False

		self.file_pathname = (file_pathname if (var_return) else None)
		return var_return
	#

	def open_url(self, url):
	#
		"""
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v0.1.00
		"""

		url_elements = urlsplit(url)

		if (url_elements.scheme == "file"): return self.open(url_elements.path)
		else: return False
	#

	def url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.00
		"""

		url_elements = urlsplit(url)
		return (os.access(url_elements.path, os.R_OK) if (url_elements.scheme == "file") else False)
	#
#

##j## EOF