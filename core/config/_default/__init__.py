#coding:utf8
import copy
from importlib import import_module
from types import ModuleType
import warnings


from core.lib.exceptions import NotConfigException, NotSupportedException


__all__ = ["ConfigurationParser"]

class ConfigurationParser:
    def __init__(self, name, *, module=None, parser=None, mapping=None, **kwargs):
        self.name = name
        
        if not kwargs and parser is None and module is None:
            raise NotConfigException(f"Configuration Values Missing")
        
        # setup the dict configuration as attribute associate value
        for key, value in kwargs:
            setattr(self, key, value)
        
        # if parser exists, parse setting values
        if parser is not None:
            if mapping:
                self.parse_mapping(mapping, parser)
            else:
                raise NotConfigException(f"Argument `mapping` missing")
        
        # parse module configuration
        if module:
            self.parse_module(module, name=name)

        # setup the Configuration Frozen status
        self.__frozen = False


    def __getitem__(self, key):
        if key in self:
            return getattr(self, key)
        else:
            raise KeyError(f"`{key}` not in settings")

    
    def __setitem__(self, key, value):
        """Update Item Key Value"""
        if self.__frozen and key in self:
            raise AttributeError(f"Frozen Configuration can't update key '{key}'")
        
        setattr(self, key, value)
        


    def _parse_method(self, parser, method):
        """Create Method Of Parser

        Create A parser method, so that extract configuraton value
        """
        if method == "str":
            return getattr(parser, "get")
        elif method == "int":
            return getattr(parser, "getint")
        elif method == "float":
            return getattr(parser, "getfloat")
        elif method == "boolean":
            return getattr(parser, "getboolean")
        else:
            raise NotSupportedException(f"`{method}` Not Supported By `parser`")

    
    def parse_mapping(self, mapping, parser):
        """Parse Configuration Value From Parser Object
        
        If mapping is a dict, key must be a configuration key or Module path, 
        value is the `parser` method attribute, like 'str' can use `get`, 'int' 
        use `getint`. if `mapping` is a str, the value must be module path
        """
        if parser is None:
            return

        if mapping is None:
            raise NotConfigException(f"Argument `mapping` doesn't settings")

        if self.name.islower():
            warnings.warn(f"`name` property can be lowercase, but parse mapping"
                f" will be uppercase")

        if isinstance(mapping, dict):
            for key, method in mapping.items():
                value = self._parse_method(parser, method)(self.name.upper(), key)
                if "MODULE" in key.upper():
                    self.parse_module(value, self.name)
                    continue
                # add key value pair to the object attribute
                setattr(self, property, value)
        elif isinstance(mapping, str):
            self.parse_module(mapping, self.name)
        

    def parse_module(self, module, name=None):
        """Parse Configuration Value From Module

        Extract configuration value from module, besides there is a condition 
        that module property name begin with `name`. if `name` is None, use 
        Object name.
        """
        if name is None:
            name = self.name
        
        # if module is not imported, first import the module
        if not isinstance(module, ModuleType):
            module = import_module(module)
        
        for property in dir(module):
            if property.upper().startswith(name.upper()):
                value = getattr(module, property)
                
                # add key value pair to the object attribute
                setattr(self, property, value)

        

    def copy(self, deep=False):
        """Return Object Copy
        
        If `deep` is True, return a deep copy of the object
        """
        if deep:
            obj = copy.deepcopy(self)
            obj.__frozen = False
            warnings.warn("Becautions: New Object frozen status is `False`")
            return obj

        return copy.copy(self)


    def get(self, configure, default=None):
        """Get Configure Value

        Extract configure associate value, if the configure in object. Otherwise
        return the `default` value
        """
        if configure not in self:
            return default
        
        self.__getitem__(configure)



    @property
    def frozen(self):
        """Frozen Status

        It's Object mutable status/
        """
        return self.__frozen


    @frozen.deleter
    def frozen(self):
        warnings.warn(f"Can't delete the object frozen status", UserWarning)
        NotImplemented


    @frozen.getter
    def fronzen(self):
        return self.__frozen
    

    @frozen.setter
    def frozen(self, value):
        if not isinstance(value, bool):
            raise ValueError(f"Object `frozen` status is boolean, not support by {type(value)}")
        
        self.__frozen = value

    def __repr__(self) -> str:
        format = f"<[{self.name.upper()}] Configuration Object at {hex(id(self))}>"
        return format

    
    __str__ = __repr__