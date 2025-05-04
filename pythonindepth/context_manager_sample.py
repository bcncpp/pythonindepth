import contextlib

run = print

def stop_database():
    run("systemctl stop postgresql.service")

def start_database():
    run("systemctl start postgresql.service")

class DBHandler:
    def __enter__(self) -> 'DBHandler':
        stop_database()
        return self
    def __exit__(self, exc_type, ex_value, ex_traceback):
        start_database()

def db_backup():
    run ("pg_dump database")

def main():
    with DBHandler():
        db_backup()

if __name__ == "__main__":
    main()