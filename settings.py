import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

database_url = conf['postgresql']['database_url']