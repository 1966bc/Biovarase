#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   winter 2018                                                              
#-----------------------------------------------------------------------------

import sqlite3 as lite
import sys
import os
import numpy
import inspect

class DBMS(object):
    def __init__(self,*args, **kwargs):
        super(DBMS, self).__init__( *args, **kwargs)

        self.args = args
        self.kwargs = kwargs
        
        path = 'biovarase.db'
        self.get_connection(path)
       
    def get_connection(self, path):
       
        self.con = lite.connect(path,
                                detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES,
                                isolation_level = 'IMMEDIATE')
        self.con.text_factory = lite.OptimizedUnicode
        

    def write(self, sql, args=()):
        
        try:
            cur = self.con.cursor()
            cur.execute(sql,args)
            self.con.commit()
            
        except:
            self.con.rollback()
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            print (sql,args)
        finally:
            try:
                cur.close()
            except:
                print (sys.exc_info()[0])
                print (sys.exc_info()[1])
                print (sys.exc_info()[2])
                print (sql,args)
                

    def read(self, fetch, sql, args=()):

        #print  sql, args
       
        try:
            cur = self.con.cursor()
            cur.execute(sql,args)

            if fetch == True:
                rs =  cur.fetchall()
            else:
                rs =  cur.fetchone()
            cur.close()                
            return rs

        except:
            print(inspect.stack()[0][3])
            print (fetch, sql, args)
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])


    def get_last_row_id(self,cur):

        return cur.lastrowid            
             
   
    def get_fields(self,table):
        """return fields name of the args table ordered by field number
       
        @param name: table,
        @return: fields
        @rtype: tuple
        """        
        try:
            
            columns = []
            fields = []

            sql = 'SELECT * FROM %s ' % table
            cur = self.con.cursor()
            cur.execute(sql)
            

            for field in cur.description:
                columns.append(field[0])
            cur.close()
            
            for k,v in enumerate(columns):
                if k > 0:
                    fields.append(v)
                    
            return tuple(fields)
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])



    def get_update_sql_args(self, args, item):
        l = list(args)
        l.append(item)
        return tuple(l)
    
    # FIXME This function sometimes returns incorrect data when pass datetime type on timestamp field.
    def get_update_sql(self,table,pk):
        """recive a table name and his pk to format an update sql statement
           
        @param name: table, pk
        @return: sql formatted stringstring
        @rtype: string
        """
        """"""

        return "UPDATE %s SET %s =? WHERE %s =?"%(table," =?, ".join(self.get_fields(table)),pk)

    # FIXME This function sometimes returns incorrect data when pass datetime type on timestamp field.
    def get_insert_sql(self,table,n):
        """recive a table name and len of args, len(args),
           to format an insert sql statement
       
        @param name: table, n
        @return: sql formatted stringstring
        @rtype: string
        """
        try:
            return "INSERT INTO %s(%s)VALUES(%s)"%(table,",".join(self.get_fields(table)), ",".join("?"*n))
        except:
            print(inspect.stack()[0][3])
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])


    # FIXME This function sometimes fails  when recive datetime type on timestamp field.
    def get_selected(self,table,field,*args):
        """recive table name, pk and make a dictionary
       
        @param name: table,field,*args
        @return: dictionary
        @rtype: dictionary
        """
        
        d = {}
        sql = 'SELECT * FROM %s WHERE %s = ? ' % (table,field)

        for k,v in enumerate(self.read(False,sql,args)):
            d[k]=v
            #print k,v

        return d


    def get_stat(self,batch_id,limit,):
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
            print (batch_id,limit)
            print (sys.exc_info()[0])
            print (sys.exc_info()[1])
            print (sys.exc_info()[2])
            return False

    def get_series(self, batch_id, limit):

        series = []

        sql = "SELECT result FROM results WHERE batch_id =? AND enable =1 ORDER BY result_id  DESC LIMIT ?"

        rs = self.read(True, sql, (batch_id, limit))

        for i in rs:
             series.append(i[0])

        return series

def main():

    bar = DBMS()
    print (bar)
    sql = "SELECT name FROM sqlite_master WHERE type = 'view'"
    rs = bar.read(True, sql)
    if rs:
        for i in enumerate(rs):
            print (i)

    input('end')
       
if __name__ == "__main__":
    main()


    
