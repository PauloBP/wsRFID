
import json
from flask import Flask
from flask import request

# from datetime import datetime
# from sqlalchemy import create_engine
from datetime import datetime
# from sqlalchemy import create_engine
import os
import psycopg2

os.environ['DATABASE_URL'] = 'postgres://tdcqtmnigcllnz:9c0c1c18391da12bd9e3e970d6a886e38d1565d7623492eefebc2e0d0116e107@ec2-54-225-76-136.compute-1.amazonaws.com:5432/d9ouc73s3504a6'
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# tag = 'TAG_BAG_003'
# cur.execute('INSERT INTO TB_TAG_RECEIVED(DTH_INSERTIO, TAG_VALUE) VALUES (current_timestamp,\''+tag+'\')')
# cur.execute('COMMIT')

# print(cur.execute('select * from TB_TAG_RECEIVED'))

# db_string = "postgres://postgres:admin@localhost:5432/RFIDDB"
#
# db = create_engine(db_string)

app = Flask(__name__)

@app.route('/tagsBagsList')
def calculate():
    pg = request.args.get('page')
    print ("Parametro: "+pg)
    offset = 10*(int(pg)-1)
    # result_set = db.execute('select * from public."TB_TAG_RECEIVED" order by "DTH_INSERTION" desc LIMIT 10'+' OFFSET '+str(offset))
    cur.execute('select * from TB_TAG_RECEIVED')
    result_set = cur.fetchall()
    tela = ""
    num_recs = 0

    # username = request.form['username']
    docs = []
    saida = ""
    x = ""
    # lista =db.execute('select count(*) nro from public."TB_TAG_RECEIVED"')
    # cur.execute('select count(*) nro from TB_TAG_RECEIVED')
    # lista = cur.fetchall()
    # print (lista[0][0])
    tot = len(result_set)
    # for r in lista:
    #     print (r[0])
    #     tot = r[0]

    numberOfPages = tot//10
    if(numberOfPages % 10 != 0):
        numberOfPages = numberOfPages + 1
    if (numberOfPages == 0):
        numberOfPages = 1
    start = pg*10
    for r in result_set:
        tela = tela + "<body><p>" + r[2] + "</p></body>"
        data = {}
        dt = r[1]
        id = r[0]
        strg = '{:%Y-%m-%d %H:%M:%S}'.format(dt)
        # print (r.DTH_INSERTION)
        # print (strg)
        data['ID'] = str(id)
        data['data'] = strg
        data['tag'] = r[2]
        x = json.dumps(data)
        # saida.join(x)
        if saida == "":
            saida = x
        else:
            saida = saida + "," + x
        print(x)
        json_data = docs.append(json.dumps(data))
        num_recs = num_recs + 1

    saida = '{"docs":[' + saida + '],"total":13,"limit":10,"page":'+str(tot)+',"pages":'+str(numberOfPages)+'}'

    return saida

    # if request.args.get('calculate') == 'addition':
    #     return request.args.get('number1') + request.args.get('number2')
    # else:
    #     return 'Unsupported operation'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)