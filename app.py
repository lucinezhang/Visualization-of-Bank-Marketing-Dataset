#!flask/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask import g
from flask import Response
from flask import request
import json
import MySQLdb
import math


app = Flask(__name__)
CORS(app)

@app.before_request
def db_connect():
    g.conn = MySQLdb.connect(host='localhost', user='root', passwd='password', db='bank')
    g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
    g.cursor.close()
    g.conn.close()
    return response

@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))

def prepare_table(request):		# 根据约束条件准备basic的临时表
	tmp_table = 'DROP TABLE IF EXISTS `tmp_table`; CREATE TABLE tmp_table SELECT * FROM original WHERE '

	if request.form['age'] != 'all':
		tmp_table = tmp_table + 'age>' + request.form['age'][0] + request.form['age'][1] + ' AND age<=' + request.form['age'][3] + request.form['age'][4]
	else:
		tmp_table = tmp_table + 'age>15 AND age<=95'

	if request.form['job'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'job="' + request.form['job'] + '"'
	else:
		tmp_table = tmp_table + ' AND job IN ("admin.","blue-collar","entrepreneur","housemaid","management","retired","self-employed","services","student","technician","unemployed","unknown")'

	if request.form['marital'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'marital="' + request.form['marital'] + '"'
	else:
		tmp_table = tmp_table + ' AND marital IN ("divorced","married","single","unknown")'

	if request.form['education'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'education="' + request.form['education'] + '"'
	else:
		tmp_table = tmp_table + ' AND education IN ("primary","secondary","tertiary","unknown")'

	if request.form['default'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'def="' + request.form['default'] + '"'
	else:
		tmp_table = tmp_table + ' AND def IN ("yes","no","unknown")'

	if request.form['housing'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'housing="' + request.form['housing'] + '"'
	else:
		tmp_table = tmp_table + ' AND housing IN ("yes","no","unknown")'

	if request.form['loan'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'loan="' + request.form['loan'] + '"'
	else:
		tmp_table = tmp_table + ' AND loan IN ("yes","no","unknown")'

	if request.form['contact'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'contact="' + request.form['contact'] + '"'
	else:
		tmp_table = tmp_table + ' AND contact IN ("cellular","telephone","unknown")'

	if request.form['month'] != 'all':
		tmp_table = tmp_table + ' AND ' + 'month="' + request.form['month'] + '"'
	else:
		tmp_table = tmp_table + ' AND month IN ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")'

	g.cursor.execute(tmp_table)
	g.cursor.close()			# 已经执行过一次语句，必须关闭然后再打开
	g.cursor = g.conn.cursor()

# ================================================================= #

def prepare_table_advance(request):		# 根据约束条件准备advance的临时表
	tmp_table = 'DROP TABLE IF EXISTS `tmp_table`; CREATE TABLE tmp_table SELECT * FROM original WHERE '

	if request['age'] != None:
		tmp_table = tmp_table + '('
		for i in range(len(request['age'])):
			tmp_table = tmp_table + 'age>' + request['age'][i][0] + request['age'][i][1] + ' AND age<=' + request['age'][i][3] + request['age'][i][4]
			if i<len(request['age'])-1:
				tmp_table = tmp_table + ' OR '
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + 'age>15 AND age<=95'

	if request['job'] != None:
		tmp_table = tmp_table + ' AND job IN ('
		for i in range(len(request['job'])):
			tmp_table = tmp_table + '"' + request['job'][i] + '"'
			if i<len(request['job'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND job IN ("admin.","blue-collar","entrepreneur","housemaid","management","retired","self-employed","services","student","technician","unemployed","unknown")'

	if request['marital'] != None:
		tmp_table = tmp_table + ' AND marital IN ('
		for i in range(len(request['marital'])):
			tmp_table = tmp_table + '"' + request['marital'][i] + '"'
			if i<len(request['marital'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND marital IN ("divorced","married","single","unknown")'

	if request['education'] != None:
		tmp_table = tmp_table + ' AND education IN ('
		for i in range(len(request['education'])):
			tmp_table = tmp_table + '"' + request['education'][i] + '"'
			if i<len(request['education'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND education IN ("primary","secondary","tertiary","unknown")'

	if request['default'] != None:
		tmp_table = tmp_table + ' AND def IN ('
		for i in range(len(request['default'])):
			tmp_table = tmp_table + '"' + request['default'][i] + '"'
			if i<len(request['default'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND def IN ("yes","no","unknown")'

	if request['housing'] != None:
		tmp_table = tmp_table + ' AND housing IN ('
		for i in range(len(request['housing'])):
			tmp_table = tmp_table + '"' + request['housing'][i] + '"'
			if i<len(request['housing'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND housing IN ("yes","no","unknown")'

	if request['loan'] != None:
		tmp_table = tmp_table + ' AND loan IN ('
		for i in range(len(request['loan'])):
			tmp_table = tmp_table + '"' + request['loan'][i] + '"'
			if i<len(request['loan'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND loan IN ("yes","no","unknown")'

	if request['contact'] != None:
		tmp_table = tmp_table + ' AND contact IN ('
		for i in range(len(request['contact'])):
			tmp_table = tmp_table + '"' + request['contact'][i] + '"'
			if i<len(request['contact'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND contact IN ("cellular","telephone","unknown")'

	if request['month'] != None:
		tmp_table = tmp_table + ' AND month IN ('
		for i in range(len(request['month'])):
			tmp_table = tmp_table + '"' + request['month'][i] + '"'
			if i<len(request['month'])-1:
				tmp_table = tmp_table + ','
		tmp_table = tmp_table + ')'
	else:
		tmp_table = tmp_table + ' AND month IN ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")'

	g.cursor.execute(tmp_table)
	g.cursor.close()			# 已经执行过一次语句，必须关闭然后再打开
	g.cursor = g.conn.cursor()


#-----------------第一张图表（年龄）------------------------#

@app.route("/pic1", methods=['GET', 'POST'])  
def pic1():
	prepare_table(request); # 基于当前筛选条件创建一个表格，之后的图都在该表格上查询

	sql1 = 'SELECT count(*) FROM tmp_table WHERE age > 15 AND age <= 25'
	sql2 = 'SELECT count(*) FROM tmp_table WHERE age > 25 AND age <= 35'
	sql3 = 'SELECT count(*) FROM tmp_table WHERE age > 35 AND age <= 45'
	sql4 = 'SELECT count(*) FROM tmp_table WHERE age > 45 AND age <= 55'
	sql5 = 'SELECT count(*) FROM tmp_table WHERE age > 55 AND age <= 65'
	sql6 = 'SELECT count(*) FROM tmp_table WHERE age > 65 AND age <= 75'
	sql7 = 'SELECT count(*) FROM tmp_table WHERE age > 75 AND age <= 85'
	sql8 = 'SELECT count(*) FROM tmp_table WHERE age > 85 AND age <= 95'

	if request.form['age'] != 'all':
		sql = 'SELECT count(*) FROM tmp_table'
		offset = int(request.form['age'][0]) - 1
	else:
		sql = sql1+' UNION '+sql2+' UNION '+sql3+' UNION '+sql4+' UNION '+sql5+' UNION '+sql6+' UNION '+sql7+' UNION '+sql8
		offset = 0

	g.cursor.execute(sql)
	number = g.cursor.fetchall()		# 从数据库获得返回数据
	sendlist=[]
	age = ['15~25','25~35','35~45','45~55','55~65','65~75','75~85','85~95']
	
	Sum = 0
	for item in number:
		Sum = Sum + item[0]				# 统计数据总数

	for item in number:
		i = {'attr':age[offset],'num':item[0], 'percent':round(item[0]/Sum*100)}
		sendlist.append(i)
		offset = offset + 1

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')	# 返回数据给前端
	return resp

#-----------------第二张图表（职业）------------------------#

@app.route("/pic2", methods=['GET', 'POST'])  
def pic2():
	sql = 'SELECT job, count(*) FROM tmp_table GROUP BY job'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'job':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第三张图表（婚姻）------------------------#

@app.route("/pic3", methods=['GET', 'POST'])  
def pic3():
	sql = 'SELECT marital, count(*) FROM tmp_table GROUP BY marital'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第四张图表（教育）------------------------#

@app.route("/pic4", methods=['GET', 'POST'])  
def pic4():
	sql = 'SELECT education, count(*) FROM tmp_table GROUP BY education'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第五张图表（default）------------------------#

@app.route("/pic5", methods=['GET', 'POST'])  
def pic5():
	sql = 'SELECT def, count(*) FROM tmp_table GROUP BY def'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第六张图表（房贷）------------------------#

@app.route("/pic6", methods=['GET', 'POST'])  
def pic6():
	sql = 'SELECT housing, count(*) FROM tmp_table GROUP BY housing'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第七张图表（贷款）------------------------#

@app.route("/pic7", methods=['GET', 'POST'])  
def pic7():
	sql = 'SELECT loan, count(*) FROM tmp_table GROUP BY loan'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第八张图表（联系方式）------------------------#

@app.route("/pic8", methods=['GET', 'POST'])  
def pic8():
	sql = 'SELECT contact, count(*) FROM tmp_table GROUP BY contact'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第九张图表（月份）------------------------#

@app.route("/pic9", methods=['GET', 'POST'])  
def pic9():
	sql = 'SELECT month, count(*) FROM tmp_table GROUP BY month'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]
	# for j in range(12):
	# 	i = {'attr':'null','num':'null'}
	# 	sendlist.append(i)

	# month = {'jan':0,'feb':1,'mar':2,'apr':3,'may':4,'jun':5,'jul':6,'aug':7,'sep':8,'oct':9,'nov':10,'dec':11}

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#===============================advance部分===================================#

#-----------------第一张图表（年龄）------------------------#

@app.route("/apic1", methods=['GET', 'POST'])  
def apic1():
	data = request.get_json(True)
	prepare_table_advance(data); # 基于当前筛选条件创建一个表格，之后的图都在该表格上查询

	sql1 = 'SELECT count(*) FROM tmp_table WHERE age > 15 AND age <= 25'
	sql2 = 'SELECT count(*) FROM tmp_table WHERE age > 25 AND age <= 35'
	sql3 = 'SELECT count(*) FROM tmp_table WHERE age > 35 AND age <= 45'
	sql4 = 'SELECT count(*) FROM tmp_table WHERE age > 45 AND age <= 55'
	sql5 = 'SELECT count(*) FROM tmp_table WHERE age > 55 AND age <= 65'
	sql6 = 'SELECT count(*) FROM tmp_table WHERE age > 65 AND age <= 75'
	sql7 = 'SELECT count(*) FROM tmp_table WHERE age > 75 AND age <= 85'
	sql8 = 'SELECT count(*) FROM tmp_table WHERE age > 85 AND age <= 95'

	sql = ''
	if data['age'] != None:
		for i in range(len(data['age'])):
			if data['age'][i][0] == '1':
				sql = sql + sql1
			elif data['age'][i][0] == '2':
				sql = sql + sql2
			elif data['age'][i][0] == '3':
				sql = sql + sql3
			elif data['age'][i][0] == '4':
				sql = sql + sql4
			elif data['age'][i][0] == '5':
				sql = sql + sql5
			elif data['age'][i][0] == '6':
				sql = sql + sql6
			elif data['age'][i][0] == '7':
				sql = sql + sql7
			elif data['age'][i][0] == '8':
				sql = sql + sql8
			if i<len(data['age'])-1:
				sql = sql + ' UNION '
	else:
		sql = sql1+' UNION '+sql2+' UNION '+sql3+' UNION '+sql4+' UNION '+sql5+' UNION '+sql6+' UNION '+sql7+' UNION '+sql8

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]
	
	Sum = 0
	for item in number:
		Sum = Sum + item[0]

	if data['age'] == None:
		age = ['15~25','25~35','35~45','45~55','55~65','65~75','75~85','85~95']
		offset = 0
		for item in number:
			i = {'attr':age[offset],'num':item[0], 'percent':round(item[0]/Sum*100)}
			sendlist.append(i)
			offset = offset + 1
	else:
		offset = 0
		for item in number:
			i = {'attr':data['age'][offset],'num':item[0], 'percent':round(item[0]/Sum*100)}
			sendlist.append(i)
			offset = offset + 1

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第二张图表（职业）------------------------#

@app.route("/apic2", methods=['GET', 'POST'])  
def apic2():
	sql = 'SELECT job, count(*) FROM tmp_table GROUP BY job'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'job':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第三张图表（婚姻）------------------------#

@app.route("/apic3", methods=['GET', 'POST'])  
def apic3():
	sql = 'SELECT marital, count(*) FROM tmp_table GROUP BY marital'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第四张图表（教育）------------------------#

@app.route("/apic4", methods=['GET', 'POST'])  
def apic4():
	sql = 'SELECT education, count(*) FROM tmp_table GROUP BY education'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第五张图表（default）------------------------#

@app.route("/apic5", methods=['GET', 'POST'])  
def apic5():
	sql = 'SELECT def, count(*) FROM tmp_table GROUP BY def'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第六张图表（房贷）------------------------#

@app.route("/apic6", methods=['GET', 'POST'])  
def apic6():
	sql = 'SELECT housing, count(*) FROM tmp_table GROUP BY housing'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第七张图表（贷款）------------------------#

@app.route("/apic7", methods=['GET', 'POST'])  
def apic7():
	sql = 'SELECT loan, count(*) FROM tmp_table GROUP BY loan'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第八张图表（联系方式）------------------------#

@app.route("/apic8", methods=['GET', 'POST'])  
def apic8():
	sql = 'SELECT contact, count(*) FROM tmp_table GROUP BY contact'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

#-----------------第九张图表（月份）------------------------#

@app.route("/apic9", methods=['GET', 'POST'])  
def apic9():
	sql = 'SELECT month, count(*) FROM tmp_table GROUP BY month'

	g.cursor.execute(sql)
	number = g.cursor.fetchall()
	sendlist=[]

	Sum = 0
	for item in number:
		Sum = Sum + item[1]

	for item in number:
		i = {'attr':item[0],'num':item[1], 'percent':round(item[1]/Sum*100)}
		sendlist.append(i)

	data = json.dumps(sendlist)
	resp = Response(data, status=200, mimetype='application/json')
	return resp

if __name__ == '__main__':
    app.run()

