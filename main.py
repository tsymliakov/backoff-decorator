import psycopg2
from time import sleep


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """

    :param start_sleep_time: начальное время ожидания
    :param factor: множитель увеличения времени ожидания
    :param border_sleep_time: максимальное время ожидания
    :return: время ожидания в секундах
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            iteration = 0
            curr_sleep_time = start_sleep_time

            while True:
                try:
                    return func(*args, **kwargs)
                except psycopg2.OperationalError:
                    if curr_sleep_time < border_sleep_time:
                        curr_sleep_time = start_sleep_time * factor ** iteration

                    if curr_sleep_time > border_sleep_time:
                        curr_sleep_time = border_sleep_time

                    sleep(curr_sleep_time)

                    iteration += 1
        return wrapper
    return decorator


@backoff(1, 2)
def get_pgconnection(db_name, db_user, password, db_host='localhost', dp_port=5432):
    with psycopg2.connect(f"dbname={db_name} user={db_user} password={password} host={db_host} port={dp_port}") as conn:
        print('Соединение установлено')
        return conn


pg_conn = get_pgconnection('some_db', 'user', '123qwe')
