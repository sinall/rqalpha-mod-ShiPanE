#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright wh1100717
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from shipane_sdk.client import Client
from rqalpha.interface import AbstractMod
from rqalpha.events import EVENT, parse_event
from rqalpha.const import ORDER_TYPE
from rqalpha.utils.logger import user_log
from rqalpha.model.account import StockAccount


class ShipaneMod(AbstractMod):
    def __init__(self):
        self._env = None
        self._mod_config = None
        self._trigger_event = None
        self._shipane_client = None
        self._expire_before = None
        self._order_id_map = {}

    def start_up(self, env, mod_config):
        self._mod_config = mod_config
        self._expire_before = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        self._trigger_event = parse_event(mod_config.trigger_event)
        self._shipane_client = Client(
            user_log,
            host=mod_config.host,
            port=mod_config.port,
            key=mod_config.key,
            client=mod_config.client
        )

        env.event_bus.add_listener(self._trigger_event, self._submit)
        env.event_bus.add_listener(EVENT.ORDER_CANCELLATION_PASS, self._cancel)

    def tear_down(self, code, exception=None):
        pass

    def _submit(self, account, data):
        if not isinstance(account, StockAccount):
            # 不是股票账户的 Order Event 忽略
            return
        if self._trigger_event == EVENT.ORDER:
            return self._submit_by_order(data)
        if self._trigger_event == EVENT.TRADE:
            return self._submit_by_trade(data)

    def _submit_by_order(self, order):
        """
        对于 响应 ORDER_CREATION_PASS 事件，已经经过了事前风控，所以比如资金不足，下单手数为0等无效订单已经排除，这里不需要额外处理。
        :param order:
        :return:
        """
        if self._is_expired(order):
            user_log.info('[实盘易] 委托已过期，忽略下单请求')
            return
        try:
            price_type = 0 if order.type == ORDER_TYPE.LIMIT else 4
            actual_order = self._shipane_client.execute(
                self._mod_config.client,
                action=order.side.name,
                symbol=order.order_book_id,
                type=order.type.name,
                priceType=price_type,
                price=order.price,
                amount=order.quantity
            )
            self._order_id_map[order.order_id] = actual_order['id']
            return actual_order
        except Exception as e:
            user_log.error("[实盘易] 下单异常：" + str(e))

    def _submit_by_trade(self, trade):
        if self._is_expired(trade):
            user_log.info('[实盘易] 委托已过期，忽略下单请求')
            return
        try:
            price_type = 0 if trade.order.type == ORDER_TYPE.LIMIT else 4
            order = trade.order
            actual_order = self._shipane_client.execute(
                self._mod_config.client,
                action=order.side.name,
                symbol=order.order_book_id,
                type=order.type.name,
                priceType=price_type,
                price=order.price,
                amount=trade.last_quantity
            )
            return actual_order
        except Exception as e:
            user_log.error("[实盘易] 下单异常：" + str(e))

    def _cancel(self, account, order):
        if not isinstance(account, StockAccount):
            # 不是股票账户的 Cancel Event 忽略
            return
        order_id = order.order_id
        try:
            if order_id in self._order_id_map:
                self._shipane_client.cancel(self._mod_config.client, self._order_id_map[order_id])
            else:
                user_log.warning('[实盘易] 未找到对应的委托编号')
        except Exception as e:
            user_log.error("[实盘易] 撤单异常：" + str(e))

    def _is_expired(self, order_or_trade):
        return order_or_trade.datetime < self._expire_before
