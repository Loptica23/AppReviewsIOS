from ConfigParser import ConfigParser, NoOptionError, NoSectionError


class Configurator(object):
    def __init__(self):
        self._configparser = ConfigParser()
        self._readConfiguration()

    def _readConfiguration(self):
        if not self._configparser.read("config.conf"):
            print("Reaing from config file is not successful!")

    def _getField(self, section, field):
        try:
            result = self._configparser.get(section, field)
            return result
        except (NoOptionError, NoSectionError):
            error = "There is no config parameter with field " + field + " and section " + section + " in config.conf"
            print(error)
            return ""

    def getLoopingTime(self):
        return self._getField("gether", "looping_time")

    def getApplicationID(self):
        return self._getField("app", "appid")

    def getCountries(self):
        countries_text = self._getField("countries", "list")
        countries_text.lower()
        countries_list = countries_text.split(',')
        return countries_list
