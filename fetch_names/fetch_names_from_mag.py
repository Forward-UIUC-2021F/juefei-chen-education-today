import mysql.connector
import os

MAG_DB_CONFIG = {
  'user' : '<Enter DB user>',
  'password': '<Enter User password>',
  'host':'<Enter host URL>',
  'db_name': '<Enter DB name>',
  'ssl_certificate_path': '<Enter path here>'
}

def create_normalized_name_set():
  db = mysql.connector.connect(
    user=MAG_DB_CONFIG['user'],
    password=MAG_DB_CONFIG['password'],
    host=MAG_DB_CONFIG['host'],
    port=3306,
    database=MAG_DB_CONFIG['db_name'],
    ssl_ca=MAG_DB_CONFIG['ssl_certificate_path'],
    ssl_disabled=False
  )

  cursor = db.cursor()
  print('Connected!')

  query = 'select normalizedname, displayname from authors'
  cursor.execute(query)
  normalized_name_set = set()
  for (normalizedname, displayname) in cursor:
    sp = normalizedname.split()

    normalized_name_set.update([s for s in sp if(len(s) > 1)])

  print(len(normalized_name_set))
  with open('./normalized_name_set.txt', 'w+') as fp:
      fp.write('\n'.join(list(normalized_name_set)))

  db.close()

if __name__ == '__main__':
  create_normalized_name_set()