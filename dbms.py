#!/usr/bin/env python
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppe.costanzi@gmail.com]
# modify:   08/12/2014
# version:  0.2                                                                  
#-----------------------------------------------------------------------------

import sqlite3 as lite
import os
import sys
import numpy

class DBMS(object):
    def __init__(self,):
        super(DBMS, self).__init__()

       
    def get_connection(self,):

        return lite.connect('biovarase.db',isolation_level = 'IMMEDIATE')
        
        
    def read(self, fetch, sql, args=()):
       
        try:
            
            con = self.get_connection()

            cur = con.cursor()
        
            cur.execute(sql,args)

            if fetch == True:
                rs =  cur.fetchall()
            else:
                rs =  cur.fetchone()
            
            return rs

        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

   
    def write(self, sql, args=()):
        try:
            con = self.get_connection() 
            cur = con.cursor()
            cur.execute(sql,args)
            con.commit()
            
        except:
            con.rollback()
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])


    def get_fields(self,table):
        """Return fields name for the passed table ordered by field position"""

        try:

            columns = []
            ret = []

            sql = 'SELECT * FROM %s ' % table
            con = self.get_connection()
            cur = con.cursor()
            cur.execute(sql)

            for field in cur.description:
                columns.append(field[0])
            cur.close()
            
            for k,v in enumerate(columns):
                if k > 0:
                    ret.append(v)
            return ret
        except:
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            
        finally:
            try:
                cur.close()
                con.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])

    def get_update_sql(self,table,pk):

        return "UPDATE %s SET %s =? WHERE %s =?"%(table," =?, ".join(self.get_fields(table)),pk)

    def get_insert_sql(self,table,n):

        #n = len(args)

        return "INSERT INTO %s(%s)VALUES(%s)"%(table,",".join(self.get_fields(table)), ",".join("?"*n))

    def get_selected(self,table,field,*args):
        """recive table name, pk and return a dictionary
       
        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """
        
        d = {}
        sql = "SELECT * FROM %s WHERE %s =?" % (table,field)

        for k,v in enumerate(self.read(False,sql,args)):
            d[k]=v
            
        return d

    def get_update_sql_args(self, args, item):
        l = list(args)
        l.append(item)
        return tuple(l)

    def get_stat(self,batch_id,limit,):

        #print batch_id,limit,

        try:

            sql = "SELECT result_id,\
                          ROUND(result,2)\
                   FROM results\
                   WHERE batch_id =?\
                   AND enable =1\
                   ORDER BY result_id DESC\
                   LIMIT ?"

            args = (batch_id, limit)
            rs = self.read(True, sql, args)
            
            results=[]
            if len(rs) > 5:
                for i in rs:
                    results.append(float(i[1]))

                avg = round(numpy.mean(results),2)
                sd = round(numpy.std(results),2)
                cv = (sd/avg)*100
                return len(rs),cv,avg,sd
            else:
                return False
        except:
            print batch_id,limit
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            print sys.exc_info()[2]
            return False   
                

    
def main():
    
    foo = DBMS()
    print (foo)

    sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    rs = foo.read(True, sql)
    if rs:
        for i in enumerate(rs):
            print (i)

   
    raw_input('end')
    
    
if __name__ == "__main__":
    main()
