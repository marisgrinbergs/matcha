
import sqlite3
import sys
import os
from typing import List, Dict

import random
import string
from typing import List
from matcha_app.zemail import *
from matcha_app.security_ import *


from fields import *
import json
import inspect

import matcha_app.file_paths

class SqlCmds:

    __ = {
    'sqlite' : {
                    #'fetch' = "SELECT profile FROM users WHERE profile LIKE {}" #'%email={}%' || '%email={}%'
                    'fetch_profile' : 'SELECT profile FROM users WHERE email="{}"',
                    'fetch_all': 'SELECT profile FROM users',
                    'insert' : "INSERT INTO users ('{}') VALUES ('{}')",
                    'add_col' : 'ALTER TABLE {} ADD {} {}',
                    'create_table' : "CREATE TABLE {} ('id' INTEGER PRIMARY KEY AUTOINCREMENT)",
                    'delete_row' : "DELETE FROM {} WHERE {}='{}'",
                    'update' : 'UPDATE users SET profile="{}" WHERE email="{}"'
                }
    }


class SQLite:
    """there must be a connexion for every thread, use cont.manag."""
    def __init__(self, file=file_paths.sqlitefile):
        self.file = file
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, type, value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
        #print(f'closed instance db connection!')


def init_db(dbname='sqlite'):
    if dbname == 'sqlite':
        db_exec('create_table', {'table': 'users'}, 'sqlite')
        db_exec('create_table', {'table': 'users', 'field': 'email', 'type': 'TEXT'}, 'sqlite')
        db_exec('create_table', {'table': 'users', 'field': 'profile', 'type': 'TEXT'}, 'sqlite')


def db_exec(action, data:'{email:dct}', dbname='sqlite') -> Dict[str, str]:
    """
        -writes in log
        -converts json to str for db ; reverse for return
    """
    if 'profile' in data:
        data['profile'] = json.dumps(data['profile']) #dct to str

    cmd = SqlCmds.__[dbname][action].format(*data.values())

    with open(file_paths.generallog, 'w+') as f:
        print(f'{dbname} >> {cmd} \n', file=f)
    db_to_file(file_paths.dblivetxt)

    if dbname == 'sqlite':
        with SQLite() as cur:
            cur.execute(cmd)
            res = cur.fetchall()
            res = [json.loads(r['profile']) for r in res] #convert str to dct
            return res


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#########################

#{'birthdate':'03/05/95', 'first_name':'natsirt'}
def get_profiles(data):
    all_profiles = db_exec('fetch_all', {}, 'sqlite')
    return (p for p in all_profiles if data <= p)

def profile_exists(email):
    return len(db_exec('fetch_profile', {'email': email}, 'sqlite')) == 1

def stock_profiles(ps):
    for p in ps:
        if len(db_exec('fetch_profile', {'email': p['email']}, 'sqlite')) == 0:
            db_exec('insert', {'email': p['email']}, 'sqlite')
            db_exec('insert', {'profile': p}, 'sqlite')
        else:
            db_exec('update', {'profile': p}, 'sqlite')


def create_profiles(master_seed):

    nb_users = 10
    min_seed = 0#(nb_users * master_seed)
    max_seed = 99999#min_seed + nb_users

    profiles = []  # to put into db list of dicts
    seed_nbs = (random.randint(0,99999) for _ in range(nb_users))
    emails = (Email.random_(seednb) for seednb in seed_nbs)
    fields = inspect.getmembers(sys.modules['fields'], inspect.isclass)

    for seed_nb, email in zip(seed_nbs, emails):
        profile = dict()
        for clsname, clsobj in fields.items():
            if clsname != 'Email':
                if clsobj.random.__code__.co_argcount == 2:
                    profile[clsobj.lowercase()] = clsobj.random_(emails, seed_nb)
                else:
                    profile[clsobj.lowercase()] = clsobj.random_(seed_nb)
        profiles.append(profile)
    return profiles


def load_db(dbname, what):
    if dbname == 'sqlite':
        ps = []
        if what == 'random':
            ps = create_profiles(0)
        if what == 'fake':
            ps = json.load(file_paths.fakedb)

            for p in ps:
                db_exec('insert', {'email': p['email']}, 'sqlite')
                db_exec('insert', {'profile': p}, 'sqlite')


# DISPLAY FUNS
def print_profile(profile, file=None):
    top = bottom = '-' * 50
    print(top, file=file)
    for k, v in profile.items():
        print(f'<{k}>'.center(15, '*'), file=file)
        if isinstance(v, list):
            for i, e in enumerate(v):
                print(f'    {i} > {e}', file=file)
        elif isinstance(v, dict):
            for a, b in v.items():
                print(f'    {a} > {b}', file=file)
        else:
            print(f'    {v}', file=file)
    print(bottom, file=file)


def db_to_file(dbfile=None):
    with open(dbfile, 'w+') as f:
        for pro in db_exec('fetch_all', {}, 'sqlite'):
            print_profile(pro, f)
















