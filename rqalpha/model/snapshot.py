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

import numpy as np

from ..utils.datetime import convert_int_to_datetime


class SnapshotObject(object):
    _STOCK_FIELDS = [
        ('datetime', np.uint64),
        ('open', np.float64),
        ('high', np.float64),
        ('low', np.float64),
        ('last', np.float64),
        ('volume', np.uint32),
        ('total_turnover', np.uint64),
        ('prev_close', np.float64)
    ]

    _FUTURE_FIELDS = _STOCK_FIELDS + [('open_interest', np.uint32), ('prev_settlement', np.float64)]

    _STOCK_FIELD_NAMES = [_n for _n, _ in _STOCK_FIELDS]
    _FUTURE_FIELD_NAMES = [_n for _n, _ in _FUTURE_FIELDS]
    _STOCK_FIELD_DTYPE = np.dtype(_STOCK_FIELDS)
    _FUTURE_FIELD_DTYPE = np.dtype(_FUTURE_FIELDS)

    _NANDict = {_n: np.nan for _n in _FUTURE_FIELD_NAMES}

    def __init__(self, instrument, data, dt=None):
        self._dt = dt
        if data is None:
            self._data = self._NANDict
        else:
            self._data = data
        self._instrument = instrument

    @staticmethod
    def fields_for_(instrument):
        if instrument.type == 'Future':
            return SnapshotObject._FUTURE_FIELD_NAMES
        else:
            return SnapshotObject._STOCK_FIELD_NAMES

    @staticmethod
    def dtype_for_(instrument):
        if instrument.type == 'Future':
            return SnapshotObject._FUTURE_FIELD_DTYPE
        else:
            return SnapshotObject._STOCK_FIELD_DTYPE

    @property
    def open(self):
        return self._data["open"]

    @property
    def last(self):
        return self._data["last"]

    @property
    def low(self):
        return self._data["low"]

    @property
    def high(self):
        return self._data["high"]

    @property
    def prev_close(self):
        return self._data['prev_close']

    @property
    def volume(self):
        return self._data['volume']

    @property
    def total_turnover(self):
        return self._data['total_turnover']

    @property
    def datetime(self):
        if self._dt is not None:
            return self._dt
        if not self.isnan:
            return convert_int_to_datetime(self._data['datetime'])
        return datetime.datetime.min

    @property
    def instrument(self):
        return self._instrument

    @property
    def order_book_id(self):
        return self._instrument.order_book_id

    @property
    def prev_settlement(self):
        return self._data['prev_settlement']

    @property
    def open_interest(self):
        return self._data['open_interest']

    @property
    def isnan(self):
        return np.isnan(self._data['last'])

    def __repr__(self):
        base = [
            ('order_book_id', repr(self._instrument.order_book_id)),
            ('datetime', repr(self.datetime)),
        ]

        if self.isnan:
            base.append(('error', repr('DATA UNAVAILABLE')))
            return 'Snapshot({0})'.format(', '.join('{0}: {1}'.format(k, v) for k, v in base) + ' NaN SNAPSHOT')

        if isinstance(self._data, dict):
            # in pt
            base.extend([k, v] for k, v in self._data.items() if k != 'datetime')
        else:
            base.extend((n, self._data[n]) for n in self._data.dtype.names if n != 'datetime')
        return "Snapshot({0})".format(', '.join('{0}: {1}'.format(k, v) for k, v in base))

    def __getitem__(self, key):
        return self.__dict__[key]
