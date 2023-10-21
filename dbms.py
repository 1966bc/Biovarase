#!/usr/bin/env python3
import sys
import inspect
import sqlite3 as lite
import datetime



class DBMS:
    def __init__(self,):

        self.set_connection()

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in DBMS.__mro__],)

    def set_connection(self):

        try:

            self.con = lite.connect("biovarase.db",
                                    detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES,
                                    isolation_level='IMMEDIATE')

            self.con.text_factory = lite.OptimizedUnicode

        except:
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                        sys.exc_info()[0], sys.modules[__name__])

    def get_mandatory(self):

        mandatory_tests = []

        sql = "SELECT tests.test\
               FROM tests\
               INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id\
               INNER JOIN sections ON tests_methods.section_id = sections.section_id\
               INNER JOIN wards ON sections.ward_id = wards.ward_id\
               INNER JOIN sites ON wards.site_id = sites.site_id\
               WHERE sections.section_id =?\
               AND tests_methods.is_mandatory =1\
               AND tests_methods.status =1;"

        args = (self.get_section_id(),)

        rs = self.read(True, sql, args)

        if rs:
            for i in rs:
                mandatory_tests.append(i[0])

        return mandatory_tests

    def get_records(self):

        try:
            file = open('records', 'r')
            ret = file.readline()
            file.close()
            return ret
        except:
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                        sys.exc_info()[0], sys.modules[__name__])

    def write(self, sql, args=()):

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)
            self.con.commit()
            return cur.lastrowid

        except:
            self.con.rollback()
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                        sys.exc_info()[0], sys.modules[__name__])

        finally:
            try:
                cur.close()
            except:
                self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                            sys.exc_info()[0], sys.modules[__name__])

    def read(self, fetch, sql, args=()):

        """Remember that fetchall() return a list.\
           An empty list is returned when no rows are available.
           Testing if the list is empty with 'if rs' or 'if not rs'
           Otherwise fetchone() return a single sequence, or None
           when no more data is available.
           Testing as 'if rs is not None'.
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql, args)

            if fetch == True:
                rs = cur.fetchall()
            else:
                rs = cur.fetchone()
            cur.close()
            return rs

        except:
            #print(sql, args)
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def dump_db(self,):

        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        s = dt + ".sql"
        with open(s, 'w') as f:
            for line in self.con.iterdump():
                f.write('%s\n' % line)
                

    def get_last_row_id(self, cur):
        return cur.lastrowid

    def get_fields(self, table):
        """return fields name of the args table ordered by field number

        @param name: table,
        @return: fields
        @rtype: tuple
        """

        try:
            columns = []
            fields = []
            sql = "SELECT * FROM {0}".format(table)
            cur = self.con.cursor()
            cur.execute(sql)

            for field in cur.description:
                columns.append(field[0])
            cur.close()

            for k, v in enumerate(columns):
                if k > 0:
                    fields.append(v)

            return tuple(fields)
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])


    def get_update_sql(self, table, pk):
        """recive a table name and his pk to format an update sql statement

        @param name: table, pk
        @return: sql formatted stringstring
        @rtype: string
        """
        """"""

        y = []
        for i in map((lambda x: x + " =?"), self.get_fields(table)):
            y.append(i)

        s = ",".join(y)
        return "UPDATE {0} SET {1} WHERE {2}{3}".format(table, s, pk, "=?")

    def get_insert_sql(self, table, n):
        """recive a table name and len of args, len(args),
           to format an insert sql statement

        @param name: table, n
        @return: sql formatted string
        @rtype: string
        """
        try:

            return "INSERT INTO {0}({1})VALUES({2})".format(table, ",".join(self.get_fields(table)), ",".join(["?"]*n))

        except:
            self.on_log(inspect.stack()[0][3], sys.exc_info()[1],
                        sys.exc_info()[0], sys.modules[__name__])

    def get_selected(self, table, field, *args):
        """Recive table name, pk and return a row as a dictionary.
        @param name: table, field, *args
        @return: dictionary
        @rtype: dictionary
        """
        d = {}

        sql = "SELECT * FROM {0} WHERE {1} = ?".format(table, field)


        for k, v in enumerate(self.read(False, sql, args)):
            d[k] = v

        return d

    def get_series(self, batch_id, workstation_id, limit=None, result_id=None):

        series = []

        if result_id is not None:

            sql = "SELECT ROUND(result,2),status\
                   FROM results\
                   WHERE batch_id =?\
                   AND result_id <=?\
                   AND workstation_id =?\
                   AND is_delete =0\
                   ORDER BY recived DESC\
                   LIMIT ?;"

            args = (batch_id, result_id, workstation_id, limit)

            rs = self.read(True, sql, args)

        else:

            sql = "SELECT ROUND(result,2),status\
                   FROM results\
                   WHERE batch_id =?\
                   AND workstation_id =?\
                   AND is_delete =0\
                   ORDER BY recived DESC\
                   LIMIT ?;"

            args = (batch_id, workstation_id, limit)

            rs = self.read(True, sql, args)


        rs = tuple(i for i in rs if i[1] != 0)

        for i in reversed(rs):
            series.append(i[0])

        return series

    def get_site_description(self,):

        sql = "SELECT sites.site_id,\
                      companies.supplier AS company,\
                      suppliers.supplier AS site,\
                      wards.ward,\
                      sections.section,\
                      sites.status\
               FROM sites\
               INNER JOIN suppliers AS companies ON companies.supplier_id = sites.supplier_id\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               INNER JOIN wards ON sites.site_id = wards.site_id\
               INNER JOIN sections ON wards.ward_id = sections.ward_id\
               WHERE sections.section_id =?;"

        args = (self.get_section_id(),)

        return self.read(False, sql, args)

    def login(self, args):

        sql = "SELECT * FROM users WHERE nickname =? AND pswrd =?;"

        cur = self.con.cursor()

        cur.execute(sql, args)

        return cur.fetchone()

    def get_section(self):

        section_id = self.get_section_id()

        args = (section_id,)

        sql = " SELECT suppliers.supplier, wards.ward, sections.section\
                FROM sites\
                INNER JOIN suppliers ON sites.comp_id = suppliers.supplier_id\
                INNER JOIN wards ON sites.site_id = wards.site_id\
                INNER JOIN sections ON wards.ward_id = sections.ward_id\
                WHERE sections.section_id=?;"

        cur = self.con.cursor()

        cur.execute(sql, args)

        self.section = cur.fetchone()

        cur.close()


    def get_test_name(self, test_id):
        sql = "SELECT * FROM tests WHERE test_id =?;"
        args = (test_id,)
        rs = self.read(False, sql, args)
        return rs[2]

    def get_control_name(self, control_id):

        sql = "SELECT description FROM controls WHERE control_id =?;"
        args = (control_id,)
        rs = self.read(False, sql, args)
        return rs[0]


    def get_section_data(self, section_id):

        sql = "SELECT suppliers.supplier_id,\
                      sites.site_id,\
                      wards.ward_id,\
                      sections.section_id\
               FROM sites\
               INNER JOIN suppliers ON suppliers.supplier_id = sites.comp_id\
               INNER JOIN wards ON sites.site_id = wards.ward_id\
               INNER JOIN sections ON wards.ward_id = sections.ward_id\
               WHERE sections.section_id =?;"

        args = (section_id,)

        return self.read(False, sql, args)

    def get_um(self, unit_id):

        sql = "SELECT unit FROM units WHERE unit_id =?;"
        return self.read(False, sql, (unit_id,))


def main():

    bar = DBMS()
    bar.set_connection()

    sql = "SELECT * FROM tests;"

    rs = bar.read(True, sql, ())

    print (rs)

    print(bar)
    input('end')


if __name__ == "__main__":
    main()

