# -*- coding: utf-8 -*-
#
# Copyright 2016 Ricequant, Inc
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
from six import itervalues

from ...const import DAYS_CNT
from ...utils.repr import property_repr


class BasePortfolio:

    __repr__ = property_repr

    def __init__(self, cash, start_date, account_type):
        self._account_type = account_type
        self._yesterday_portfolio_value = cash
        self._cash = cash
        self._starting_cash = cash
        self._start_date = start_date
        self._current_date = start_date

        self._frozen_cash = 0.
        self._total_commission = 0.
        self._total_tax = 0.

        self._dividend_receivable = 0.
        self._dividend_info = {}

    @property
    def _type(self):
        return self._account_type

    @property
    def _pid(self) -> int:
        return self._account_type.value

    @property
    def daily_returns(self) -> float:
        return 0 if self._yesterday_portfolio_value == 0 else self.daily_pnl / self._yesterday_portfolio_value

    @property
    def starting_cash(self) -> float:
        return self._starting_cash

    @property
    def start_date(self) -> datetime.date:
        return self._start_date

    @property
    def frozen_cash(self) -> float:
        return self._frozen_cash

    @property
    def cash(self) -> float:
        # 可用资金
        raise NotImplementedError

    @property
    def portfolio_value(self) -> float:
        # 投资组合总值
        raise NotImplementedError

    @property
    def positions(self) -> "Position[]":
        # 持仓
        raise NotImplementedError

    @property
    def daily_pnl(self) -> float:
        # 当日盈亏
        raise NotImplementedError

    @property
    def market_value(self) -> float:
        return sum(position.market_value for position in itervalues(self.positions))

    @property
    def pnl(self) -> float:
        # 总盈亏
        return self.portfolio_value - self.starting_cash

    @property
    def total_returns(self) -> float:
        # 总收益率
        return 0 if self.starting_cash == 0 else self.pnl / self.starting_cash

    @property
    def annualized_returns(self) -> float:
        # 年化收益率
        return (1 + self.total_returns) ** (
            DAYS_CNT.DAYS_A_YEAR / float((self._current_date - self.start_date).days + 1)) - 1

    @property
    def transaction_cost(self) -> float:
        # 总费用
        return self._total_commission + self._total_tax
