# -*- coding: utf-8 -*-

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

# pylint: disable=import-error, no-name-in-module

try: from urllib.parse import urlsplit
except ImportError: from urlparse import urlsplit

from dpt_settings import Settings

from .vfs_based import VfsBased

class File(VfsBased):
    """
"File" provides a streamer for local files.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: streamer
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout_retries = 5):
        """
Constructor __init__(File)

:param timeout_retries: Retries before timing out (not used)

:since: v1.0.0
        """

        VfsBased.__init__(self, timeout_retries)

        self.io_chunk_size = int(Settings.get("global_io_chunk_size_local", 524288))
    #

    def open_url(self, url):
        """
Opens a streamer session for the given URL.

:param url: URL to be streamed

:return: (bool) True on success
:since:  v1.0.0
        """

        url_elements = urlsplit(url)
        return (VfsBased.open_url(self, url) if (url_elements.scheme == "file") else False)
    #
#
