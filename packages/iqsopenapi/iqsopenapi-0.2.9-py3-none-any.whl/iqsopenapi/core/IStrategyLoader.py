# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class IStrategyLoader(ABC):
    """策略加载器"""
    @abstractmethod
    def load(self):
        """加载"""
        pass