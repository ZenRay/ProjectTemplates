#coding:utf8
import configparser

from os import path

from ._default import ConfigurationParser


__all__ = ["DEFAULT_LOG_SETTINGS", "DEFAULT_SPARK_SETTINGS"]
parser = configparser.ConfigParser()
parser.read(path.join(path.dirname(__file__), "./default.conf"))


# Extract default log settings
DEFAULT_LOG_SETTINGS = ConfigurationParser("LOG", parser=parser, 
    mapping={"LOG_MODULE": "str"})

# Extract default spark settings
DEFAULT_SPARK_SETTINGS = ConfigurationParser("SPARK", parser=parser,
    mapping={"SPARK_MODULE": "str"})

del parser