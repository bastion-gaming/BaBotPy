import discord
import sqlite3 as sql
import datetime as dt
import time as t
import json
from core import welcome as wel
from gems import gemsFonctions as GF


DB_NOM = 'bastionDB'

conn = sql.connect('DB/{}.db'.format(DB_NOM))

def init():
	with open("DB/DBlist.json", "r") as f:
		l = json.load(f)
	for one in l:
		with open("DB/Templates/{}Template.json".format(one), "r") as f:
			t = json.load(f)
		cursor = conn.cursor()
		script = "CREATE TABLE IF NOT EXISTS {}(".format(one)
		i = 0
		PRIMARYKEY = ""
		PRIMARYKEYlink = ""
		link = ""
		for x in t:
			if i != 0:
				script += ", "
			y = t[x].split("_")
			if len(y) > 1:
				if y[0] == "ID":
					script += "{0} {1} NOT NULL".format(x, y[1])
					link = "FOREIGN KEY(ID) REFERENCES IDs(ID)"
				elif y[0] == "PRIMARYKEY":
					script += "{0} {1} NOT NULL".format(x, y[1])
					PRIMARYKEY = "{}".format(x)
				elif y[0] == "link":
					script += "{0} INTEGER NOT NULL".format(x)
					PRIMARYKEYlink = "{}".format(x)
					link = "FOREIGN KEY({1}) REFERENCES {0}({1})".format(y[1], x)
			else:
				script += "{0} {1}".format(x, t[x])
			i += 1
		if PRIMARYKEY != "" and PRIMARYKEYlink != "":
			script += ", PRIMARY KEY ({}, {})".format(PRIMARYKEY, PRIMARYKEYlink)
		elif PRIMARYKEY != "" and PRIMARYKEYlink == "":
			script += ", PRIMARY KEY ({})".format(PRIMARYKEY)
		elif PRIMARYKEY == "" and PRIMARYKEYlink != "":
			script += ", PRIMARY KEY ({})".format(PRIMARYKEYlink)
		if link != "":
			script += ", {}".format(link)
		script += ")"
		cursor.execute(script)
		conn.commit()
	return "SQL >> DB initialisée"


def checkField():
	with open("DB/DBlist.json", "r") as f:
		l = json.load(f)
	for one in l:
		with open("DB/Templates/{}Template.json".format(one), "r") as f:
			t = json.load(f)
		cursor = conn.cursor()
		cursor.execute("PRAGMA table_info({0});".format(one))
		rows = cursor.fetchall()
		flag = 0

		#Suppression
		for x in rows:
			if x not in t:
				script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
				cursor.execute(script)
				init()
				cursor.execute("PRAGMA table_info({0}_old);".format(one))
				temp = ""
				for z in cursor.fetchall():
					if temp == "":
						temp += "{}".format(z[1])
					else:
						temp += ", {}".format(z[1])
				script = "INSERT INTO {0} ({1})\n	SELECT {1}\n	FROM {0}_old".format(one, temp)
				print(script)
				cursor.execute(script)
				cursor.execute("DROP TABLE {}_old".format(one))
				conn.commit()
				flag = "sup"+str(flag)

		#Type & add
		for x in t:
			check = False
			NotCheck = False
			y = t[x].split("_")
			for row in rows:
				if row[1] == x:
					if len(y) > 1:
						if row[2] == y[1]:
							check = True
						elif y[0] == "link":
							if row[2] == "INTEGER":
								check = True
							else:
								NotCheck = True
						else:
							NotCheck = True
					else:
						if row[2] == t[x]:
							check = True
						else:
							NotCheck = True
			if NotCheck:
				script = "ALTER TABLE {0} RENAME TO {0}_old".format(one)
				cursor.execute(script)
				init()
				cursor.execute("PRAGMA table_info({0}_old);".format(one))
				temp = ""
				for z in cursor.fetchall():
					if temp == "":
						temp += "{}".format(z[1])
					else:
						temp += ", {}".format(z[1])
				script = "INSERT INTO {0} ({1})\n	SELECT {1}\n	FROM {0}_old".format(one, temp)
				print(script)
				cursor.execute(script)
				cursor.execute("DROP TABLE {}_old".format(one))
				conn.commit()
				flag = "type"+str(flag)
			elif not check:
				if len(y) > 1:
					temp = y[1]
				else:
					temp = y[0]
				script = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(one, x, temp)
				cursor.execute(script)
				flag = "add"+str(flag)
	return flag
