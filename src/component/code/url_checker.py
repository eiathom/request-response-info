"""
allow a user to enter URL's and receive information on the responsivness \
of that URL
"""

import sys
import urllib2
import json
import re

from constants import URL_REGEX
from constants import NEW_LINE

URL_FORMAT_PATTERN = re.compile(URL_REGEX)


def make_http_url_requests():
    """
    for an entered URL, attempt to make a request and parse the response
    keep looping until no inout is received
    """
    try:
        write_out("enter URL's to get info, to quit press return")
        responses = {}
        while True:
            url_to_use = sys.stdin.readline()
            if url_to_use == NEW_LINE or not url_to_use:
                # no input data recieved from the user, we should exit
                write_out("program exiting")
                if responses:
                    responses_in_program = get_json_dump(responses)
                    sorted(responses_in_program)
                    write_out("count of responses by Status_code")
                    write_out(responses_in_program)
                sys.exit(0)
            # remove trailing newline character from user input data
            url_to_use = url_to_use.rstrip()
            write_out("{}URL entered: '{}'".format(NEW_LINE, url_to_use))
            checked_data = get_checked_url(url_to_use)
            # if the url is valid, we get no error data back
            if not checked_data:
                # valid URL; proceed to make request
                checked_data = get_http_request_response_data(url_to_use)
            # update the responses so far per status code
            if checked_data.has_key('Status_code'):
                update_responses(responses, checked_data['Status_code'])
            json_data = get_json_dump(checked_data)
            write_out(json_data)
    except KeyboardInterrupt:
        # we want to continue running our program
        # we control how to end the program
        pass


def get_checked_url(url_to_use):
    """
    check the url is valid before makng any request
    return error data if the URL is in fact malformed
    """
    if not URL_FORMAT_PATTERN.match(url_to_use):
        write_out("Url '{}', is invalid".format(url_to_use), False)
        return get_error_data(url_to_use, "Invalid URL", True)


def get_json_dump(data):
    """
    get dump of data as JSON
    """
    return json.dumps(data, indent=4, separators=(',', ': '))


def update_responses(responses, data_key):
    """
    update the statuses response number of URL request
    """
    if responses.has_key(data_key):
        responses[data_key] += 1
    else:
        responses[data_key] = 1


def write_out(some_string, is_std_out=True):
    """
    helper function to write to std[out|err]
    """
    if some_string:
        formatted_string = "{}{}".format(some_string, NEW_LINE)
        if not is_std_out:
            sys.stderr.write(formatted_string)
        else:
            sys.stdout.write(formatted_string)


def get_error_data(url_used, message, is_error=False):
    """
    get an error object if request returns an error response
    """
    data = {}
    data['Url'] = url_used
    data_key = 'Error' if is_error else 'Status_code'
    data[data_key] = message
    return data


def get_response_content(response, response_info):
    """
    get content from the request response
    """
    data = {}
    data['Url'] = response.geturl()
    data['Status_code'] = response.getcode()
    data['Content_length'] = response_info.getheader('content-length')
    data['Date'] = response_info.getheader('Date')
    return data


def get_http_request_response_data(url_to_use):
    """
    get http request response data
    """
    response = None
    try:
        request = urllib2.Request(url_to_use)
        response = urllib2.urlopen(request, timeout=10)
        response_info = response.info()
        return get_response_content(response, response_info)
    except Exception as exception:
        return get_handled_exception_response_data(url_to_use, exception)
    finally:
        if response:
            response.close()


def get_handled_exception_response_data(url_to_use, exception):
    """
    handle specific HTTP, URL & common exceptions and return some data
    """
    if isinstance(exception, urllib2.HTTPError):
        write_out(
            "Unable to reach '{}': {} returned"
                .format(url_to_use, exception.code), False)
        return get_error_data(url_to_use, exception.code)
    elif isinstance(exception, urllib2.URLError):
        write_out(
            "Error attempting to reach '{}': {}".format(url_to_use,
                str(exception.reason)), False)
        return get_error_data(url_to_use, "Invalid URL", True)
    else:
        write_out(
            "Error executing request to '{}': {}".format(url_to_use,
                exception.message), False)
        return get_error_data(url_to_use, exception.message, True)


if __name__ == '__main__':
    """
    program entry-point
    """
    make_http_url_requests()
