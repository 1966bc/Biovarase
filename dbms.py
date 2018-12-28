#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This is the database administration module of Biovarase."""
import sys
import inspect
import sqlite3 as lite
import datetime

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "4.2"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2018-12-25"
__status__ = "Production"


class DBMS(object):
    def __init__(self, *args, **kwargs):
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

    def dump_db(self,):

        
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        s = dt + ".sql"
        with open(s, 'w') as f:
            for line in self.con.iterdump():
                f.write('%s\n' % line)


    def get_last_row_id(self, cur):

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



