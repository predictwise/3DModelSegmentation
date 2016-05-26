__author__ = 'wlw'
import sqlite3
import numpy as np
import io


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

if __name__ == '__main__':
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)

    x = np.arange(12).reshape(2, 6)

    con = sqlite3.connect("/home/wlw/oliverProjects/3DClassification/classification.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cur.execute("create table test (arr array)")

    # With this setup, you can simply insert the NumPy array with no change in syntax:

    cur.execute("insert into test (arr) values (?)", (x, ))
    con.commit()
    # And retrieve the array directly from sqlite as a NumPy array:

    cur.execute("select arr from test")
    data = cur.fetchone()[0]

    print(data)
    # [[ 0  1  2  3  4  5]
    #  [ 6  7  8  9 10 11]]
    print(type(data))
    # <type 'numpy.ndarray'>