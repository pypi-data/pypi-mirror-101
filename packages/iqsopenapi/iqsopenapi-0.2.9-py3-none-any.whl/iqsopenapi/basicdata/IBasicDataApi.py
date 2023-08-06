# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class IBasicDataApi(ABC):
    """基础数据接口"""

    def __init__(self):
        """构造函数"""
        pass
    
    @abstractmethod
    def GetContract(self, symbol, exchange):
        """获取合约信息"""
        pass
    
    @abstractmethod
    def GetMainContract(self, variety):
        """获取主力合约信息（期货）"""
        pass
    
    @abstractmethod
    def GetOpenTimes(self,begin,end):
        """获取开盘时间"""
        pass

