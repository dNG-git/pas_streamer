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

# pylint: disable=import-error,no-name-in-module

from os import path
import os

try: from urllib.parse import unquote, urlsplit
except ImportError:
#
	from urllib import unquote
	from urlparse import urlsplit
#

from dNG.pas.data.binary import Binary
from dNG.pas.data.mime_type import MimeType
from dNG.pas.data.settings import Settings
from dNG.pas.runtime.io_exception import IOException
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
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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
		"""
Filename used by this streamer
		"""
		self.resource = None
		"""
Active file resource
		"""

		self.io_chunk_size = int(Settings.get("pas_global_io_chunk_size_local", 524288))

		self.supported_features['seeking'] = True
	#

	def close(self):
	#
		"""
Closes all related resource pointers for the active streamer session.

:return: (bool) True on success
:since: v0.1.00
		"""

		with self._lock:
		#
			if (self.resource == None): _return = False
			else:
			#
				if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.close()- (#echo(__LINE__)#)", self, context = "pas_streamer")
				_return = self.resource.close()
				self.resource = None
			#
		#

		return _return
	#

	def get_position(self):
	#
		"""
Returns the current offset.

:return: (int) Offset
:since:  v0.1.00
		"""

		with self._lock:
		#
			if (self.resource == None): raise IOException("Streamer resource is invalid")
			return self.resource.get_position()
		#
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v0.1.00
		"""

		with self._lock:
		#
			if (self.file_pathname == None): raise IOException("Streamer resource is invalid")
			return os.stat(self.file_pathname).st_size
		#
	#

	def is_eof(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v0.1.00
		"""

		with self._lock:
		#
			return (True if (self.resource == None) else self.resource.is_eof())
		#
	#

	def _is_file_access_allowed(self, file_pathname):
	#
		"""
Checks if the file access is allowed for streaming.

:param file_pathname: Path to the requested file

:return: (bool) True if allowed
:since:  v0.1.00
		"""

		_return = False

		if (Settings.is_defined("pas_streamer_file_basedir_list")):
		#
			basedir_list = Settings.get("pas_streamer_file_basedir_list")

			if (type(basedir_list) == list):
			#
				file_absolute_pathname = path.abspath(file_pathname)

				for basedir in basedir_list:
				#
					if (file_absolute_pathname.startswith(basedir)):
					#
						_return = True
						break
					#
				#

				if ((not _return) and self.log_handler != None): self.log_handler.warning("streamer.File denied access to {0}", file_pathname, context = "pas_streamer")
			#
		#
		else: _return = True

		return _return
	#

	def is_resource_valid(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.00
		"""

		with self._lock: return (self.resource != None)
	#

	def is_url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.00
		"""

		url_elements = urlsplit(url)
		return (os.access(File._unescape_path(url_elements.path[1:]), os.R_OK) if (url_elements.scheme == "file") else False)
	#

	def read(self, _bytes = None):
	#
		"""
Reads from the current streamer session.

:param bytes: How many bytes to read from the current position (0 means
              until EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.00
		"""

		if (_bytes == None): _bytes = self.io_chunk_size
		_return = None

		if (self.resource == None): raise IOException("Streamer resource is invalid")
		elif (self.stream_size != 0 and (not self.resource.is_eof())):
		# Thread safety
			with self._lock:
			#
				is_size_limited = (self.stream_size > 0)

				if (self.resource == None): raise IOException("Streamer resource is invalid")
				elif ((self.stream_size < 0 or is_size_limited) and (not self.resource.is_eof())):
				#
					if (is_size_limited):
					#
						if (_bytes > self.stream_size): _bytes = self.stream_size
						self.stream_size -= _bytes
					#

					_return = (self.resource.read(_bytes) if (_bytes > 0) else None)
				#
			#
		#

		return _return
	#

	def seek(self, offset):
	#
		"""
Seek to a given offset.

:param offset: Seek to the given offset

:return: (bool) True on success
:since:  v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.seek({1:d})- (#echo(__LINE__)#)", self, offset, context = "pas_streamer")

		with self._lock:
		#
			return (False if (self.resource == None) else self.resource.seek(offset))
		#
	#

	def _open(self, file_pathname):
	#
		"""
Opens a file session.

:param file_pathname: Path to the requested file

:return: (bool) True on success
:since:  v0.1.00
		"""

		_return = False

		file_pathname = Binary.str(file_pathname)
		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}._open({1})- (#echo(__LINE__)#)", self, file_pathname, context = "pas_streamer")

		with self._lock:
		#
			self.file_pathname = None

			if (self.resource == None):
			#
				self.resource = dNG.data.file.File(timeout_retries = self.timeout_retries)
				_return = self.resource.open(file_pathname, True, "rb")
			#

			if (_return): _return = self._is_file_access_allowed(file_pathname)

			if (_return): self.file_pathname = file_pathname
			elif (self.resource != None):
			#
				self.resource.close()
				self.resource = None
			#
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

		url_elements = urlsplit(url)

		if (url_elements.scheme == "file"): return self._open(File._unescape_path(url_elements.path[1:]))
		else: return False
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