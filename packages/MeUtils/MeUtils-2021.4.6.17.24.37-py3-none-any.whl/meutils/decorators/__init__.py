#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : decorator_utils
# @Time         : 2020/4/30 10:46 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
"""
@wrapt.decorator
def noargs(wrapped, instance, args, kwargs):
    logger.info(f'noargs decorator')

    return wrapped(*args, **kwargs)


def withargs(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        logger.info(f'withargs decorator: {myarg1}, {myarg2}')
        return wrapped(*args, **kwargs)

    return wrapper
"""
import inspect

import wrapt
from loguru import logger


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


@wrapt.decorator
def opener(wrapped, instance, args, kwargs):
    """
    opener(yaml.load)("conf.yaml")
    opener(json.load)("conf.json")

    """
    path = args[0]
    with open(path) as f:
        return wrapped(f)


@wrapt.decorator
def args(wrapped, instance, args, kwargs):
    func_name = wrapped.__name__
    logger.debug(f'FUNC-{func_name} ARGS: {args}')
    logger.debug(f'FUNC-{func_name} KWARGS: {kwargs}')
    logger.debug(f'FUNC-{func_name} DEFINED ARGS: {inspect.getfullargspec(wrapped).args}')  # .varargs

    return wrapped(*args, **kwargs)


@wrapt.decorator
def deprecated(wrapped, instance, args, kwargs):
    func_name = wrapped.__name__
    logger.warning(f"{func_name} deprecated")
    return wrapped(*args, **kwargs)


if __name__ == '__main__':
    class A:

        def __init__(self, ):
            print('A实例化')


    @Singleton
    class B:
        def __init__(self, ):
            print('B实例化')


    for _ in range(3):
        print('\n', _)
        A()
        B()
