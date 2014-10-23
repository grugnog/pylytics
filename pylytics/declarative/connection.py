"""
Utilities for making database connections easier.
"""

import mysql


def get_named_connection(connection_name):
    if connection_name not in (settings.DATABASES.keys()):
        raise ValueError("The database {} isn't recognised - check "
                         "your settings in settings.py".format(database))
    else:
        kwargs = settings.DATABASES[connection_name]
        return mysql.connector.connect(**kwargs)


class NamedConnection(object):
    """
    Returns a connection, using database parameters defined in the settings
    file.

    Example usage:
        with NamedConnection('platform') as connection:
            cursor = connection.cursor( ... )
            cursor.execute('...')
            cursor.close()

    """

    # Having use_connection_pool would be interesting here too.
    # But we don't need connection pools for now. Unless it would allow us to
    # pull and push data in parallel.
    def __init__(self, connection_name, *args, **kwargs):
        self.connection_name = connection_name

    def __enter__(self):
        self.connection = get_named_connection(self.connection_name)
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()
