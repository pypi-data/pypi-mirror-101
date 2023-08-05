"""This module defines the different types of properties that can be added on a node or a relationship.
For relationship properties see ./relationships
"""
import uuid
import json
from datetime import date, datetime

from neo4j.time import DateTime, Date

from pentaquark.exceptions import PentaQuarkValidationError


class Property:
    python_type = None
    graphql_type = None

    def __init__(self, /, required=False, allow_null=True, default=None, exposed=True, help_text=None, **extra_kwargs):
        """

        :param required: is field required when object is saved in the graph
        :param allow_null:
        :param default: default value or callable
        :param exposed: whether the field is exposed in the GraphQL API
        :param extra_kwargs:
        """
        self.required = required
        self.allow_null = allow_null
        self.default = default
        self.name = None
        self.instance = None
        self.exposed = exposed
        self.help_text = help_text

    def bind(self, instance, name):
        self.instance = instance
        self.name = name

    def default_value(self):
        if self.default is None:
            return None
        if callable(self.default):
            v = self.default()
        else:
            v = self.default
        return self._validate(v)

    @property
    def has_default(self):
        return self.default is not None

    def from_cypher(self, __value):
        """Value returned from Cypher, to be translated to Python type"""
        if __value is None:
            return __value
        if self.python_type:
            return self.python_type(__value)
        return __value

    def to_cypher(self, __value):
        """From Python type to Cypher type"""
        if __value is None:
            return __value
        if self.python_type:
            return self.python_type(__value)
        return __value

    def _validate(self, __value, **kwargs):
        if __value is None or self.python_type is None:
            return __value
        try:
            return self.python_type(__value)
        except ValueError as e:
            raise PentaQuarkValidationError(e)

    def get_graphql_type(self):
        return self.graphql_type

    def to_graphql(self, __value):
        return __value

    def __set__(self, instance, __value):
        cache = instance.cached_properties
        old_value = cache.get(self.name)
        kwargs = instance.initial_data
        new_value = self._validate(__value, **kwargs)
        if old_value != new_value:
            instance.is_sync = False
            cache[self.name] = new_value

    def __get__(self, instance, owner):
        """Get value from cache in instance or retrieve from db.

        :param instance: instance of calling class
        :param owner: type of calling class
        :return:
        """
        cache = instance.cached_properties
        return cache.get(self.name)


class StringProperty(Property):
    python_type = str
    graphql_type = "String"

    def _validate(self, __value, **kwargs):
        if __value is None:
            return __value
        if isinstance(__value, (float, int, str)):
            return str(__value)
        raise PentaQuarkValidationError(f"'{__value}' can not be cast to str safely. "
                                        f"Use 'str()' if you want to do it anyway")


class UUIDProperty(StringProperty):
    graphql_type = "UUID"

    def default_value(self):
        return uuid.uuid4()

    @property
    def has_default(self):
        return True

    def from_cypher(self, __value):
        if __value:
            return uuid.UUID(__value)

    def to_cypher(self, __value):
        if __value is None:
            return __value
        if isinstance(__value, uuid.UUID):
            return __value.hex
        return __value

    def _validate(self, __value, **kwargs):
        if __value is None:
            return __value
        if isinstance(__value, str):
            return uuid.UUID(__value)
        if isinstance(__value, uuid.UUID):
            return __value
        raise PentaQuarkValidationError(f"'{__value}' seems not to be valid UUID")

    def to_graphql(self, __value):
        return __value.hex


class JSONProperty(StringProperty):
    def from_cypher(self, __value):
        if __value:
            return json.loads(__value)

    def to_cypher(self, __value):
        if __value:
            return json.dumps(__value)

    def _validate(self, __value, **kwargs):
        if __value is None:
            return None
        try:
            json.dumps(__value)
        except TypeError as e:
            raise PentaQuarkValidationError(f"'{__value}' is not json serializable ({e})")
        return __value

    def to_graphql(self, __value):
        return json.dumps(__value)


class IntegerProperty(Property):
    python_type = int
    graphql_type = "Int"

    def __init__(self, min_value=None, max_value=None, step=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step


class FloatProperty(Property):
    python_type = float
    graphql_type = "Float"


class BooleanProperty(Property):
    python_type = bool
    graphql_type = "Boolean"


# TODO: manage timezones (through LocalDate / LocalDateTime types in Neo4j)
class TemporalProperty(Property):
    DEFAULT_FORMAT = ""
    python_type = date
    cypher_type = Date

    def __init__(self, fmt="", **kwargs):
        super().__init__(**kwargs)
        self.format = fmt or self.DEFAULT_FORMAT

    def get_cypher_type(self):
        return self.cypher_type

    def from_cypher(self, __value):
        if __value:
            # value is a neo4j.time.DateTime object
            return __value.to_native()

    def to_cypher(self, __value):
        dt = __value
        ret = self.get_cypher_type()(dt.year, dt.month, dt.day)
        return ret

    def _validate(self, __value, **kwargs):
        if __value is None:
            return __value
        if isinstance(__value, self.python_type):
            return __value
        if isinstance(__value, int):  # FIXME isinstance(datetime(2020, 1, 1), date) == True
            return self.python_type.fromtimestamp(__value)
        if isinstance(__value, str):
            try:
                return self.python_type.strptime(__value, self.format)
            except AttributeError:
                return datetime.strptime(__value, self.format).date()
            except ValueError as e:
                raise PentaQuarkValidationError(e)
        raise PentaQuarkValidationError(f"Invalid {self.python_type.__name__}: {__value} "
                                        f"(expected string format: {self.format})")


class DateProperty(TemporalProperty):
    DEFAULT_FORMAT = "%Y-%m-%d"
    # TODO: define a Date scalar type
    graphql_type = "String"


class DateTimeProperty(TemporalProperty):
    DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"
    python_type = datetime
    cypher_type = DateTime
    # TODO: define a DateTime scalar type
    graphql_type = "String"

    def to_cypher(self, __value):
        dt = __value
        ret = self.cypher_type(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        return ret
