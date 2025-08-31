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
    def __init__(self, db_name, autocommit=True):
        
        self.db_name = db_name
        self.autocommit = autocommit
        self.con = None
        self._set_connection()

    def __str__(self):
        return "class: {0}\nMRO: {1}".format(
            self.__class__.__name__, [x.__name__ for x in type(self).__mro__]
        )

    def _set_connection(self):
        try:
            isolation = None if self.autocommit else "IMMEDIATE"
            self.con = lite.connect(
                self.db_name,
                detect_types=lite.PARSE_DECLTYPES | lite.PARSE_COLNAMES,
                isolation_level=isolation,
            )
            return self.con
        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None


    def _ensure_connection(self):
        """Ensure there is a usable connection. If missing or broken, reopen it.
        For SQLite we attempt a lightweight SELECT 1 to validate the handle.
        """
        if self.con is None:
            self._set_connection()
            return
        try:
            cur = self.con.cursor()
            try:
                cur.execute("SELECT 1")
            finally:
                cur.close()
        except Exception:
            # Reopen on failure
            self._set_connection()

    def write(self, sql, args=()):
        """
            Execute a DML statement (INSERT/UPDATE/DELETE).
            Returns:
              - lastrowid when available and non-zero,
              - otherwise the affected rowcount,
              - None on error.
            Commits only if autocommit is disabled.
        """
        cursor = None
        try:
            self._ensure_connection()
            if self.con is None:
                raise RuntimeError("No active DB connection")
            
            params = tuple(args)
            cursor = self.con.cursor()
            cursor.execute(sql, params)

            if not self.autocommit:
                self.con.commit()

            last_id = getattr(cursor, "lastrowid", None)
            return last_id if last_id not in (None, 0) else cursor.rowcount
        
        except Exception as e:
            # Rollback only if autocommit is disabled
            try:
                if cursor and not getattr(self, "autocommit", True):
                    self.con.rollback()
            except Exception:
                pass

            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None

        finally:

            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)

    def read(self, fetch, sql, args=()):
        """
            Execute a SELECT.
            If fetch is True:  return a list (possibly empty).
            If fetch is False: return a single row or None when no rows.
            Remember that fetchall() return a list.  An empty list
            is returned when no rows are available.  Testing if the list
            is empty with 'if rs' or 'if not rs' Otherwise fetchone()
            return a single sequence, or None when no more data is
            available.  Testing as 'if rs is not None'.
        """
        cursor = None
        try:
            self._ensure_connection()
            if self.con is None:
                raise RuntimeError("No active DB connection")
            params = tuple(args)
            cursor = self.con.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall() if fetch else cursor.fetchone()
        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            # keep the original behavior: None on error
            return None

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)

    def _get_columns(self, table):
        """
            Internal helper.
            Return all column names in declaration order (PK included as the first).
            Uses LIMIT 0 to fetch only cursor metadata.
        """
        cursor = None
        try:
            self._ensure_connection()
            if self.con is None:
                raise RuntimeError("No active DB connection")

            sql = f"SELECT * FROM {table} LIMIT 0"
            cursor = self.con.cursor()
            cursor.execute(sql)
            desc = cursor.description or ()
            return tuple(d[0] for d in desc)
        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return tuple()
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as e:
                    f = inspect.currentframe()
                    function = f.f_code.co_name + ".close"
                    caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)


    def build_sql(self, table, op):
        """
        Generate SQL for INSERT or UPDATE using project conventions:
        - PK is the first column 
        - placeholders use '?'
        """
        try:
            all_cols = list(self._get_columns(table))  # includes PK as first column
        
            if op == "insert":
                fields = all_cols[1:]  # skip PK
                cols_list = ",".join(fields)
                placeholders = ",".join(["?"] * len(fields))
                return f"INSERT INTO {table}({cols_list}) VALUES({placeholders})"

            elif op == "update":
                primary_key = all_cols[0]
                set_cols = [c for c in all_cols if c != primary_key]
                set_clause = ", ".join(f"{c} = ?" for c in set_cols)
                return f"UPDATE {table} SET {set_clause} WHERE {primary_key} = ?"

            else:
                raise ValueError("op must be 'insert' or 'update'")

        except Exception as e:
            f = inspect.currentframe()
            function = f.f_code.co_name
            caller = f.f_back.f_code.co_name if f and f.f_back else "<top>"
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return None

    def dump_db(self):
        """
            Dump the whole SQLite DB using iterdump() into a timestamped .sql file.
        """
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = dt + ".sql"
        try:
            if self.con is None:
                # Log a warning (no active exception here)
                frame = inspect.currentframe()
                try:
                    function = frame.f_code.co_name
                    caller = frame.f_back.f_code.co_name if frame and frame.f_back else "<top>"
                finally:
                    del frame
                self.on_log(function,
                            "Database connection is not established. Cannot dump.",
                            Warning,
                            sys.modules[__name__],
                            caller)
                return False

            with open(filename, "w", encoding="utf-8", errors="backslashreplace") as fh:
                try:
                    for line in self.con.iterdump():
                        fh.write(f"{line}\n")
                except Exception as e:
                    frame = inspect.currentframe()
                    try:
                        function = frame.f_code.co_name
                        caller = frame.f_back.f_code.co_name if frame and frame.f_back else "<top>"
                    finally:
                        del frame
                    self.on_log(function, e, type(e), sys.modules[__name__], caller)
                    return False

            return True

        except Exception as e:
            frame = inspect.currentframe()
            try:
                function = frame.f_code.co_name
                caller = frame.f_back.f_code.co_name if frame and frame.f_back else "<top>"
            finally:
                del frame
            self.on_log(function, e, type(e), sys.modules[__name__], caller)
            return False

    
def main():

    foo = DBMS("biovarase.db")
    print(foo)
    print(foo.con)

if __name__ == "__main__":
    main()


