# from SOAPpy import SOAPServer
#
# def calcula(op1,op2,operacao):
#         if operacao == '+':
#                 return op1 + op2
#         if operacao == '-':
#                 return op1 - op2
#         if operacao == '*':
#                 return op1 * op2
#         if operacao == '/':
#                 return op1 / op2
# server = SOAPServer(('localhost',8081))
# server.registerFunction(calcula)
# server.serve_forever()
import json
from flask import Flask
from flask import request

from datetime import datetime
from sqlalchemy import create_engine

db_string = "postgres://postgres:admin@localhost:5432/RFIDDB"

db = create_engine(db_string)

# Create
# db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")
# db.execute("INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')")

# Read


app = Flask(__name__)

@app.route('/tagsBagsList')
def calculate():
    pg = request.args.get('page')
    print ("Parametro: "+pg)
    offset = 10*(int(pg)-1)
    result_set = db.execute('select * from public."TB_TAG_RECEIVED" order by "DTH_INSERTION" desc LIMIT 10'+' OFFSET '+str(offset))
    tela = ""
    num_recs = 0

    # username = request.form['username']
    docs = []
    saida = ""
    x = ""
    lista =db.execute('select count(*) nro from public."TB_TAG_RECEIVED"')
    tot = 0
    for r in lista:
        print (r.nro)
        tot = r.nro
    # for r in lista:
    #     counterlist = r
    # print(counterlist.split(","))
    # tot = result_set.rowcount
    numberOfPages = tot//10
    if(numberOfPages % 10 != 0):
        numberOfPages = numberOfPages + 1
    if (numberOfPages == 0):
        numberOfPages = 1
    start = pg*10
    for r in result_set:
        tela = tela + "<body><p>" + r.TAG_VALUE + "</p></body>"
        data = {}
        dt = r.DTH_INSERTION
        id = r.ID
        strg = '{:%Y-%m-%d %H:%M:%S}'.format(dt)
        # print (r.DTH_INSERTION)
        # print (strg)
        data['ID'] = str(id)
        data['data'] = strg
        data['tag'] = r.TAG_VALUE
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