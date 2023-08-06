# -*- coding: utf-8 -*-
import numpy as np
from iqsopenapi import *
import datetime

def on_init(ctx):
    #variables
    ctx.f1 = 5
    ctx.f2 = 0.2
    ctx.f3 = 0.2
    ctx.bet_size = 0.1
    ctx.symbol = 'rb'
    ctx.domi_contract = None
    ctx.last_domi = None

    risk = ctx.get_risk()

    fixed_hand = risk['fixed_hand']

    risk_ratio = risk['risk_ratio']

    # positions = ctx.get_positions()

    # position = ctx.get_position('rb2010.SHFE')

    # order =
    # ctx.insert_order('m2009.DCE',OrderSide.Sell,OrderType.MKT,Offset.Open,0,8)
    # order =
    # ctx.insert_order('m2009.DCE',OrderSide.Buy,OrderType.MKT,Offset.Open,0,5)

    # order = ctx.insert_smart_order('c2009.DCE', -20)

    id = ctx.get_strategy_id()

    ctx.subscribe(('cu2010.SHFE','1m'),('rr2009.DCE','1m'),('rb2010.SHFE','1m'),('sc2009.INE','1m'))

    ctx.domi_contract = ctx.get_dominant_contract(ctx.symbol)
    conInfo = ctx.get_contract(ctx.domi_contract.symbol)

    last_bars = ctx.get_last_bars(ctx.domi_contract.symbol,'1d',300)

    last_ticks = ctx.get_last_ticks(ctx.domi_contract.symbol,100)

    # account = ctx.get_account()

    # orders = ctx.get_open_orders()

    # positions = ctx.get_positions()

    # trades = ctx.get_trades()

    # order = ctx.insert_order('rb2010.SHFE',OrderSide.Buy,OrderType.MKT,Offset.Open,0,3)

    # order = ctx.insert_smart_order('rb2010.SHFE', 1, 3508)

    #order1 = ctx.cancel_order(order)

    # order2 = ctx.get_order(order.order_id)

    bars1 = ctx.get_history_bars('rb2010.SHFE','1m','20200521','20200522')

    bars2 = ctx.get_history_bars('rb2010.SHFE','1m',datetime(2020,5,21,9,10,0),datetime(2020,5,21,11,10,0))

    bars2 = ctx.get_history_bars('rb2010.SHFE','1m',date(2020,5,21),date(2020,5,22))
    
    ctx.run_by_time(run_time,datetime(2020,5,21,13,58,0),'CCC','DDDDD')

    ctx.run_by_time(run_time,time(13,50,0))

    ctx.insert_func_at_time(run_time,time(13,49,0))

    ctx.insert_func_at_time(run_time,datetime(2020,6,4,10,35,50),ctx)

    pass

def run_time(*args):
    ctx = args[0][0]
    ctx.unsubscribe(('rb2010.SHFE','TICK'))
    logger.info('unsubscribe')
    
def on_open(ctx):
    logger.info('on open raised')
    
def on_close(ctx):
    ctx.last_domi = ctx.domi_contract
    logger.info('on close raised')

def on_market_close(ctx,bar):
    logger.info('on market close bar:{0},{1},{2}'.format(bar.symbol,bar.local_time,bar.close))

def on_tick(ctx,tick):
    logger.info('tick:{0},{1},{2}'.format(tick.symbol,tick.local_time,tick.last))

def on_order(ctx,order):
    logger.info('on order:{0},{1},{2},{3}'.format(order.symbol,order.side.name,order.offset.name,order.status.name))

def on_trade(ctx,trade):
    logger.info('on trade:{0},{1},{2},{3},{4}'.format(trade.symbol,trade.side.name,trade.offset.name,trade.quantity,trade.price))
    
def on_bar(ctx,bar):
    logger.info('bar:{0},{1},{2}'.format(bar.symbol,bar.local_time,bar.close))
    
config = {
    "runtime":"DEBUG",
    "run_type":"LIVE_TRADING",
    "log":{
            'level':'INFO',
            'file' :"/home/sunliusi/logs/strategy.log",
        },
    #"ext_notify":{
    #        "type":"websocket",
    #        "address":"ws://localhost:14002/"
    #    },
    # "acct_info":{
    #     "strategy_id":"21",
    #     "account":"10030"
    # },
    "risk":{
        "fixed_hand":10,
        "risk_ratio":1.0
    },
    "acct_info":{
           "strategy_id":"1021",
           "account":"093959",
           "password":"640423",
           "comp_counter":98,
           "broker_type":152
       }
}
run_func(**globals())