from flask import Blueprint, request, current_app, redirect

from utils import water_quality_predict_system_pyo3_extends as pyo3
from utils.util import md5
from conn.connection_pool import connection_pool 

USERELKEYS = ['id', 'name', 'password', 'active', 'created', 'updated']

user_route = Blueprint('user', __name__, url_prefix='/user')

@user_route.route('/', methods=['GET'])
def fetch_user():
  args = dict(request.args)

  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'SELECT * FROM `user` WHERE 1=1 '
  params = list()
  for key, val in args.items():
    if key not in USERELKEYS: continue
    sql += f'AND {key}=%s '
    params.append(val)
  try:
    cursor.execute(sql, params)
    data = cursor.fetchall()
  except Exception as e:
    current_app.logger.error(f'sql excute faild when fetch user, following error: {e.__str__()}')
    return { "ok": True, "message": "sql execute faild", "error": e.__str__() }  
  current_app.logger.info("fetch user data")
  cursor.close()
  connection_pool.close(conn)
  
  return { "ok": True, "result": data }

@user_route.route('/', methods=['POST'])
def inject_user():
  args = dict(pyo3.bytes_2_dict(request.data))
  if not (args.keys().__contains__("name") and args.keys().__contains__("password")):
    current_app.logger.error("the params not found")
    return { "ok": False, "message": "the params not found" }
  
  uuid = pyo3.generate_uuid()
  name, password = args['name'], args['password']

  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'INSERT INTO `user` (`id`, `name`, `password`) VALUE ( %s, %s, %s )'
  params = uuid, name, md5(password)
  try:
    cursor.execute(sql, params)
    conn.commit()
  except Exception as e:
    current_app.logger.error(f'sql excute faild when insert user, following error: {e.__str__()}')
    return { "ok": False, "message": "sql excute faild", "error": e.__str__() }
  current_app.logger.info(f'user(id="{uuid}") is inserted')
  cursor.close()
  connection_pool.close(conn)

  return { "ok": True, "message": "inject success" }

@user_route.route('/', methods=['DELETE'])
def delete_user():
  args = dict(request.args)
  if "id" not in args.keys():
    current_app.logger.error('required param "id" is not found')
    return { "ok": False, "message": 'required param "id" is not found' } 
  
  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'DELETE FROM `user` WHERE `id`=%s'
  params = [args.get('id')]
  try:
    cursor.execute(sql, params)
    conn.commit()
  except Exception as e:
    current_app.logger.error(f'sql excute faild when delete user, following error: {e.__str__()}')
    return { "ok": False, "message": 'sql execute faild', "error": e.__str__() }
  current_app.logger.info(f'delete user(id="{args.get("id")}")')
  cursor.close()
  connection_pool.close(conn)

  return { "ok": True }

@user_route.route('/', methods=['PUT'])
def update_user():
  args = dict(request.args)
  data = dict(pyo3.bytes_2_dict(request.data))
  if "id" not in args.keys():
    current_app.logger.error('required param "id" is not found')
    return { "ok": False, "message": 'required param "id" is not found' } 
  
  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'UPDATE `user` SET '
  sub_sql = list()
  params = list()
  for key, val in data.items():
    if key not in USERELKEYS: continue
    sub_sql.append(f'{key}=%s')
    if key == 'password': val = md5(val)
    params.append(val)
  sql += ','.join(sub_sql)
  sql += 'WHERE id=%s'
  params.append(args.get('id'))
  try:
    cursor.execute(sql, params)
    conn.commit()
  except Exception as e:
    current_app.logger.error(f'execute sql faild when update user(id="{args.get("id")}"), following error: { e.__str__() }')
    return { "ok": False, "message": "execute sql faild", "error": e.__str__() }
  current_app.logger.info(f'update user(id="{args.get("id")}")')
  cursor.close()
  connection_pool.close(conn)

  return { "ok": True }

@user_route.route('/login', methods=['POST'])
def login():
  data = dict(pyo3.bytes_2_dict(request.data))

  conn = connection_pool.get_conn()
  cursor = conn.cursor()
  sql = 'SELECT * FROM `user` WHERE `name`=%s AND `password`=%s'
  params = [ data.get("name"), md5(data.get("password")) ]
  try:
    cursor.execute(sql, params)
    data = cursor.fetchone()
  except Exception as e:
    current_app.logger.error(f'sql execute faild when signin, following error: {e.__str__()}')
    return { "ok": False, "message": "sql execute faild", "error": e.__str__() }
  current_app.logger.info('signin success')
  cursor.close()
  connection_pool.close(conn)

  return { "ok": True, "result": data }

