import requests
import json
from requests.adapters import ConnectionError
import datetime

MAX_URI_LEN = 8192
USER_AGENT = 'python-neutron-sks'


# ENDPOINT_URL = u'http://bkcloud12:9696'


class LogSummary:
    def __init__(self, info_number, warning_number, error_number, debug_number, other_number, total_number):
        self.info_number = info_number
        self.warning_number = warning_number
        self.error_number = error_number
        self.debug_number = debug_number
        self.other_number = other_number
        self.total_number = total_number


def request(url, method, body=None, headers=None, **kwargs):
    """Request without authentication."""

    content_type = kwargs.pop('content_type', None) or 'application/json'
    headers = headers or {}
    headers.setdefault('Accept', content_type)

    if body:
        headers.setdefault('Content-Type', content_type)

    headers['User-Agent'] = USER_AGENT
    try:
        resp = requests.request(
            method,
            url,
            data=body,
            headers=headers,
            # verify=self.verify_cert,
            # timeout=self.timeout,
            **kwargs)
    except:
        raise ConnectionError
    return resp, resp.text


# def get_nova_log_summary(keystone_token, endpoint, date_from, date_to):
def get_nova_log_summary(endpoint, date_from, date_to):
    method = "GET"
    if date_from != "unspecified":
        start_date = date_from.strftime('%Y:%m:%d-%H:%M:%S')
    else:
        start_date = date_from
    if date_to != "unspecified":
        end_date = date_to.strftime('%Y:%m:%d-%H:%M:%S')
    else:
        end_date = date_to
    # body = {"start_date": start_date, "end_date": end_date}
    # header = {'X-Auth-Token': keystone_token}
    endpoint += "?start_date=" + start_date + "&end_date=" + end_date
    try:
        resp, reply_body = request(endpoint, method, body={})

        status_code = resp.status_code
        if status_code in (requests.codes.ok,
                           requests.codes.created,
                           requests.codes.accepted,
                           requests.codes.no_content):
            data = json.loads(reply_body)
            return LogSummary(data['info_number'], data['warning_number'], data['error_number'],
                              data['debug_number'], data['other_number'], data['total_number'])
        else:
            return "error"
    except ConnectionError:
        return "Connection to Server has broken"


def get_date_from_input(date_input):
    if date_input is None:
        return None
    elif not date_input:
        return "none"
    else:
        try:
            return datetime.datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            return None


class DateError(Exception):
    pass


class LogTypeError(Exception):
    pass


def get_nova_logs_count_by_day(endpoint, log_type, start_date, end_date):
    log_types = ('info', 'debug', 'error', 'warning', 'other', 'all')
    method = "GET"
    if log_type not in log_types:
        raise LogTypeError(" log type is not in correct format ")
    date_from = get_date_from_input(start_date)
    date_to = get_date_from_input(end_date)
    if date_from is None or date_to is None:
        raise DateError("invalid input!")
    if isinstance(date_from, datetime.date) and isinstance(date_to, datetime.date) and date_from > date_to:
        return DateError("date from must be smaller than date to")
    # body = {"start_date": start_date, "end_date": end_date}
    # header = {'X-Auth-Token': keystone_token}
    endpoint += "?log_type=" + log_type + "start_date=" + start_date + "&end_date=" + end_date
    try:
        resp, reply_body = request(endpoint, method, body={})
        status_code = resp.status_code
        if status_code in (requests.codes.ok,
                           requests.codes.created,
                           requests.codes.accepted,
                           requests.codes.no_content):
            data = json.loads(reply_body)
            return LogSummary(data['info_number'], data['warning_number'], data['error_number'],
                              data['debug_number'], data['other_number'], data['total_number'])
        else:
            return "error"
    except ConnectionError:
        return "Connection to Server has broken"
