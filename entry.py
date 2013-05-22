import sqlite3 as lite
import sys
import pickle

con = lite.connect('semNet.db')

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS skosNet")
cur.execute("CREATE TABLE IF NOT EXISTS skosNet(skosNode TEXT PRIMARY KEY, neighbors TEXT)")

s = raw_input("Enter skos file no: ")
with open('skos_'+str(s)+'.dict','r') as f:
        d=pickle.load(f)
        i=0
        for node in d:
                cur.execute("INSERT INTO skosNet (skosNode, neighbors) VALUES(?,?)", (node, str(d[node])))
                i+=1
        con.commit()
        print 'Entry complete.. = ', i, ' records'


if con:
        con.close()
