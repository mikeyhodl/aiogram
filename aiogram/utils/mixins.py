import contextvars
from typing import Type, TypeVar

__all__ = ("DataMixin", "ContextInstanceMixin")


class DataMixin:
    @property
    def data(self):
        data = getattr(self, "_data", None)
        if data is None:
            data = {}
            setattr(self, "_data", data)
        return data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, item):
        return item in self.data

    def get(self, key, default=None):
        return self.data.get(key, default)


T = TypeVar("T")


class ContextInstanceMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__context_instance = contextvars.ContextVar(f"instance_{cls.__name__}")
        return cls

    @classmethod
    def get_current(cls: Type[T], no_error=True) -> T:
        if no_error:
            return cls.__context_instance.get(None)
        return cls.__context_instance.get()

    @classmethod
    def set_current(cls: Type[T], value: T) -> contextvars.Token:
        if not isinstance(value, cls):
            raise TypeError(
                f"Value should be instance of {cls.__name__!r} not {type(value).__name__!r}"
            )
        return cls.__context_instance.set(value)

    @classmethod
    def reset_current(cls: Type[T], token: contextvars.Token):
        cls.__context_instance.reset(token)
