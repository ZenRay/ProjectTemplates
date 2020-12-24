#coding:utf8
import logging


from os import path
from logging import config, handlers

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)



class LogCore:
    """Basic Log Class"""
    def __init__( 
        self, file, formatter, root="root", initial_logger=True, when=None
        ):
        if not path.exists(file):
            raise FileNotFoundError(f"{file} doesn't exist")
        
        # 如果需要根据时间 Rotated File，设置 _timerotated 为 True，When 表示更新条件
        # 具体内容参看 TimedRotatingFileHandler 参看参数 when 
        if when is not None:
            self._timerotated = True
            self._when = when
        else:
            self._timerotated = False

        self.fhandler = self._file_handler(
            file, formatter, self._timerotated, level=logging.DEBUG
        )
        self.stream_handler = self._create_formatter(formatter)
        

        # 初始化 logger
        if initial_logger:
            self._logger = logging.getLogger(root)



    def _file_handler(self, file, formatter=None, rotate=False, **kwargs):
        """Set File Handler"""
        if not rotate:
            handler = logging.FileHandler(file, encoding="utf8", delay=True)
        else:
            if self.timerotated:
                handler = handlers.TimedRotatingFileHandler(
                    filename=file, when=self._when, delay=True, **kwargs
                )
            else:
                handler = handlers.RotatingFileHandler(
                    filename=file, backupCount=31, delay=True,
                    **kwargs
                )
        
        if formatter is not None:
            formatter = self._create_formatter(formatter)
            handler.setFormatter(formatter)

        # setup logging level
        level = kwargs.get("level", False)
        if level is not None:
            handler.setLevel(level)
        
        return handler


    def _stream_handler(self, formatter=None, **kwargs):
        """Set Stream Handler"""
        import sys
        handler = logging.StreamHandler(sys.stdout)

        if formatter is not None:
            formatter = self._create_formatter(formatter)
            handler.setFormatter(formatter)
        
        # setup level
        level = kwargs.get("level", logging.INFO)
        handler.setLevel(level)

        return handler
    

    def _create_formatter(self, format, datefmt=None, **kwargs):
        """Create Formatter"""
        if isinstance(format, str):
            formatter = logging.Formatter(fmt=format, datefmt=datefmt, **kwargs)
        elif isinstance(format, logging.Formatter):
            formatter = format
        else:
            raise TypeError("`format` must be formatted str or `logging.Formatter`"
                            f", but get {type(format)}")
        
        return formatter

    
    @classmethod
    def update_logger(logger, layer, root=None, keep=False):
        """Update Logger
        
        Set a logger to the new layer. It's cautions that `layer` must a layer
        format string, eg: 'main.core'. If current layer is a child of logger, 
        keep the parent name if keep is `True`.

        If `keep` is False, replace the logger name with `root` and `layer`
        """
        if keep and isinstance(root, str):
            if logger.name.startswith(root):
                logger = logger.getChild(layer)
            elif root in logger.name:
                logger.name = logger.name.replace(root, f"{root}.{layer}")
            else:
                logger.name = f"{logger.name}.{root}.{layer}"
            
        else:
            if root is None:
                root = ""
            
            logger.name = f"{root}.{layer}"

            return logger