import contextlib

run = print

def stop_database():
    run("systemctl stop postgresql.service")

def start_database():
    run("systemctl start postgresql.service")

def db_backup():
    run("pg_dump database")

@contextlib.contextmanager
def db_handler():
    try:
        stop_database()
        yield
    finally: 
        start_database()
      
with db_handler():
    db_backup()