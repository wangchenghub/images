# coding=utf-8

import time
# 悲观锁装饰器：
"""
使用说明：
    所有对想要被保护的数据的操作，必须先定义一个函数，在函数内部进行操作，
    然后再使用本装饰器，如果不构造函数的话，无法使用.
    
    0： 代表未占用， 可以执行
    1： 代表被占用， 不可执行
    2： 代表被占用， 不可执行
"""

lock = 0

def pessimistic_lock(func):
    def switch():
        global lock
        lock = 1 if lock == 0 else 2
        return lock

    def wrapper(*args, **kwargs):
        global lock
        while True:
            if switch() != 2:
                result = func(*args, **kwargs)
                lock = 0
                return result
            time.sleep(1)
    return wrapper
