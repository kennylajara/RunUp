# Built-in
from pathlib import Path
import sqlite3
from sqlite3 import Error

# 3rd Party
import click


class RunupDB:
    """
    Handle the database where the data is stored.
    
    The `.runup` files are SQLite3 databases containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """
    
    def __init__(self, context:Path, verbose:bool):
        self._dbname:Path = Path(f'{context}/.runup/runup.db')
        self._verbose:bool = verbose
        self._conn = None
        
    def execute(self, query):
        """Execute a query."""

        if self._verbose:
            click.echo(f'Execute query on database: {self._dbname}')
            click.echo(query)

        try:
            c = self._conn.cursor()
            c.execute(query)
        except Error as e:
            click.echo(e)

    def close_connection(self):
        """Close database connection"""

        if self._verbose:
            click.echo(f'Closing connection to: {self._dbname}')
        self._conn.close()
        if self._verbose:
            click.echo(f'Connetion closed')

    def connect(self):
        """Create a database connection to a `runup.db`."""
        if self._verbose:
            click.echo(f'Creating connection to: {self._dbname}')

        try:
            self._conn = sqlite3.connect(self._dbname)
            if self._verbose:
                click.echo(f'Database version: {sqlite3.version}')
        except Error as e:
            click.echo(e)
        
    def create_database(self):
        """Create a database `runup.db`."""
        self.connect()
        self.close_connection()