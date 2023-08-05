#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : demo
# @Time         : 2021/4/2 3:54 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 


from meutils.decorators.catch import feishu_catch

from meutils.decorators.feishu import feishu_hook

@feishu_catch()
# @feishu_hook("H")
def f():
    return 1


print(f())