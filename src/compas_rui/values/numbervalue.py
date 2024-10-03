from .value import Value


class NumberValue(Value):
    def _check_bounds(self, value):
        if self.minval is not None:
            if value < self.minval:
                raise ValueError("Value must be greater than {}".format(self.minval))

        if self.maxval is not None:
            if value > self.maxval:
                raise ValueError("Value must be less than {}".format(self.maxval))

    def check(self, value):
        super().check(value)
        self._check_bounds(value)

    @property
    def minval(self):
        return self._minval

    @minval.setter
    def minval(self, value):
        self._check_type(value)
        self._minval = value

    @property
    def maxval(self):
        return self._maxval

    @maxval.setter
    def maxval(self, value):
        self._check_type(value)
        self._maxval = value


class FloatValue(NumberValue):
    def __init__(self, value=0.0, minval=None, maxval=None, options=None):
        super().__init__(value, float, options=options)
        if minval is not None:
            self._check_type(minval)
        if maxval is not None:
            self._check_type(maxval)
        self._minval = minval
        self._maxval = maxval
        self._check_bounds(value)

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "float",
            "options": self.options,
            "minval": self.minval,
            "maxval": self.maxval,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._options = data["options"]
        self._minval = data["minval"]
        self._maxval = data["maxval"]


class IntValue(NumberValue):
    def __init__(self, value=0, minval=None, maxval=None, options=None):
        super().__init__(value, int, options=options)
        if minval is not None:
            self._check_type(minval)
        if maxval is not None:
            self._check_type(maxval)
        self._minval = minval
        self._maxval = maxval
        self._check_bounds(value)

    @property
    def data(self):
        return {
            "value": self.value,
            "value_type": "int",
            "options": self.options,
            "minval": self.minval,
            "maxval": self.maxval,
        }

    @data.setter
    def data(self, data):
        self._value = data["value"]
        self._options = data["options"]
        self._minval = data["minval"]
        self._maxval = data["maxval"]
