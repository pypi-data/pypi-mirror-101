<p>内容</p>
<ul>
<li>常量</li>
</ul>
<table width="553">
<tbody>
<tr>
<td width="277">
<p>名称</p>
</td>
<td width="277">
<p>说明</p>
</td>
</tr>
<tr>
<td width="277">
<p>Exchange</p>
</td>
<td width="277">
<p>交易所</p>
</td>
</tr>
<tr>
<td width="277">
<p>Direction</p>
</td>
<td width="277">
<p>买卖方向</p>
</td>
</tr>
<tr>
<td width="277">
<p>Offset</p>
</td>
<td width="277">
<p>开平标识</p>
</td>
</tr>
<tr>
<td width="277">
<p>OrderStatus</p>
</td>
<td width="277">
<p>报单状态</p>
</td>
</tr>
<tr>
<td width="277">
<p>OrderType</p>
</td>
<td width="277">
<p>报单类型</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<ul>
<li>数据结构</li>
</ul>
<table width="553">
<tbody>
<tr>
<td width="277">
<p>名称</p>
</td>
<td width="277">
<p>说明</p>
</td>
</tr>
<tr>
<td width="277">
<p>Order</p>
</td>
<td width="277">
<p>报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>Trade</p>
</td>
<td width="277">
<p>成交单</p>
</td>
</tr>
<tr>
<td width="277">
<p>Tick</p>
</td>
<td width="277">
<p>tick行情</p>
</td>
</tr>
<tr>
<td width="277">
<p>Bar</p>
</td>
<td width="277">
<p>K线行情</p>
</td>
</tr>
<tr>
<td width="277">
<p>Position</p>
</td>
<td width="277">
<p>持仓信息</p>
</td>
</tr>
<tr>
<td width="277">
<p>Account</p>
</td>
<td width="277">
<p>账户信息</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<ul>
<li>回调函数</li>
</ul>
<table width="553">
<tbody>
<tr>
<td width="277">
<p>名称</p>
</td>
<td width="277">
<p>说明</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_init(ctx)</p>
</td>
<td width="277">
<p>策略初始化回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_stop(ctx)</p>
</td>
<td width="277">
<p>策略停止时回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_tick(ctx, tick)</p>
</td>
<td width="277">
<p>tick行情回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_bar(ctx, bar)</p>
</td>
<td width="277">
<p>K线行情回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_order(ctx, order)</p>
</td>
<td width="277">
<p>报单回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_trade(ctx, trade)</p>
</td>
<td width="277">
<p>成交回调&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_cancel(ctx, order)</p>
</td>
<td width="277">
<p>撤单回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_open(ctx)</p>
</td>
<td width="277">
<p>开盘前回调</p>
</td>
</tr>
<tr>
<td width="277">
<p>def on_close(ctx)</p>
</td>
<td width="277">
<p>收盘后回调</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<ul>
<li>方法</li>
</ul>
<table width="553">
<tbody>
<tr>
<td width="277">
<p>名称</p>
</td>
<td width="277">
<p>说明</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.subscribe</p>
</td>
<td width="277">
<p>行情订阅</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.unsubscribe</p>
</td>
<td width="277">
<p>取消订阅</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_subscribelist</p>
</td>
<td width="277">
<p>获取订阅信息</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.insert_order</p>
</td>
<td width="277">
<p>发送报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.insert_smart_order</p>
</td>
<td width="277">
<p>发送智能报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.cancel_order</p>
</td>
<td width="277">
<p>发送撤单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_orders</p>
</td>
<td width="277">
<p>查询当日报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_order</p>
</td>
<td width="277">
<p>查询特定报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_open_orders</p>
</td>
<td width="277">
<p>查询已发送未完全成交报单</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_positions</p>
</td>
<td width="277">
<p>查询持仓</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_position</p>
</td>
<td width="277">
<p>查询特定合约持仓</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_account</p>
</td>
<td width="277">
<p>查询账户信息</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_contract</p>
</td>
<td width="277">
<p>查询合约信息</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_domain_contract</p>
</td>
<td width="277">
<p>查询品种主力合约</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_last_ticks</p>
</td>
<td width="277">
<p>获取最近几笔tick数据</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_last_bars</p>
</td>
<td width="277">
<p>获取最近几笔bar数据</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_history_bars</p>
</td>
<td width="277">
<p>获取历史k线数据</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_strategy_id</p>
</td>
<td width="277">
<p>获取策略编号</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.get_datetime</p>
</td>
<td width="277">
<p>获取当前日期和时间</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.run_by_time</p>
</td>
<td width="277">
<p>定时启动函数</p>
</td>
</tr>
<tr>
<td width="277">
<p>ctx.insert_func_at_time</p>
</td>
<td width="277">
<p>插入定时执行的函数</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<h1>常量</h1>
<p>Exchange(交易所)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>值</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>Exchange.SHFE</p>
</td>
<td width="184">
<p>&ldquo;SHFE&rdquo;</p>
</td>
<td width="184">
<p>上海期货交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>Exchange.CFFEX</p>
</td>
<td width="184">
<p>&ldquo;CFFEX&rdquo;</p>
</td>
<td width="184">
<p>中国金融交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>Exchange.DCE</p>
</td>
<td width="184">
<p>&ldquo;DCE&rdquo;</p>
</td>
<td width="184">
<p>大连期货交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>Exchange.ZCE</p>
</td>
<td width="184">
<p>&ldquo;CZCE&rdquo;</p>
</td>
<td width="184">
<p>郑州期货交易所</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>OrderSide(买卖方向/持仓方向)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>&nbsp;</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderSide.Buy</p>
</td>
<td width="184">
<p>&nbsp;</p>
</td>
<td width="184">
<p>买入</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderSide.Sell</p>
</td>
<td width="184">
<p>&nbsp;</p>
</td>
<td width="184">
<p>卖出</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>PosSide(买卖方向/持仓方向)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>值</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>PosSide.Net</p>
</td>
<td width="184">
<p>0</p>
</td>
<td width="184">
<p>净（股票）</p>
</td>
</tr>
<tr>
<td width="184">
<p>PosSide.Long</p>
</td>
<td width="184">
<p>1</p>
</td>
<td width="184">
<p>多</p>
</td>
</tr>
<tr>
<td width="184">
<p>PosSide.Short</p>
</td>
<td width="184">
<p>2</p>
</td>
<td width="184">
<p>空</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Offset(开平标识)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>值</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>Offset.Open</p>
</td>
<td width="184">
<p>0</p>
</td>
<td width="184">
<p>开仓</p>
</td>
</tr>
<tr>
<td width="184">
<p>Offset.Close</p>
</td>
<td width="184">
<p>1</p>
</td>
<td width="184">
<p>平仓</p>
</td>
</tr>
<tr>
<td width="184">
<p>Offset.CloseToday</p>
</td>
<td width="184">
<p>2</p>
</td>
<td width="184">
<p>平今</p>
</td>
</tr>
<tr>
<td width="184">
<p>Offset.CloseYesterday</p>
</td>
<td width="184">
<p>3</p>
</td>
<td width="184">
<p>平昨</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>OrderStatus(报单状态)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>值</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus. UnKnow</p>
</td>
<td width="184">
<p>-1</p>
</td>
<td width="184">
<p>未知</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.NotSent</p>
</td>
<td width="184">
<p>0</p>
</td>
<td width="184">
<p>未发</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.Sended</p>
</td>
<td width="184">
<p>1</p>
</td>
<td width="184">
<p>已发</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.Accepted</p>
</td>
<td width="184">
<p>2</p>
</td>
<td width="184">
<p>已报</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.PartiallyFilled</p>
</td>
<td width="184">
<p>3</p>
</td>
<td width="184">
<p>部分成交</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.Cancelled</p>
</td>
<td width="184">
<p>4</p>
</td>
<td width="184">
<p>已撤</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.Filled</p>
</td>
<td width="184">
<p>5</p>
</td>
<td width="184">
<p>全部成交</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.Rejected</p>
</td>
<td width="184">
<p>6</p>
</td>
<td width="184">
<p>已拒绝</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderStatus.PendingCancel</p>
</td>
<td width="184">
<p>7</p>
</td>
<td width="184">
<p>待撤</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>OrderType(委托类型)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>符号</p>
</td>
<td width="184">
<p>值</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderType.LMT</p>
</td>
<td width="184">
<p>0</p>
</td>
<td width="184">
<p>限价</p>
</td>
</tr>
<tr>
<td width="184">
<p>OrderType.MKT</p>
</td>
<td width="184">
<p>1</p>
</td>
<td width="184">
<p>市价</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h1>数据结构</h1>
<p>Order(报单)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>order_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>订单ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>strategy_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>策略ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>account_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>账户ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>Exchange</p>
</td>
<td width="184">
<p>交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>order_time</p>
</td>
<td width="184">
<p>datetime</p>
</td>
<td width="184">
<p>下单时间</p>
</td>
</tr>
<tr>
<td width="184">
<p>order_type</p>
</td>
<td width="184">
<p>OrderType</p>
</td>
<td width="184">
<p>委托类型</p>
</td>
</tr>
<tr>
<td width="184">
<p>status</p>
</td>
<td width="184">
<p>OrderStatus</p>
</td>
<td width="184">
<p>报单状态</p>
</td>
</tr>
<tr>
<td width="184">
<p>offset</p>
</td>
<td width="184">
<p>Offset</p>
</td>
<td width="184">
<p>开平标识</p>
</td>
</tr>
<tr>
<td width="184">
<p>side</p>
</td>
<td width="184">
<p>OrderSide</p>
</td>
<td width="184">
<p>买卖方向</p>
</td>
</tr>
<tr>
<td width="184">
<p>price</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>委托价格</p>
</td>
</tr>
<tr>
<td width="184">
<p>quantity</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>委托数量</p>
</td>
</tr>
<tr>
<td width="184">
<p>filled</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>成交数量</p>
</td>
</tr>
<tr>
<td width="184">
<p>note</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>备注，失败时包含失败信息</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Trade(成交回报)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>trade_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>成交ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>order_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>报单ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>account_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>账户ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>strategy_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>策略ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>Exchange</p>
</td>
<td width="184">
<p>交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>filled_time</p>
</td>
<td width="184">
<p>datetime</p>
</td>
<td width="184">
<p>成交时间</p>
</td>
</tr>
<tr>
<td width="184">
<p>offset</p>
</td>
<td width="184">
<p>Offset</p>
</td>
<td width="184">
<p>开平标识</p>
</td>
</tr>
<tr>
<td width="184">
<p>side</p>
</td>
<td width="184">
<p>OrderSide</p>
</td>
<td width="184">
<p>买卖方向</p>
</td>
</tr>
<tr>
<td width="184">
<p>price</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>成交价格</p>
</td>
</tr>
<tr>
<td width="184">
<p>quantity</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>成交数量</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Tick(tick行情)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>local_time</p>
</td>
<td width="184">
<p>datetime.datetime</p>
</td>
<td width="184">
<p>时间</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>交易所代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>last</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最新价</p>
</td>
</tr>
<tr>
<td width="184">
<p>open</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>开盘价</p>
</td>
</tr>
<tr>
<td width="184">
<p>high</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最高价</p>
</td>
</tr>
<tr>
<td width="184">
<p>low</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最低价</p>
</td>
</tr>
<tr>
<td width="184">
<p>pre_close</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>收盘价</p>
</td>
</tr>
<tr>
<td width="184">
<p>volume</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>成交量</p>
</td>
</tr>
<tr>
<td width="184">
<p>turnover</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>成交金额</p>
</td>
</tr>
<tr>
<td width="184">
<p>open_interest</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>持仓量</p>
</td>
</tr>
<tr>
<td width="184">
<p>settlement</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>结算价</p>
</td>
</tr>
<tr>
<td width="184">
<p>upper_limit</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>涨停价</p>
</td>
</tr>
<tr>
<td width="184">
<p>lower_limit</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>跌停价</p>
</td>
</tr>
<tr>
<td width="184">
<p>bids</p>
</td>
<td width="184">
<p>list</p>
</td>
<td width="184">
<p>买N档</p>
</td>
</tr>
<tr>
<td width="184">
<p>asks</p>
</td>
<td width="184">
<p>list</p>
</td>
<td width="184">
<p>卖N档</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>bids与asks</p>
<p>[(float,int)...]</p>
<p>[(价格,挂单数量)...]</p>
<p>&nbsp;</p>
<p>Bar(bar行情)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>local_time</p>
</td>
<td width="184">
<p>datetime.datetime</p>
</td>
<td width="184">
<p>时间</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>交易所代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>open</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>开盘价</p>
</td>
</tr>
<tr>
<td width="184">
<p>high</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最高价</p>
</td>
</tr>
<tr>
<td width="184">
<p>low</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最低价</p>
</td>
</tr>
<tr>
<td width="184">
<p>close</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>收盘价</p>
</td>
</tr>
<tr>
<td width="184">
<p>volume</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>成交量</p>
</td>
</tr>
<tr>
<td width="184">
<p>open_interest</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>持仓量</p>
</td>
</tr>
<tr>
<td width="184">
<p>turnover</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>成交金额</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Position(持仓信息)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>account_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>账号ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>strategy_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>策略ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>交易所代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>side</p>
</td>
<td width="184">
<p>PosSide</p>
</td>
<td width="184">
<p>持仓方向</p>
</td>
</tr>
<tr>
<td width="184">
<p>quantity</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>总持仓量</p>
</td>
</tr>
<tr>
<td width="184">
<p>today_qty</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>今仓数量</p>
</td>
</tr>
<tr>
<td width="184">
<p>frozen</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>总冻结量</p>
</td>
</tr>
<tr>
<td width="184">
<p>today_avl</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>今仓可用</p>
</td>
</tr>
<tr>
<td width="184">
<p>profit</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>持仓盈利</p>
</td>
</tr>
<tr>
<td width="184">
<p>cost</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>持仓成本</p>
</td>
</tr>
<tr>
<td width="184">
<p>margin</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>保证金</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Account(账户信息)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>account_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>账户ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>strategy_id</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>策略ID</p>
</td>
</tr>
<tr>
<td width="184">
<p>total_value</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>总资产</p>
</td>
</tr>
<tr>
<td width="184">
<p>available</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>可用资金</p>
</td>
</tr>
<tr>
<td width="184">
<p>frozen_cash</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>冻结资金</p>
</td>
</tr>
<tr>
<td width="184">
<p>margin</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>保证金</p>
</td>
</tr>
<tr>
<td width="184">
<p>market_value</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>市值</p>
</td>
</tr>
<tr>
<td width="184">
<p>margin</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>保证金</p>
</td>
</tr>
<tr>
<td width="184">
<p>begin_balance</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>期初权益</p>
</td>
</tr>
<tr>
<td width="184">
<p>withdraw</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>可提资金</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>Contract(合约信息)</p>
<table width="553">
<tbody>
<tr>
<td width="184">
<p>字段</p>
</td>
<td width="184">
<p>类型</p>
</td>
<td width="184">
<p>说明</p>
</td>
</tr>
<tr>
<td width="184">
<p>symbol</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>合约代码</p>
</td>
</tr>
<tr>
<td width="184">
<p>name</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>名称</p>
</td>
</tr>
<tr>
<td width="184">
<p>exchange</p>
</td>
<td width="184">
<p>str</p>
</td>
<td width="184">
<p>交易所</p>
</td>
</tr>
<tr>
<td width="184">
<p>lots</p>
</td>
<td width="184">
<p>int</p>
</td>
<td width="184">
<p>合约乘数</p>
</td>
</tr>
<tr>
<td width="184">
<p>step</p>
</td>
<td width="184">
<p>float</p>
</td>
<td width="184">
<p>最小价差</p>
</td>
</tr>
<tr>
<td width="184">
<p>expire_date</p>
</td>
<td width="184">
<p>datetime.datetime</p>
</td>
<td width="184">
<p>到期日</p>
</td>
</tr>
<tr>
<td width="184">
<p>list_date</p>
</td>
<td width="184">
<p>datetime.datetime</p>
</td>
<td width="184">
<p>上市日</p>
</td>
</tr>
<tr>
<td width="184">
<p>trade_times</p>
</td>
<td width="184">
<p>[]</p>
</td>
<td width="184">
<p>交易时间</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p>trade_times</p>
<p>[(datetime.time,datetime.time)...]</p>
<p>[(开始时间,结束时间)...]</p>
<h1>回调函数</h1>
<p>on_init(ctx)</p>
<p>功能：策略运行前调用</p>
<p>输入：ctx</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_stop(ctx)</p>
<p>功能：策略停止时调用</p>
<p>输入：ctx</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_tick(ctx, tick)</p>
<p>功能：接收到tick行情时调用</p>
<p>输入：ctx，Tick对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_bar(ctx, bar)</p>
<p>功能：接收到K线行情时调用</p>
<p>输入：ctx，Bar对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_order(ctx, order)</p>
<p>功能：在报单时调用</p>
<p>输入：ctx，Order对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_trade(ctx, trade)</p>
<p>功能：在订单成交时调用</p>
<p>输入：ctx，Trade对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_cancel(ctx, order)</p>
<p>功能：在撤单时调用</p>
<p>输入：ctx，Order对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>on_open(ctx)</p>
<p>功能：开盘前30分钟调用</p>
<p>输入：ctx</p>
<p>&nbsp;</p>
<p>on_close(ctx)</p>
<p>功能：收盘后30分钟调用</p>
<p>输入：ctx</p>
<h1>方法</h1>
<p>ctx.subscribe(subinfo)</p>
<p>功能：订阅指定合约和周期</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; subinfo&mdash;订阅信息，包含合约代码、周期的tuple</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 例如：(&ldquo;rb2005&rdquo;,&rdquo;tick&rdquo;)，（&ldquo;j2001&rdquo;,&rdquo;5m&rdquo;）</p>
<p>&nbsp;&ldquo;tick&rdquo;表示Tick行情，&rdquo;5m&rdquo;表示5分钟Bar行情。</p>
<p>输出：Boolean</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; False&mdash;订阅失败</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; True&mdash;订阅成功</p>
<p>&nbsp;</p>
<p>ctx.unsubscribe(subinfo)</p>
<p>功能：取消订阅指定合约和周期</p>
<p>输入：同ctx.subscribe</p>
<p>输出：Boolean</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; False&mdash;取消订阅失败</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; True&mdash;取消订阅成功</p>
<p>&nbsp;</p>
<p>ctx.get_subscribelist()</p>
<p>功能：查询已订阅的行情</p>
<p>输出：subinfo的列表</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 例如：[(&ldquo;rb2005&rdquo;,&rdquo;tick&rdquo;),(&ldquo;j2001&rdquo;,&rdquo;5m&rdquo;)]、[]</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 空列表表示没有成功订阅任何行情</p>
<p>&nbsp;</p>
<p>ctx.insert_order(symbol, direction, order_type, offset, price, quantity)</p>
<p>功能：报单</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; direction&mdash;买卖方向, Direction对象</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; order_type&mdash;报单类型, OrderType对象</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; offset&mdash;开平标识, Offset对象</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; price&mdash;委托价格, float</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; quantity&mdash;委托手数, int</p>
<p>输出：Order对象</p>
<p>&nbsp;</p>
<p>ctx.insert_smart_order(symbol, quantity, price=None)</p>
<p>功能：智能报单，根据当前持仓平仓或者开仓，优先平老仓</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; quantity&mdash;委托手数，正值表示买入，负值表示卖出, int</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 当前多仓，正数：开多仓</p>
<p>当前多仓，负数：平多仓，超过头寸数量反方向开空仓</p>
<p>当前空仓，正数：平空仓，超过头寸数量反方向开多仓</p>
<p>当前空仓，负数：开空仓</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; price&mdash;委托价格，None表示市价单，否则为限价单, float</p>
<p>输出：Order对象</p>
<p>&nbsp;</p>
<p>ctx.cancel_order(order)</p>
<p>功能：撤单</p>
<p>输入：Order对象</p>
<p>输出：None</p>
<p>&nbsp;</p>
<p>ctx.get_orders()</p>
<p>功能：查询当日委托</p>
<p>输出：Order对象列表</p>
<p>&nbsp;</p>
<p>ctx.get_order(order_id)</p>
<p>功能：按照报单ID(客户端ID)获取订单信息</p>
<p>输入：str</p>
<p>输出：Order对象</p>
<p>&nbsp;</p>
<p>ctx.get_open_orders()</p>
<p>功能：查询已发送且未完全成交的订单</p>
<p>输出：Order对象列表</p>
<p>&nbsp;</p>
<p>ctx.get_positions()</p>
<p>功能：查询当前所有持仓信息</p>
<p>输出：仓位字典{symbol:position,...}</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; position&mdash;Position对象</p>
<p>&nbsp;</p>
<p>ctx.get_position(symbol)</p>
<p>功能：查询指定合约的持仓信息</p>
<p>输入：str</p>
<p>输出：Position对象</p>
<p>&nbsp;</p>
<p>ctx.get_account()</p>
<p>功能：查询账户信息</p>
<p>输出：Account对象</p>
<p>&nbsp;</p>
<p>ctx.get_contract(symbol)</p>
<p>功能：查询合约信息</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>输出：Contract对象</p>
<p>&nbsp;</p>
<p>ctx.get_dominant_contract(future)</p>
<p>功能：按照品种名查询</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; future&mdash;品种代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 例如：&rsquo;rb&rsquo;,&rsquo;m&rsquo;,&rsquo;pp&rsquo;</p>
<p>输出：合约代码, str</p>
<p>&nbsp;</p>
<p>ctx.get_last_ticks(symbol, count)</p>
<p>功能：查询最近几笔tick行情</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; count&mdash;tick行情数据数量, int</p>
<p>输出：Tick对象列表</p>
<p>&nbsp;</p>
<p>ctx.get_last_bars(symbol, period, count)</p>
<p>功能：查询最近几笔k线数据</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; period&mdash;周期信息，例如&rdquo;3m&rdquo;、&rdquo;1d&rdquo;, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &ldquo;3m&rdquo;表示3分钟行情，&rdquo;1d&rdquo;表示日线行情</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; count&mdash;K线行情数据数量, int</p>
<p>&nbsp;</p>
<p>ctx.get_history_bars(symbol, period, start_time, end_time)</p>
<p>功能：查询历史K线数据</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; symbol&mdash;合约代码, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; period&mdash;周期信息, str</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; start_time&mdash;开始时间, datetime.datetime</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; end_time&mdash;结束时间, datetime.datetime</p>
<p>输出：Bar对象列表</p>
<p>&nbsp;</p>
<p>ctx.get_strategy_id()</p>
<p>功能：获取策略编号</p>
<p>输出：str</p>
<p>&nbsp;</p>
<p>ctx.get_datetime()</p>
<p>功能：获取当前时间</p>
<p>输出：datetime.datetime</p>
<p>&nbsp;</p>
<p>ctx.run_by_time(func, run_time)</p>
<p>功能：定时运行函数</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; func&mdash;需要执行的函数, python function</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; run_time&mdash;每日定时, datetime.time</p>
<p>&nbsp;</p>
<p>ctx.insert_func_at_time(func, run_time)</p>
<p>功能：指定时间运行函数</p>
<p>输入：</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; func&mdash;需要执行的函数, python function</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; run_time&mdash;指定时间, datetime.datetime</p>