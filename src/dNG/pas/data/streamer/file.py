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
from weakref import ref
import os

try: from urllib.parse import unquote, urlsplit
except ImportError:
#
	from urllib import unquote
	from urlparse import urlsplit
#

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

		with self.lock:
		#
			if (self.resource == None): _return = False
			else:
			#
				if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Streamer.close()- (#echo(__LINE__)#)")
				_return = self.resource.close()
				self.resource = None
			#
		#

		return _return
	#

	def eof_check(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True on success
:since:  v0.1.00
		"""

		with self.lock:
		#
			return (True if (self.resource == None) else self.resource.eof_check())
		#
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset; False on error
:since:  v0.1.00
		"""

		with self.lock:
		#
			return (False if (self.resource == None) else self.resource.get_position())
		#
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes; False on error
:since:  v0.1.00
		"""

		with self.lock:
		#
			return (False if (self.file_pathname == None) else os.stat(self.file_pathname).st_size)
		#
	#

	def read(self, _bytes = 65536):
	#
		"""
Reads from the current streamer session.

:param bytes: How many bytes to read from the current position (0 means
              until EOF)

:return: (mixed) Data; None if EOF; False on error
:since:  v0.1.00
		"""

		with self.lock:
		#
			if (self.resource == None): _return = False
			elif (self.resource.eof_check()): _return = None
			else:
			#
				if (self.stream_size > 0):
				#
					if (_bytes > self.stream_size): _bytes = self.stream_size
					self.stream_size -= _bytes
				#

				_return = (self.resource.read(_bytes) if (_bytes > 0) else None)
			#
		#

		return _return
	#

	def resource_check(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		with self.lock:
		#
			return (False if (self.resource == None) else True)
		#
	#

	def seek(self, offset):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Streamer.seek({0:d})- (#echo(__LINE__)#)".format(offset))

		with self.lock:
		#
			return (False if (self.resource == None) else self.resource.seek(offset))
		#
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

	def _open(self, file_pathname, exclusive_id):
	#
		"""
Opens a file session.

:param file_pathname: Path to the requested file
:param exclusive_id: Closes all other streamers with them same exclusive ID.

:return: (bool) True on success
:since:  v0.1.00
		"""

		file_pathname = Binary.str(file_pathname)
		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -Streamer._open({0}, +exclusive_id)- (#echo(__LINE__)#)".format(file_pathname))

		with self.lock:
		#
			if (self.resource == None):
			#
				url_ext = path.splitext(file_pathname)[1]
				mimetype_definition = MimeType.get_instance().get(url_ext[1:])

				self.resource = dNG.data.file.File(timeout_retries = self.timeout_retries)
				_return = self.resource.open(file_pathname, True, ("r" if (mimetype_definition['class'] == "text") else "rb"))

				if (_return and exclusive_id != None):
				#
					with Abstract.exclusive_lock:
					#
						if (exclusive_id in Abstract.exclusive_streamers):
						#
							streamer = Abstract.exclusive_streamers[exclusive_id]()
							if (streamer != None): streamer.close()
						#

						Abstract.exclusive_streamers[exclusive_id] = ref(self)
					#
				#
			#
			else: _return = False

			self.file_pathname = (file_pathname if (_return) else None)
		#

		return _return
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

		url_elements = urlsplit(url)

		if (url_elements.scheme == "file"): return self._open(File._unescape_path(url_elements.path[1:]), exclusive_id)
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
		return (os.access(File._unescape_path(url_elements.path), os.R_OK) if (url_elements.scheme == "file") else False)
	#

	@staticmethod
	def _unescape_path(url_elements_path):
	#
		"""
Unescapes the path.

:param url_elements_path: Escaped path from an URL

:return: (str) Unescaped path
:since:  v0.1.00
		"""

		return path.normpath(unquote(Binary.str(url_elements_path)))
	#
#

##j## EOF