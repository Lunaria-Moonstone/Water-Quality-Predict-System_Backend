import os
import concurrent.futures
from typing import List
# import threading

from utils.util import singleton
from utils import water_quality_predict_system_pyo3_extends as pyo3

@singleton
class SampleExtractor:
  def __init__(self) -> None:
    env_list = os.environ
    self._cspath = env_list.get('cspath')
    self._espath = env_list.get('espath')
  def extract(self, file_list: List[str]):
    # base_name = os.path.join(self._cspath, name + '.tar')
    # target_path = os.path.join(self._espath)

    # We should limit the maximum number of threads to safeguard the performance of the system
    # thread = threading.Thread(target=self._extract(base_name, target_path))
    # thread.start()
    # thread.join()
    base_file_list = [os.path.join(self._cspath, file_name + '.tar') for file_name in file_list]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      futures = [executor.submit(self._extract(base_file, self._espath)) for base_file in base_file_list]
      concurrent.futures.wait(futures)
  @staticmethod
  def _extract(base_file: str, target_path: str):
    pass