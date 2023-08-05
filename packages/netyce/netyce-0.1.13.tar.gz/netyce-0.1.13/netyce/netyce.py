import base64
import logging
import os
from datetime import date
from typing import AnyStr, Any

import pymysql

_sql_session: Any = None
logger = logging.getLogger('netyce')


def sql_connect(host: str = '127.0.0.1', port: int = 3306, db: str = 'YCE',
                user: str = 'justread', password: AnyStr = None) -> None:
    """To set up the SQL connection

    Args:
        host: the IP or hostname of the node to connect to. ['127.0.0.1']
        port: [3306]
        db: default database to use. ['YCE']
        user: the user to connect with. ['justread']
        password: the password matching the user.

    Returns:
        the pymysql object
    """

    global _sql_session

    if _sql_session:
        return

    password = password or base64.b64decode(os.environ.get(user))  # type: ignore

    connection_dict = {
        'host': host,
        'user': user,
        'port': port,
        'password': password,
        'database': db,
    }
    connection = pymysql.connect(binary_prefix=True, **connection_dict)
    _sql_session = connection.cursor()


def sql_disconnect() -> None:
    global _sql_session
    if _sql_session:
        try:
            _sql_session.close()
        finally:
            _sql_session = None


def sql_query_one(query: str, **kwargs) -> tuple:
    """execute a query and read a single line of output

    Args:
        query: the query to be executed
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple fetched from the database

    """
    sql_connect(**kwargs)
    _sql_session.execute(query)
    return _sql_session.fetchone()


def sql_query_all(query: str, **kwargs) -> tuple:
    """execute a query and read all lines of output

    Args:
        query: the query to be executed
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple of tuples fetched from the database

    """
    sql_connect(**kwargs)
    _sql_session.execute(query)
    return _sql_session.fetchall()


def sql_query_many(query: str, size: int, **kwargs) -> tuple:
    """execute a query and read the desired amount of lines of output

    Args:
        query: the query to be executed
        size: the amount of lines to receive back
        kwargs: args to pass to the sql_connect function

    Returns:
        the tuple of tuples fetched from the database,
        limited on the amount of lines desired

    """
    sql_connect(**kwargs)
    _sql_session.execute(query)
    return _sql_session.fetchmany(size=size)


def init_log(file_level: str = 'WARNING', console_level: str = 'WARNING',
             logfile: str = None) -> None:
    """Initializes the logging for an output file and console.

    Args:
        file_level: One of the options: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
          Fallback value is 'WARNING'
        console_level: One of the options: 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'
          Fallback value is 'WARNING'
        logfile: Provide the complete path to store the logfile. Else cwd with a date.

    Returns:
        nothing.

    Raises:
        nothing.

    """

    global logger
    possible_levels = ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')
    # should be the minimal to control the file and console handler
    # This is not used in another way, since no output is defined.
    logger.setLevel('DEBUG')

    if logfile:
        dir_logfile = os.path.dirname(logfile)
        if dir_logfile:
            os.makedirs(dir_logfile, exist_ok=True)
        path_logfile = logfile
    else:
        path = os.path.join(os.getcwd(), "logs")
        os.makedirs(path, exist_ok=True)
        path_logfile = '%s/%s.log' % (path, date.today())

    file_level = file_level.upper()
    console_level = console_level.upper()

    if file_level not in possible_levels:
        print("LOG LEVEL %r doesnt exist, Fallback is 'WARNING'" % file_level)
        file_level = "WARNING"

    if console_level not in possible_levels:
        print("LOG LEVEL %r doesnt exist, Fallback is 'WARNING'" % console_level)
        console_level = "WARNING"

    fh = logging.FileHandler('%s' % path_logfile)
    fh.setLevel(file_level)
    fh_formatter = logging.Formatter('%(asctime)s %(name)-12s - %(levelname)-8s - %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fh_formatter)

    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    con_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    ch.setFormatter(con_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("log path: %s" % path_logfile)


def _schema_primary_lists(sql_input: tuple) -> tuple:
    """Get the schema information and the primary keys for the given input.

    Args:
        sql_input: A tuple of tuples

    Returns:
        2 lists: schema(list) and primary_key(list)
    """
    pri_list = [sch for sch, pri in sql_input if 'PRI' in pri]
    schema_list = [sch for sch, pri in sql_input]
    return schema_list, pri_list


def sql_schema_primary(table_name: str, database: str = 'YCE', **kwargs) -> tuple:
    """Get the schema information for the given table_name.

    Args:
        table_name: The name of the table you wish to extract the information from
        database: The database, default = YCE

    Returns:
        2 lists: schema(list) and primary_key(list)
    """
    sql = "SELECT column_name, column_key " \
          "FROM information_schema.columns " \
          "WHERE table_schema = %r " \
          "AND table_name = %r" % (database, table_name)
    output = sql_query_all(sql, **kwargs)

    schema_list, pri_list = _schema_primary_lists(output)
    return schema_list, pri_list
