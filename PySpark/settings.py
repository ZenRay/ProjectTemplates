#coding:utf8
"""
This module contains spark configuration:
* SPARK_DEPLOY_MODE, spark deploy mode, default value is 'client'
* SPARK_MASTER, master type, default value is 'local'
* SPARK_DRIVER_MEMORY, driver memory configuration, default value is '3g'
* SPARK_EXECUTOR_MEMORY, executor memory configuration, default value is '2g'
* SPARK_EXECUTOR_CORES, executor cores numbers, defualt value is 1

More detail configuration, see link [Configuration](https://spark.apache.org/docs/latest/configuration.html)
User can customize the configuration, and suggest that obey the under rules:
* configuration name starts with 'SPARK'
"""

SPARK_DEPLOY_MODE = "client"
SPARK_MASTER = "local"
SPARK_DRIVER_MEMORY = "3g"
SPARK_EXECUTOR_MEMORY = "2g"
SPARK_EXECUTOR_CORES = 1

