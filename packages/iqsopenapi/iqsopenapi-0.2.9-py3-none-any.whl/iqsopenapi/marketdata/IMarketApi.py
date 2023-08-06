# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class IMarketApi(ABC):
    """行情接口"""

    def __init__(self,event_bus):
        """构造函数"""
        pass
    
    @abstractmethod
    def Init(self,strategyID):
        """初始化"""
        pass

    @abstractmethod
    def GetSubscibes(self):
        """获取订阅列表"""
        pass
    
    @abstractmethod
    def Subscribe(self,*subInfos):
        """行情订阅"""
        pass
    
    @abstractmethod
    def Unsubscribe(self,*subInfos):
        """取消订阅"""
        pass
    
    @abstractmethod
    def GetHisBar(self, symbol, exchange, barType, startTime, endTime):
        """获取历史K线数据"""
        pass
    
    @abstractmethod
    def GetLastBar(self, symbol, exchange, barType, count):
        """获取历史K线数据"""
        pass
    
    @abstractmethod
    def GetHisTick(self, symbol, exchange, startTime, endTime):
        """获取历史TICK数据"""
        pass
    
    @abstractmethod
    def GetLastTick(self, symbol, exchange, count):
        """获取历史TICK数据"""
        pass
