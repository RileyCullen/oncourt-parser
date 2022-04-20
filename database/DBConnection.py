import pyodbc

class DBConnection:
    """A singleton class that opens a database connection"""
    _instance = None

    def __new__(cls):
        """
        Enforces singleton pattern for DB connection.
        """
        if (cls._instance is None):
            cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance
    
    def create_connection(self, server: str, database: str, username: str, \
        password: str, driver: str):
        """
        Handles initializing the connection to DB.

        Returns:
        --------
        A pyodbc connection object.
        """
        self._conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+\
            ';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    def get_connection(self): return self._conn

    def close_connection(self): self._conn.close()