#!/usr/bin/env python
# -*- coding:utf-8 -*-
#函数
import threading
import time

# threading.active_count()  #返回当前线程对象Thread的个数
# threading.enumerate()  #返回当前运行的线程对象Thread(包括后台的)的list
# threading.Condition()  #返回条件变量对象的工厂函数, 主要用户线程的并发
# threading.current_thread()  #返回当前的线程对象Thread, 文档后面解释没看懂
# threading.Lock()  #返回一个新的锁对象, 是在thread模块的基础上实现的 与acquire()和release()结合使用
#
# #类
# threading.Thread  #一个表示线程控制的类, 这个类常被继承
# thraeding.Timer  #定时器,线程在一定时间后执行
# threading.ThreadError  #引发中各种线程相关异常
# threading.Thread(group = None, target = None, name = None, args = () kwars = {})
# group : 应该为None
# target : 可以传入一个函数用于run()方法调用,
# name : 线程名 默认使用"Thread-N"
# args : 元组, 表示传入target函数的参数
# kwargs : 字典, 传入target函数中关键字参数
# 属性:
# name  #线程表示, 没有任何语义
# doemon  #布尔值, 如果是守护线程为True, 不是为False, 主线程不是守护线程, 默认threading.Thread.damon = False
# 类方法:
# run()  #用以表示线程活动的方法。
# start()  #启动线程活动。
# join([time])  #等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
# isAlive(): 返回线程是否活动的。
# getName(): 返回线程名。
# setName(): 设置线程名。
def test_thread(count) :
    while count > 0 :
        print "count = %d" % count
        count = count - 1
        time.sleep(1)
def main() :
    my_thread = threading.Thread(target = test_thread, args = (10, ))
    my_thread.start()
    my_thread.join()

if __name__ == '__main__':
    main()
