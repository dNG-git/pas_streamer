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

from dNG.pas.runtime.io_exception import IOException
from dNG.pas.runtime.value_exception import ValueException
from .abstract import Abstract

class AbstractEncapsulated(Abstract):
#
	"""
The abstract streamer encapsulates another streamer for transforming it.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	_ENCAPSULATED_METHODS = ( "close",
	                          "get_io_chunk_size",
	                          "get_size",
	                          "is_eof",
	                          "is_resource_valid",
	                          "is_supported",
	                          "is_url_supported",
	                          "open_url",
	                          "read",
	                          "seek",
	                          "set_io_chunk_size",
	                          "set_range",
	                          "tell"
	                        )
	"""
Methods implemented by an encapsulated streamer.
	"""

	def __init__(self, streamer):
	#
		"""
Constructor __init__(AbstractEncapsulated)

:param streamer: Encapsulated streamer instance

:since: v0.1.00
		"""

		if (not isinstance(streamer, Abstract)): raise ValueException("Given streamer is not supported")

		Abstract.__init__(self)

		self.streamer = streamer
		"""
Encapsulated streamer instance
		"""
	#

	def __getattribute__(self, name):
	#
		"""
python.org: Called unconditionally to implement attribute accesses for
instances of the class.

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v0.1.03
		"""

		if (name in ( "__class__", "streamer" )
		    or name not in self.__class__._ENCAPSULATED_METHODS
		   ): _return = object.__getattribute__(self, name)
		else:
		#
			streamer = self.streamer
			if (streamer is None): raise IOException("'{0}' not available".format(name))
			_return = getattr(streamer, name)
		#

		return _return
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (bytes) Response data
:since:  v0.1.00
		"""

		data = self.read()

		if (data is None):
		#
			self.close()
			raise StopIteration()
		#

		return data
	#
#

##j## EOF