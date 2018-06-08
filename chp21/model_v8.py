import abc
import collections


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validated(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validated(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):
    """a number greater than zero"""

    def validated(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):
    """a string with at least one non-space character"""

    def validated(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class EntityMeta(type):
    """元类,用于创建带有验证字段的业务实体"""

    @classmethod
    def __prepare__(cls, name, bases):                         # __prepare__方法的第一个参数是元类,随后两个参数是要构建的类的名称和基类组成的元组,
        return collections.OrderedDict()                       # 返回值必须是映射.元类构建新类时,__prepare__方法返回的映射会传给__new__方法的最
                                                               # 后一个参数,然后再传给__init__方法.

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls._field_names = []
        for key, attr, in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)
                cls._field_names.append(key)


class Entity(metaclass=EntityMeta):
    """带验证字段的业务实体"""

    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name