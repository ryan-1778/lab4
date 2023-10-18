#!/usr/bin/env python3

from hashlib import sha1
import os
import sqlite3
import sys

def main():
    if not os.path.isfile('database.db'):
        print("Cannot find database.db in current working directory")
        sys.exit(1)

    if len(sys.argv) != 3:
        print("Usage: %s <username> <password>" % os.path.basename(sys.argv[0]))
        sys.exit(1)

    username, password = sys.argv[1:3]

    con = sqlite3.connect('database.db')
    cur = con.cursor()

    try:
        cur.execute("SELECT username,length FROM users WHERE username='%s' AND password='%s'" % (
                username, sha1(password.encode('ascii')).hexdigest()))
    except:
        print("Internal error")
        sys.exit(1)

    res = cur.fetchone()

    if res is None:
        print("Access denied")
        sys.exit(2)

    if len(res[0]) != res[1]:
        print("Internal error")
        sys.exit(1)

    print("Welcome, %s." % res[0])

    con.commit()
    con.close()

if __name__ == '__main__':
    main()
