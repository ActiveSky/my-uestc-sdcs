import hashlib
import rpyc
from fastapi import HTTPException
from rpyc import Service

from logger import Logger
from store import KVStore


_HOST = '127.0.0.1'


class KVService(Service):
    def __init__(self, 
                 port,        # 当前服务实例的端口号
                 all_ports):  # 所有服务实例的端口号列表
        # 初始化当前服务实例的端口号和所有端口列表
        self.port = port
        self.all_ports = all_ports
        
        # 初始化日志记录器和键值存储
        self.logger = Logger(f'log.txt')
        self.store = KVStore(self.logger)
    
    def handle_http_request(self, operation, k, v=None):
        # 获取日志记录器和目标端口
        logger = self.logger
        target_port = self._select_rpc(k)

        # 判断操作是否在本地执行
        if self._is_local(target_port):
            # 本地操作日志记录
            logger.info(f'send operation "{operation} {k} {v}" to local')
            # 执行本地RPC请求处理
            result = self.exposed_handle_rpc_request(operation, k, v)
        else:
            # 远程操作日志记录
            logger.info(f'send operation "{operation} {k} {v}" to {target_port}')
            # 建立远程连接并执行RPC请求
            with rpyc.connect(_HOST, port=target_port) as conn:
                result = conn.root.handle_rpc_request(operation, k, v)
        
        # 处理get操作的特殊情况
        if operation == 'get':
            if result is None:
                raise HTTPException(404)
            result = eval(str(result))
        
        return result
    
    def exposed_handle_rpc_request(self, operation, k, v=None):
        # 根据操作类型分发到不同的处理函数
        if operation == 'set':
            return self.do_set(k, v)
        elif operation == 'get':
            return self.do_get(k)
        else:
            return self.do_delete(k)

    def do_set(self, k, v):
        # 记录set操作日志并执行存储
        self.logger.info(f'handle operation: set {k}, {v}')
        self.store.set(k, v) # return None
        
    def do_get(self, k):
        # 记录get操作日志并从存储中获取值
        self.logger.info(f'handle operation: get {k}')
        return self.store.get(k)
    
    def do_delete(self, k):
        # 记录delete操作日志并执行删除
        self.logger.info(f'handle operation: delete {k}')
        return self.store.delete(k)

    def _select_rpc(self, k):
        # 使用哈希函数选择目标端口
        id_ = self._hash(k) % len(self.all_ports)
        self.logger.info(f'hash id {id_}')
        return self.all_ports[id_]

    def _is_local(self, port):
        # 判断端口是否为本地端口
        return port == self.port

    def _hash(self, x):
        # 使用MD5哈希算法计算键的哈希值
        md5_machine = hashlib.md5()
        md5_machine.update(x.encode('utf-8'))
        md5_hash_string = md5_machine.hexdigest()
        return int(md5_hash_string, 16)
