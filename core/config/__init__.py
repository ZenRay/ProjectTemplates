#coding:utf8
import configparser

from os import path

from ._default import ConfigurationParser


__all__ = ["DEFUALT_LOG_SETTINGS"]
parser = configparser.ConfigParser()
parser.read(path.join(path.dirname(__file__), "./default.conf"))


# Extract default log settings
DEFUALT_LOG_SETTINGS = ConfigurationParser("LOG", parser=parser, 
    mapping={"LOG_MODULE": "str"})



del parser