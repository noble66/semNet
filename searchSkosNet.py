import sqlite3 as lite
import sys
import pickle

# searches SKOS network using semNet.db i.e. nodes which are keys in adjacency associated array

def get_neigbors(word):

        con = lite.connect('semNet.db')
        result = []
        with con:
                print 'Searching word: ', word
                cur = con.cursor()
                cur.execute("SELECT neighbors FROM skosNet where skosNode LIKE ?", (word,))
                rows = cur.fetchall()
                for row in rows:
                        result.append(row)
        return result


def retrive_keys():
        con = lite.connect('semNet.db')
        result = []
        with con:
                cur = con.cursor()
                cur.execute("SELECT skosNode FROM skosNet")
                rows = cur.fetchall()
                for r in rows:
                        result.append(r)
                print 'Returning list of ', len(rows), 'unique skos nodes'
                return result
                
def match_keys(target):
        with open('skosKeys.list','r') as f:
                result = []
                klist = pickle.load(f)
                for k in klist:
                        words_in_key = [str(x.lower()) for x in str(k).strip('\(\)').split('_')]
                        words_in_key[0]= words_in_key[0][2:]
                        words_in_key[-1] = words_in_key[-1][:-2]
                        if target.lower() in words_in_key:
                                result.append(k)
                return result

