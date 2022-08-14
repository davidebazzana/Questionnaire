import sqlite3
import csv
from pathlib import Path

import click
from flask import current_app, g
from flask.cli import with_appcontext

TABLES_NAME_AND_NUMBER_OF_COLUMNS = [('question',15), ('ans_weight',4)]

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
    
    for table in TABLES_NAME_AND_NUMBER_OF_COLUMNS:
        src_path = (mod_path/f"{table[0]}s.csv").resolve()
        file = open(src_path)
        contents = csv.reader(file)
        insert_records = f"INSERT INTO {table[0]} {tuple(contents.__next__())} VALUES ({ (table[1]-1)*'?,' + '?'})"
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
