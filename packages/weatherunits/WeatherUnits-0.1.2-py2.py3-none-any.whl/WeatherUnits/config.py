import logging
from configparser import ConfigParser
from pathlib import Path

from pytz import timezone


class _Config(ConfigParser):

	def __init__(self, *args, **kwargs):
		rootPath = Path(__file__).parent
		self.path = rootPath.joinpath('config.ini')
		super(_Config, self).__init__(*args, **kwargs)
		self.read()

	def read(self, *args, **kwargs):
		super().read(self.path, *args, **kwargs)

	def update(self):
		# TODO: Add change indicator
		self.read()

	def __getattr__(self, item):
		return self[item]

	@property
	def tz(self):
		try:
			return timezone(self['Location']['timezone'])
		except Exception as e:
			logging.error('Unable load timezone from config\n', e)

	@property
	def loc(self):
		return float(self['Location']['lat']), float(self['Location']['lon'])

	@property
	def lat(self):
		return float(self['Location']['lat'])

	@property
	def lon(self):
		return float(self['Location']['lon'])


config = _Config()
