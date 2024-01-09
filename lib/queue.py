import redis
import time

class TimePriorityQueue:
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def is_empty(self):
        return self.__db.zcard(self.key) == 0
    
    #入队，根据当前时间戳作为score，保证按照时间顺序出队
    #避免重复入队，使用zadd的nx参数
    def enqueue(self, item):
        self.__db.zadd(self.key, {item: time.time()}, nx=True)
    
    #删除某一个元素
    def remove(self, item):
        self.__db.zrem(self.key, item)

    #获取下一个元素
    def peek(self):
        return self.__db.zrange(self.key, 0, 0, withscores=True)[0][0].decode('utf-8')

    #获取队列长度
    def qsize(self):
        return self.__db.zcard(self.key)
    
    #获取元素在队列中的位置
    def index(self, item):
        return self.__db.zrank(self.key, item)
    
    #清理某段时间之前的元素
    def clean(self, before_time):
        self.__db.zremrangebyscore(self.key, 0, before_time)
