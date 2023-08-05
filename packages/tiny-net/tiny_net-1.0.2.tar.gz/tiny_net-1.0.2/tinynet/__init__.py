#!/usr/bin/env python3

import urllib3
import json

class Link:

	def __init__(self, link):
		self.link = link

	def _on_request(self):
		http = urllib3.PoolManager()
		response = http.request('GET', 'http://tinynet.link/app', fields={'url': self.link})
		return json.loads(response.data.decode('utf8'))

	def show_url(self):
		s_url = self._on_request()
		return s_url