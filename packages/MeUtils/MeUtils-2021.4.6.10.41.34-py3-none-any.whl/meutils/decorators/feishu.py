#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : notice
# @Time         : 2021/4/2 3:46 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def feishu_hook(title, text='', hook_url=get_zk_config('/mipush/bot')['logger']):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        body = {"title": title, "text": text}
        requests.post(hook_url, json=body).json()

        return wrapped(*args, **kwargs)

    return wrapper


def feishu_catch(more_info=True, hook_url=get_zk_config('/mipush/bot')['logger']):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            wrapped(*args, **kwargs)
        except Exception as e:
            text = traceback.format_exc() if more_info else e

            body = {"title": wrapped.__name__, "text": text}
            requests.post(hook_url, json=body).json()

        return wrapped(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    @feishu_hook('HOOK')
    def f():
        pass


    f()
