#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  biovarase
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   ver MMXXV
# -----------------------------------------------------------------------------
import sys
import inspect

import bcrypt 

class Controller:
    
    def __str__(self):
        return "class: {0}\nMRO: {1}".format(self.__class__.__name__,
                                             [x.__name__ for x in Controller.__mro__],)

    def get_new_password(self):
        try:
            new_password = b'pass'
            # Generate a salt and hash the password
            hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            return hashed_password
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
                level="error",
                message=f"Error generating new password: {e}",
            )
            return None  # Or raise an exception, depending on your error handling policy

    def on_login(self, args):
        nick, password = args
        password = password.strip()  # Rimuovi spazi (già byte string)

        sql = "SELECT pswrd FROM users WHERE nickname =?;"
        cur = self.con.cursor()
        cur.execute(sql, (nick,))
        result = cur.fetchone()

        if result:
            hashed_password_from_db = result[0].encode('utf-8')  # Codifica l'hash dal DB a byte string
            if bcrypt.checkpw(password, hashed_password_from_db):  # Confronta byte strings
                sql = "SELECT * FROM users WHERE nickname =?;"
                cur = self.con.cursor()
                cur.execute(sql, (nick,))
                return cur.fetchone()
            else:
                return None
        else:
            return None

    def get_selected(self, table, field, *args):
        """Recive table name, pk and return a row as a dictionary."""
        d = {}
        try:
            sql = "SELECT * FROM {0} WHERE {1} = ?".format(table, field)
            for k, v in enumerate(self.read(False, sql, args)):
                d[k] = v
            return d
        except sqlite3.Error as db_err:
            self.on_log(inspect.stack()[0][3], db_err, type(db_err), sys.modules[__name__], level='error', message=f"Database error while selecting from {table}: {db_err}")
            return {}
        except Exception as e:
            self.on_log(inspect.stack()[0][3], e, type(e), sys.modules[__name__], level='error', message=f"An unexpected error occurred in get_selected: {e}")
            return {}

    def get_mandatory(self):
        mandatory_tests = []
        sql = "SELECT tests.description " \
              "FROM tests " \
              "INNER JOIN tests_methods ON tests.test_id = tests_methods.test_id " \
              "INNER JOIN sections ON tests_methods.section_id = sections.section_id " \
              "INNER JOIN labs ON sections.lab_id = labs.lab_id " \
              "INNER JOIN sites ON labs.site_id = sites.site_id " \
              "WHERE sections.section_id =? " \
              "AND tests_methods.is_mandatory = 1 " \
              "AND tests_methods.status = 1;"

        args = (self.get_section_id(),)
        rs = self.read(True, sql, args)  # Let read() handle errors

        if rs:
            for i in rs:
                mandatory_tests.append(i[0])

        return mandatory_tests

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

    def get_idd_by_section_id(self, section_id):

        sql = "SELECT sites.site_id,\
                      sites.supplier_id,\
                      sites.comp_id,\
                      labs.lab_id,\
                      sections.section_id\
               FROM sites\
               INNER JOIN labs ON sites.site_id = labs.site_id\
               INNER JOIN sections ON labs.lab_id = sections.lab_id\
               WHERE sections.section_id =?;"

        args = (section_id,)

        rs = self.read(False, sql, args)

        return rs

    def get_test_name(self, test_id):

        sql = "SELECT * FROM tests WHERE test_id =?;"
        args = (test_id,)
        rs = self.read(False, sql, args)
        return rs[1]

    def get_control_name(self, control_id):

        sql = "SELECT description FROM controls WHERE control_id =?;"
        args = (control_id,)
        rs = self.read(False, sql, args)
        return rs[0]

    def get_um(self, unit_id):

        sql = "SELECT unit FROM units WHERE unit_id =?;"
        return self.read(False, sql, (unit_id,))

def main():

    bar = Controller()
    print(bar)
    input('end')


if __name__ == "__main__":
    main()


