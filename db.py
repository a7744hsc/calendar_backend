from flask import  g
import sqlite3
# from .main import app

# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')

def get_db(db_address):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(db_address)
    return g.sqlite_db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db(db_address):
    print("""Connects to the specific database.""")
    rv = sqlite3.connect(db_address)
    # rv.row_factory = sqlite3.Row
    rv.row_factory = dict_factory

    return rv