#coding:utf8
"""
PySpark basic job template
"""


# try:
#     from core.config import DEFAULT_SPARK_SETTINGS
#     DEFAULT_SPARK_SETTINGS.parse_module("PySpark.settings")
# except ModuleNotFoundError:
#     import PySpark.settings as DEFAULT_SPARK_SETTINGS


# parser = configparser.ConfigParser()
# parser.read(path.join(path.dirname(__file__), "./spark.cfg"))

# # create a configuration file `settings.py` at libs/python
# if parser.getboolean("project", "init_config"):
#     try:
#         from PySpark import settings
#         filename = path.join(path.dirname(__file__), "./lib/python/settings.py")
#         file = open(filename, "w", encoding="utf8")
#         # write header
#         file.write(r"#coding:utf8\n\n")

#         # write settings doc
#         file.write(settings.__doc__)

#         # add configuration value
#         for property in dir(DEFAULT_SPARK_SETTINGS):
#             if property.startswith("SPARK"):
#                 file.write(property, DEFAULT_SPARK_SETTINGS.get(property))
#     finally:
#         file.close()