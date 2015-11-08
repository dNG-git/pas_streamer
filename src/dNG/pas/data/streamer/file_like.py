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

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dNG.pas.data.settings import Settings
from dNG.pas.runtime.io_exception import IOException
from dNG.pas.vfs.file_like_wrapper_mixin import FileLikeWrapperMixin
from .abstract import Abstract

class FileLike(FileLikeWrapperMixin, Abstract):
#
	"""
"FileLike" takes an existing file-like instance to provide the streaming
interface.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.02
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_FILE_WRAPPED_METHODS = ( "seek",
	                          "tell"
	                        )

	def __init__(self, timeout_retries = 5):
	#
		"""
Constructor __init__(FileLike)

:param timeout_retries: Retries before timing out

:since: v0.1.02
		"""

		Abstract.__init__(self, timeout_retries)
		FileLikeWrapperMixin.__init__(self)

		self.size = None
		"""
File-like resource size
		"""

		self.io_chunk_size = int(Settings.get("pas_global_io_chunk_size_local", 524288))

		self.supported_features['external_size'] = True
		self.supported_features['seeking'] = self._supports_seeking
	#

	def close(self):
	#
		"""
python.org: Flush and close this stream.

:since: v0.1.02
		"""

		with self._lock:
		#
			if (self._wrapped_resource is not None):
			#
				if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.close()- (#echo(__LINE__)#)", self, context = "pas_streamer")

				FileLikeWrapperMixin.close(self)
			#
		#
	#

	def get_size(self):
	#
		"""
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v0.1.02
		"""

		with self._lock:
		#
			if (self.size is None): raise IOException("Streamer resource size is not defined")
			return self.size
		#
	#

	def is_eof(self):
	#
		"""
Checks if the resource has reached EOF.

:return: (bool) True if EOF
:since:  v0.1.02
		"""

		with self._lock:
		#
			if (self._wrapped_resource is None): _return = True
			elif (hasattr(self._wrapped_resource, "is_eof")): _return = self._wrapped_resource.is_eof()
			else: _return = (self.tell() == self.get_size())
		#

		return _return
	#

	def is_resource_valid(self):
	#
		"""
Returns true if the streamer resource is available.

:return: (bool) True on success
:since:  v0.1.02
		"""

		return (self._wrapped_resource is not None)
	#

	def is_url_supported(self, url):
	#
		"""
Returns true if the streamer is able to return data for the given URL.

:param url: URL to be streamed

:return: (bool) True if supported
:since:  v0.1.02
		"""

		url_elements = urlsplit(url)
		return (url_elements.scheme == "file-like")
	#

	def read(self, n = None):
	#
		"""
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)

:return: (bytes) Data; None if EOF
:since:  v0.1.02
		"""

		if (n is None): n = self.io_chunk_size

		if (self._wrapped_resource is None): raise IOException("Streamer resource is invalid")
		return (self._wrapped_resource.read() if (n < 1) else self._wrapped_resource.read(n))
	#

	def set_file(self, resource):
	#
		"""
Sets the file-like resource to be used.

:param resource: File-like resource

:since: v0.1.02
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_file()- (#echo(__LINE__)#)", self, context = "pas_streamer")

		with self._lock:
		#
			self._set_wrapped_resource(resource)
			if (hasattr(resource, "get_size")): self.set_size(resource.get_size())
		#
	#

	def set_size(self, size):
	#
		"""
Sets the size of the resource if calculated externally.

:param size: Resource size

:since: v0.1.02
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.set_size({1:d})- (#echo(__LINE__)#)", self, size, context = "pas_streamer")

		self.size = size
	#

	def _supports_seeking(self):
	#
		"""
Returns false if the resource has no defined size or does not support
seeking.

:since: v0.1.02
		"""

		return (self.size is not None)
	#
#

##j## EOF