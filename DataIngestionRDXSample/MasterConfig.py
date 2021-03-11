from configparser import ConfigParser
from os import path

class MasterConfigReader(object):
	def __init__(self):
		self.config = ConfigParser()
		config_file = path.join(path.dirname(path.abspath(__file__)),"data_ingestion_config.ini")
		self.config.read(config_file)
			
	def get(self,section,key):
		return self.config.get(section,key)