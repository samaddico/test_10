from core.db.helpers import call_close, get_autocommit_connection
from core.environment import DB_DATA


class DBConn:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def _connect(self):
        if not self._has_connection():
            self._connection = get_autocommit_connection(**DB_DATA)
            self._cursor = self._connection.cursor()

    def _has_connection(self):
        return self._connection and self._cursor

    def __del__(self):
        call_close(self._cursor, self._connection)


class Query(DBConn):
    def __init__(self):
        super().__init__()

        self._params = None
        self._query_string = None

    def prepare(self, query_string: str, params: tuple = None):
        self._params = params
        self._query_string = query_string

    def execute(self):
        args = (self._query_string, self._params) if self._params else (self._query_string,)
        self._connect()
        self._cursor.execute(*args)
