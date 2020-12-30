#coding:utf8
"""
Module contains Spark global context that refrences the link 
[Best Practices Writing Production](https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f)
"""
import abc


class BaseContext(metaclass=abc.ABCMeta):
    """Context Abstract Class
    
    Spark context abstract class, there are three basic methods:
    1. `execute`, can execute the spark transform
    2. `init_broadcast`, initialize the broadcast variable
    3. `init_accumulator`, initialize the accumulator
    """
    @abc.abstractmethod
    def execute(self):
        ...

    @abc.abstractmethod
    def init_broadcast(self):
        ...


    @abc.abstractmethod
    def init_accumulator(self):
        ...




class JobContext(BaseContext):
    """Job Context

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def init_accumulator(self, sc=None):
        if sc is None:
            sc = self.__sc
        
        pass

    
    def init_broadcast(self, sc=None):
        if sc is None:
            sc = self.__sc
        pass

    
    def execute(self, func, *args, **kwargs):
        """Execute Spark Application"""
        func(*args, **kwargs)
