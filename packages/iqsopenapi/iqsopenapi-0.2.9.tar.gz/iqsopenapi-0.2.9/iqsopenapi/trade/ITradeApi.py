# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class ITradeApi(ABC):
    """交易接口"""

    def __init__(self,event_bus):
        """构造函数"""
        pass

    @abstractmethod
    def Init(self):
        """初始化"""
        pass
    
    @abstractmethod
    def SendOrder(self,symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        pass
    
    @abstractmethod
    def CancelOrder(self,order):
        """撤单"""
        pass
    
    @abstractmethod
    def GetAccount(self):
        """获取账户信息"""
        pass
    
    @abstractmethod
    def GetOrder(self,orderId):
        """获取指定id的委托"""
        pass
    
    @abstractmethod
    def GetOpenOrders(self):
        """获取打开的订单"""
        pass

    @abstractmethod
    def GetOrders(self):
        """获取当日委托"""
        pass
    
    @abstractmethod
    def GetPositions(self):
        """获取持仓"""
        pass
    
    @abstractmethod
    def GetTrades(self):
        """获取当日成交"""
        pass