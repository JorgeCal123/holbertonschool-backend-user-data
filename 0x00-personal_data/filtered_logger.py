#!/usr/bin/env python3
"""filter logger"""
import re
import logging
from typing import List
import logging
from os import environ
from mysql.connector import connection

PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """method filter datum"""
    msm = message
    for field in fields:
        msm = re.sub(field + "=" + f"[^,{separator}]+",
                             " " + field + "=" + redaction, msm)
    return msm


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """method constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method format"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return logging.Formatter(self.FORMAT).format(record)


def get_db() -> connection.MySQLConnection:
    """
    method get_db that Connect to mysql
    """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    connector = connection.MySQLConnection(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector


def get_logger() -> logging.Logger:
    """ method get logger"""
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_h = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log.setFormatter(formatter)
    log.addHandler(stream_h)

    return log
