import sqlite3
import json
import sys

DB_NAME = "schneehoehen.db"


def get_cursor(db_name=DB_NAME):
    connection = sqlite3.connect(db_name)
    return connection.cursor()


def db_connect(func):
    def _db_connect(*args, **kwargs):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return _db_connect


@db_connect
def create_table(cursor):
    create_sql = """create table if not exists 
        data(name text, date text, tal int, berg int, neuschnee int, zustand text, letzter text, UNIQUE(name, date) ON CONFLICT REPLACE);
    """
    cursor.execute(create_sql)


VALUES = [
    ("adelboden-lenk", "2024-10-16", 0, 0, 0, "k.A.", "k.A."),
    ("arlberg", "2024-10-16", 0, 0, 0, "k.A.", "k.A."),
]


@db_connect
def insert(cursor, values):
    cursor.executemany(
        "insert into  data(name, date, tal, berg, neuschnee, zustand, letzter) values (?, ?, ?, ?, ?, ?, ?)",
        values,
    )


@db_connect
def dump(cursor):
    sql = """SELECT * from data order by name, date"""
    cursor.execute(sql)
    for row in cursor.fetchall():
        print(row)


def normalize(s):
    if s == "k.A.":
        s = "0"
    suffix = " cm"
    if s.endswith(suffix):
        s = s[: -len(suffix)]
    return int(s)


def load_values(filename):
    data = json.load(open(filename))
    values = []
    for name, entry in data.items():
        row = [
            name,
            entry.get("date", 0),
            normalize(entry.get("Schneeh\u00f6he (Talstation)", "0")),
            normalize(entry.get("Schneeh\u00f6he (Bergstation)", "0")),
            normalize(entry.get("Neuschneemenge", "0")),
            entry.get("Schneezustand", ""),
            entry.get("Letzter Schneefall", ""),
        ]
        values.append(row)
    return values


if __name__ == "__main__":
    create_table()
    values = load_values("schneehoehen.json")
    insert(values=values)
    # insert(values=VALUES)
    #dump()
