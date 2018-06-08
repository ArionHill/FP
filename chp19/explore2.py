from collections import abc
import keyword


class FrozenJSON:
    # __new__是类方法, 第一个参数是类本身, 余下参数与__init__一样.
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            # 默认行为是委托给超类的__new__方法. 这里调用的是object基类的__new__方法, 把唯一的参数设为FrozenJSON.
            # 也就是说, 在FrozenJSON.__new__方法中, super().__new__(cls)表达式会调用object.__new__(FrozenJSON),
            # 而object类构建的实例其实是FrozenJSON实例, 即那个实例的__class__属性存储的是FrozenJSON类的引用.
            # 真正的构建操作由解释器调用C语言实现的object.__new__方法执行.
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    # 仅当无法使用常规的方式获取属性（即在实例、类或超类中找不到指定的属性），
    # 解释器才会调用特殊的__getattr__方法。
    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])
