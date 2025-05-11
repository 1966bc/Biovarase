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
import sqlite3 as lite
import datetime

class DBMS:
    def __init__(self, db_name):
        self.set_connection(db_name)

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(
            self.__class__.__name__, [x.__name__ for x in DBMS.__mro__]
        )

    def set_connection(self, db_name):
        try:
            self.con = lite.connect(
                db_name,
                detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES,
                isolation_level="IMMEDIATE",
            )
        except lite.Error as db_err:
            self.on_log(
                inspect.stack()[0][3],
                db_err,
                type(db_err),
                sys.modules[__name__],
            )
            self.con = None  # Important: Set con to None if connection fails
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            self.con = None

    def write(self, sql, args=()):
        try:
            cur = self.con.cursor()
            cur.execute(sql, args)
            self.con.commit()
            return cur.lastrowid
        except lite.Error as db_err:
            self.con.rollback()
            self.on_log(
                inspect.stack()[0][3],
                db_err,
                type(db_err),
                sys.modules[__name__],
            )
            return None
        except Exception as e:
            self.con.rollback()
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return None
        finally:
            try:
                cur.close()
            except lite.Error as cur_err:
                self.on_log(
                    inspect.stack()[0][3],
                    cur_err,
                    type(cur_err),
                    sys.modules[__name__],
                )

    def read(self, fetch, sql, args=()):
        """Remember that fetchall() return a list.  An empty list
        is returned when no rows are available.  Testing if the list
        is empty with 'if rs' or 'if not rs' Otherwise fetchone()
        return a single sequence, or None when no more data is
        available.  Testing as 'if rs is not None'.
        """
        try:
            cur = self.con.cursor()
            cur.execute(sql, args)

            if fetch:
                rs = cur.fetchall()
            else:
                rs = cur.fetchone()
            cur.close()
            return rs
        except lite.Error as db_err:
            self.on_log(
                inspect.stack()[0][3],
                db_err,
                type(db_err),
                sys.modules[__name__],
            )
            return None
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return None
        finally:
            try:
                cur.close()
            except lite.Error as cur_err:
                self.on_log(
                    inspect.stack()[0][3],
                    cur_err,
                    type(cur_err),
                    sys.modules[__name__],
                )

    def get_last_row_id(self, cur):
        try:
            return cur.lastrowid
        except lite.Error as db_err:
            self.on_log(
                inspect.stack()[0][3],
                db_err,
                type(db_err),
                sys.modules[__name__],
            )
            return None
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return None

    def get_fields(self, table):
        """Return fields name of the args table ordered by field number."""

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
        except lite.Error as db_err:
            self.on_log(
                inspect.stack()[0][3],
                db_err,
                type(db_err),
                sys.modules[__name__],
            )
            return tuple()  # Return empty tuple on error
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return tuple()

    def get_update_sql(self, table, pk):
        """Recive a table name and his pk to format an update sql statement."""
        try:
            fields = self.get_fields(table)
            if not fields:
                return None  # Or raise an exception if appropriate
            y = []
            for i in map((lambda x: x + " =?"), fields):
                y.append(i)

            s = ",".join(y)

            return "UPDATE {0} SET {1} WHERE {2}{3}".format(table, s, pk, "=?")
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return None

    def get_insert_sql(self, table, n):
        """Recive a table name and len of args, len(args),  to format an insert sql statement"""
        try:
            fields = self.get_fields(table)
            if not fields:
                return None  # Or raise an exception
            return "INSERT INTO {0}({1})VALUES({2})".format(
                table, ",".join(fields), ",".join(["?"] * n)
            )
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return None

    def dump_db(self):
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = dt + ".sql"
        try:
            with open(filename, 'w') as f:
                if self.con:
                    try:
                        for line in self.con.iterdump():
                            f.write('%s\n' % line)
                    except lite.Error as db_err:
                        self.on_log(
                            inspect.stack()[0][3],
                            db_err,
                            type(db_err),
                            sys.modules[__name__],
                        )
                        return False  # Indicate failure
                    except Exception as e:
                        self.on_log(
                            inspect.stack()[0][3],
                            e,
                            type(e),
                            sys.modules[__name__],
                        )
                        return False  # Indicate failure
                    return True  # Indicate success
                else:
                    self.on_log(
                        inspect.stack()[0][3],
                        "Warning",
                        "Database connection is not established. Cannot dump.",
                        sys.modules[__name__],
                    )
                    return False  # Indicate failure
        except IOError as io_err:
            self.on_log(
                inspect.stack()[0][3],
                io_err,
                type(io_err),
                sys.modules[__name__],
            )
            return False  # Indicate failure
        except Exception as e:
            self.on_log(
                inspect.stack()[0][3],
                e,
                type(e),
                sys.modules[__name__],
            )
            return False  # Indicate failure

    
def main():

    foo = DBMS("biovarase.db")
    print(foo.con)

if __name__ == "__main__":
    main()

