from flask import Blueprint, request, current_app

from utils import water_quality_predict_system_pyo3_extends as pyo3
from conn.connection_pool import connection_pool
from utils.extractor import SampleExtractor


SAMPLEELKEYS = ['id', ]
SAMPLEPRELOADELKEYS = ['id', ]

extractor = SampleExtractor()

sample_route = Blueprint('sample', __name__, url_prefix='/sample')

@sample_route.route('/predownload/', methods=['GET'])
def fetch_predownload_sample():
  args = dict(request.args)
  
  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'SELECT * FROM `sample_preload` WHERE 1=1 '
  params = list()
  for key, val in args.items():
    if key not in SAMPLEPRELOADELKEYS: continue
    sql += f'AND {key}=%s '
    params.append(val)
  try:
    cursor.execute(sql, params)
    data = cursor.fetchall()
  except Exception as e:
    current_app.logger.error(f'sql excute faild when fetch sample preload, following error: {e.__str__() }')
    return { "ok": False, "message": "sql execute faild", "error": e.__str__()}
  current_app.logger.info("fetch sample preload")
  cursor.close()
  connection_pool.close(conn)

  return { "ok": True, "result": data }

@sample_route.route('/predownload/', methods=['POST'])
def extract_sample_from_predownload():
  '''
  extract local samples which were compressed
  '''
  extractor.extract('hello')
  return { "ok": True }

@sample_route.route('/', methods=['GET'])
def fetch_sample():
  '''
  fetch extracted samples
  '''
  args = dict(request.args)

  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'SELECT * FROM `sample` WHERE 1=1 '
  params = list()
  for key, val in args.items():
    if key not in SAMPLEELKEYS: continue
    sql += f'AND {key}=%s '
    params.append(val)
  try:
    cursor.execute(sql, params)
    data = cursor.fetchall()
  except Exception as e:
    current_app.logger.error(f'sql excute faild when fetch sample, following error: {e.__str__()}')
    return { "ok": True, "message": "sql execute faild", "error": e.__str__() }  
  current_app.logger.info("fetch sample data")
  cursor.close()
  connection_pool.close(conn)
  
  return { "ok": True, "result": data }