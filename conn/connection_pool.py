import os

import pymysql

from utils.util import singleton

@singleton
class ConnectionPool: 
  def __init__(self) -> None:
    env_list = os.environ
    self._name = env_list.get('cname')
    self._passkey = env_list.get('cpass')
    self._host = env_list.get('chost')
    self._port = env_list.get('cport') 
    self._database = env_list.get('cdatabase')
    self._pool = []

  def __del__(self):
    while self._pool:
      self._pool.pop().close()

  def get_conn(self):
    if not self._pool:
      conn = pymysql.connect(
        host=self._host,
        port=self._port,
        user=self._name,
        password=self._passkey,
        database=self._database
      )
      self._pool.append(conn)
    return self._pool.pop()
    
  def close(self, conn):
    self._pool.append(conn)

connection_pool = ConnectionPool()