import sqlite3
import csv
from pathlib import Path

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def import_questions_answers_weights_from_csv():
    db = get_db()
    cursor = db.cursor()

    mod_path = Path(__file__).parent.parent
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"PRAGMA table_info ({table['name']})")
        table_info = cursor.fetchall()
        table_n_columns = len(table_info)
        src_path = (mod_path/f"{table['name']}s.csv").resolve()
        file = open(src_path)
        contents = csv.reader(file)
        insert_records = f"INSERT INTO {table['name']} {tuple(contents.__next__())} VALUES ({ (table_n_columns-1)*'?,' + '?'})"
        cursor.executemany(insert_records, contents)

    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    import_questions_answers_weights_from_csv()
    click.echo('Imported questions, answers and weights from csv files')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
