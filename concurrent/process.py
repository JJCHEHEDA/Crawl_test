#-*- coding: utf8 -*-

import multiprocessing, os
from time import sleep, ctime
from multiprocessing import Queue as Queue
from multiprocessing import Pipe as Pipe


'''创建多个函数作为多个进程'''
def func1(val):
    print ("Run child process func1 at:{}".format(ctime()))
    sleep(val)
    print ("End func1 at:{}".format(ctime()))

def func2(val):
    print ("Run child process func2 at:{}".format(ctime()))
    sleep(val)
    print ("End func2 at:{}".format(ctime()))


def main1():
    print ("Parent process id:{}".format(os.getpid())) 
    p1 = multiprocessing.Process(target = func1, args = (2,))
    p2 = multiprocessing.Process(target = func2, args = (4,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print ("Process END!")


'''进程间的通信'''

'''用Queue'''
def worker(my_queue):
    print ("worker process:{}, at:{}".format(os.getpid(), ctime()))
    for task in ['task'+str(i) for i in range(1,4)]:
        print ("Worker put {} into the queue".format(task))
        my_queue.put(task)

def consumer(my_queue):
    print("consumer process:{}, at:{}".format(os.getpid(), ctime()))
    sleep(0.1)
    while True:
        try:
            res = my_queue.get(block=False)
            print ("Consumer get {} from queue".format(res))
        except:
            print ("Queue is empty at:{}".format(ctime()))
            break

def main2():
    q = Queue()
    process_worker = multiprocessing.Process(target=worker, args=(q,))
    process_consumer = multiprocessing.Process(target=consumer, args=(q,))
    process_worker.start()
    process_consumer.start()
    process_worker.join()
    process_consumer.join()

'''用Pipe()
管道模式，调用Pipe()返回管道的两端的connection(conn1,conn2)代表一个管道的两个端'''

def receiver(rece_conn):
    while True:
        try:
            res = rece_conn.recv()
            print ("recv:{}".format(res))
        except EOFError:
            break

def main3():
    print ("Start...")
    send_conn, recv_conn = Pipe()
    p1 = multiprocessing.Process(target=receiver, args=(recv_conn,))
    p1.start()

    for i in range(1,5):
        send_conn.send(i)
        print ("send:{}".format(i))

    send_conn.close()
    p1.join()
    print ("End...")



if __name__ == "__main__":
    main3()
