


import os
import psycopg2

os.environ['DATABASE_URL'] = 'postgres://tdcqtmnigcllnz:9c0c1c18391da12bd9e3e970d6a886e38d1565d7623492eefebc2e0d0116e107@ec2-54-225-76-136.compute-1.amazonaws.com:5432/d9ouc73s3504a6'
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
# result_set = cur.execute('select * from TB_TAG_RECEIVED')
cur.execute('select * from TB_TAG_RECEIVED')
lista = cur.fetchall()
print(lista[0][0])
strg = '{:%Y-%m-%d %H:%M:%S}'.format(lista[0][1])
print(strg)
print(lista[0][0])
for item in lista:
    print(item[1])


