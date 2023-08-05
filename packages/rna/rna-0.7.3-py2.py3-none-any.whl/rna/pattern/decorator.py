"""
Decorator base class providing the same behaviour for both

    @Decorator
    def ..

and

    @Decorator(my_option=True)
    def ..

Additionally it can be applied to methods, function, staticmethods, ... without thinking
"""
import abc
import functools
import inspect


class DecoratorMeta(abc.ABCMeta):
    """
    Meta class for creation of only one instance
    """

    def __call__(cls, *args, **kwargs):
        """
        Allow two signatures:
            1)
                @Decorator
                def fun...

                -> args = (fun,)
                -> kwargs = {}
            2)
                @Decorator(3, option=24)
                def fun...

                -> args = 3
                -> kwargs = {'option': 24}
        """
        func = None
        if args and callable(args[0]) and not args[1:] and not kwargs:
            # Signature 1
            func = args[0]
            args = args[1:]
        instance = cls.__new__(cls, *args, **kwargs)
        instance._func = func  # pylint:disable=attribute-defined-outside-init
        instance._obj = None  # pylint:disable=attribute-defined-outside-init
        instance._wrapped = None  # pylint:disable=attribute-defined-outside-init

        if instance._func is not None:
            # Signature 1
            functools.update_wrapper(instance, func)

        if isinstance(instance, cls):
            instance.__init__(*args, **kwargs)

        return instance


# pylint:disable=access-member-before-definition,attribute-defined-outside-init
class DecoratorBase(metaclass=DecoratorMeta):
    """
    Abstract decorator base class providing the same behaviour for two signatures:
        1)
            @DecoratorBase
            def fun...

            -> args = (fun,)
            -> kwargs = {}
        2)
            @DecoratorBase(3, option=24)
            def fun...

            -> args = 3
            -> kwargs = {'option': 24}

    Additionally it can be applied to methods, function, staticmethods, ... without thinking.
    Additionally functools.wraps is automatically applied to wrapped method. We recommend to
    not use it in addition.
    """

    def __call__(self, *args, **kwargs):
        if self._func is None:
            # Signature 2
            assert len(args) == 1
            assert not kwargs
            self._func = args[0]
            functools.update_wrapper(self, self._func)
            return self.wrapped
        # Signature 1
        return self.wrapped(*args, **kwargs)

    @property
    def wrapped(self):
        """
        Returns:
            wrapped function self._func
        """
        if self._wrapped is None:
            if self._obj:
                # Signature 2: _func is a method
                wrap = self._wrap_method(self._func)
                wrap = functools.partial(wrap, self._obj)
            elif "self" in inspect.Signature.from_callable(self._func).parameters:
                # Signature 1: _func is a method but _obj is None
                wrap = self._wrap_method(self._func)
            else:
                wrap = self._wrap_function(self._func)
            wrap = functools.wraps(self._func)(wrap)
            self._wrapped = wrap
        return self._wrapped

    def __get__(self, obj, obj_type=None):
        # Signature 2: self._func is a method!
        self._obj = obj
        return self

    @abc.abstractmethod
    def _wrap_function(self, func):
        """
        To implement for user

        Returns:
            callable: function
        """

    @abc.abstractmethod
    def _wrap_method(self, func):
        """
        To implement for user

        Returns:
            callable: method
        """


# pylint:disable=too-few-public-methods,invalid-name
class Decorator(DecoratorBase):
    """
    The Decorator class provides easy wrapping with only :py:meth:`_wrap` to be implemented.
    """

    __doc__ = DecoratorBase.__doc__.replace("DecoratorBase", "Decorator") + __doc__

    def _wrap_function(self, func):
        def wrap(*args, **kwargs):
            return self._wrap(None, func, *args, **kwargs)

        return wrap

    def _wrap_method(self, func):
        def wrap(this, *args, **kwargs):
            def prepended_self(*args, **kwargs):
                return func(this, *args, **kwargs)

            return self._wrap(this, prepended_self, *args, **kwargs)

        return wrap

    @abc.abstractmethod
    def _wrap(self, this, func, *args, **kwargs):
        """
        This is a generic wrapper method for both methods and classes. Special about this is that
        it needs to have.

        Args:
            this: obj if func is method then 'this' corresponds to 'self' in the wrapped method.
                if this is None, func is a function or staticmethod
            func: func is the function to be wrapped and will be passed as an explicit kwarg
                NOTE: When calling the function, do not use self as the first attribute even if
                func is a method. This is handled internally.
            *args: Arguments passed to decorated function. Can be passed to func.
            **kwargs: Kwargs passed to decorated function. Can be passed to func.

        Examples:
            >>> from rna.pattern.decorator import Decorator
            >>> # pylint:disable=too-few-public-methods,invalid-name
            >>> class add_args_multiply_kwargs(Decorator):
            ...     def __init__(self, att=None):
            ...         self.att = att
            ...
            ...     def _wrap(
            ...         self, this, func, *args, **kwargs
            ...     ):
            ...         if this is None:  # we are wrapping a function!
            ...             args = args + tuple([sum(args)])
            ...         else:  # we are wrapping a method
            ...             args = args + tuple([this.fast_sum(args)])
            ...         kwargs["res"] = func(*args, **kwargs)
            ...         assert self.att is None or self.att == 42  # we have access to decorator
            ...         return args, kwargs

            >>> class C:
            ...     def fast_sum(self, args):
            ...         return sum(args)
            ...
            ...     @add_args_multiply_kwargs
            ...     def multiply_kwargs(self, *args, **kwargs):
            ...         val = 1
            ...         for v in kwargs.values():
            ...             val *= v
            ...         return val

            >>> @add_args_multiply_kwargs
            ... def multiply_kwargs(*args, **kwargs):
            ...     val = 1
            ...     for v in kwargs.values():
            ...         val *= v
            ...     return val

            >>> C().multiply_kwargs(3, 3, 4, a=2, b=3, c=10)
            ((3, 3, 4, 10), {'a': 2, 'b': 3, 'c': 10, 'res': 60})
            >>> multiply_kwargs(3, 3, 4, a=2, b=3, c=10)
            ((3, 3, 4, 10), {'a': 2, 'b': 3, 'c': 10, 'res': 60})
        """
