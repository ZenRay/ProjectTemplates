#coding:utf8
"""
logging 的可用 formatters 
搭建的基本思路是以开发和部署两个不同阶段配置了 Formatter，以及继承自 logging 中
formatter 类的基础类，它是对其的扩展
"""

import logging
from unittest.mock import Base

from core.config import DEFUALT_LOG_SETTINGS


# 日期格式
__DATE_FMT = DEFUALT_LOG_SETTINGS.get("LOG_DATEFORMAT", "%Y-%m-%d")

__BASIC_FORMAT = "%(levelname)s:%(name)s:%(message)s"
__DEV_FORMAT = "Loger:%(name)s Module:%(module)s Func:%(funcName)s %(lineno)d:%(message)s"
__PROD_FORMAT = DEFUALT_LOG_SETTINGS.get(
    "LOG_FORMAT", "%(asctime)s [%(name)s] %(levelname)s:[%(module)s %(lineno)d] %(message)s"
)




class BaseFormater(logging.Formatter):
    def __self__(self, *, fmt_mode=None, **kwargs):
        self.format_mode = fmt_mode
        # 根据 formatter 要求的模式确定信息模版
        if fmt_mode is None:
            super().__init__(**kwargs)
        
        if fmt_mode == "easy":
            kwargs["fmt"] = __BASIC_FORMAT

        super().__init__(**kwargs)



dev_formatter = BaseFormater(datefmt="%Y-%m-%d", fmt=__DEV_FORMAT)
prod_formatter = BaseFormater(datefmt=__DATE_FMT, fmt=__PROD_FORMAT)
