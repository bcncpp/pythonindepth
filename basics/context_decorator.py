import contextlib

run = print

def stop_database():
    run("systemctl stop postgresql.service")

def start_database():
    run("systemctl start postgresql.service")

class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_database()
        return self

    def __exit__(self, ext_type, ex_value, ex_tracebook):
        start_database()

@dbhandler_decorator()
def offline_backup():
    run("pg_dump database")

if __name__ == "__main__":
    offline_backup()