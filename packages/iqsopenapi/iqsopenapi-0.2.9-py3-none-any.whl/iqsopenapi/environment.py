from urllib.parse import urljoin

class Environment(object):

    _env = None

    def __init__(self, config):
        Environment._env = self
        self.config = GlobalConfig()
        if config is not None:
            self.config.__dict__.update(config)       

        self.market_api = None

        self.basicdata_api = None

        self.trade_api = None

        self.acct_info = None

        self.scheduler = None

        self.event_bus = None

    def get_instance():
        """
        返回已经创建的 Environment 对象
        """
        if Environment._env is None:
            raise RuntimeError(u"Environment has not been created.")
        return Environment._env

    def get_apiurl(self,relativeUrl):
        if self.config.runtime == 'DEBUG':
            return urljoin("https://dev-apigateway.inquantstudio.com/", relativeUrl)
        return urljoin("https://apigateway.inquantstudio.com/", relativeUrl)

    def get_ykapiurl(self,relativeUrl):
        if self.config.runtime == 'DEBUG':
            return urljoin("https://dev-vir.inquant.cn/", relativeUrl)
        return urljoin("https://vir.inquant.cn/", relativeUrl)

    def get_quoteaddr(self):
        if self.config.runtime == 'DEBUG':
            return "wss://dev-quotegateway.inquantstudio.com"
        return "wss://quotegateway.inquantstudio.com"
    
    def get_trademsgaddr(self):
        if self.config.runtime == 'DEBUG':
            return "wss://dev-apigateway.inquantstudio.com/msg/"
        return "wss://apigateway.inquantstudio.com/msg/"

    def get_yktrademsgaddr(self):
        if self.config.runtime == 'DEBUG':
            return "wss://dev-vir.inquant.cn/msg/"
        return "wss://vir.inquant.cn/msg/"

    def get_livetradeaddr(self):
        if self.config.runtime == 'DEBUG':
            return "https://dev-trade.inquant.cn/tradeAcc/"
        return "https://trade.inquant.cn/tradeAcc/"

class GlobalConfig(object):
    """全局配置"""

    def __init__(self):

        """运行时 DEBUG RELEASE"""
        self.runtime = "RELEASE"

        """日志文件
        {
            level = INFO,
            file = '/home/admin/logs/1.log'
        }
        """
        self.log = None

        """交易类型 BACKTEST PAPER_TRADING LIVE_TRADING  YK_PAPER_TRADING"""
        self.run_type = None

        """外部通知配置
            {
                "type":"websocket",
                "address":"ws://localhost:9090/"
            }
        """
        self.ext_notify = None

        """"账户
            模拟盘:
            {
                "strategy_id":"1021",
                "account":"2012"
            }
            pc模拟盘:
            {
                "strategy_id":"21",
                "account":"10034",
                "user_token":"Ol2OTtExAI29PCeKuEJuKg**"
            }
            实盘:
            {
                "strategy_id":"1021",
                "account":"10010101",
                "password":"pwd",
                "comp_counter":100,
                "broker_type":12
            }
        """
        self.acct_info = None