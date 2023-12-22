import os

from utils.water_quality_predict_system_pyo3_extends import md5_process

salt = os.environ.get('salt')

def singleton(cls):
  instance = {}
  def get_instance():
    if cls not in instance:
      instance[cls] = cls()
    return instance[cls]
  return get_instance

def md5(s: str) -> str:
  return md5_process(s + salt)
