from datetime import datetime, timedelta
import json
import requests

from timeclock.logs import get_logger, message_void
from timeclock.config import get_configuration, set_configuration, get_project_data, set_project_data



def get_request_headers(domain='timeclock.concentricsky.com', config=None):
    if config is None:
        config = get_configuration(domain=domain)

    return {
        'Authorization': 'Token {}'.format(config['api_key']),
        'Accept': 'application/json'
    }


def cache_project_data(domain='timeclock.concentricsky.com', output_callback=message_void, config=None):
    if config is None:
        config = get_configuration(domain)

    output = []
    projects_url = 'https://{}/api/v1/project/'.format(domain)
    output_callback("Requesting project data from {}".format(projects_url))

    response = requests.get(projects_url, headers=get_request_headers(config=config), allow_redirects=False)
    output_callback("Response status {}: {} chars".format(response.status_code, len(response.content)))
    if response.status_code != 200:
        output_callback("Failed with Error:")
        output_callback(response.content[0:1000])
        return

    try:
        project_data = response.json()
    except (ValueError, json.decoder.JSONDecodeError, TypeError) as e:
        output_callback("Error decoding projects response from {}".format(projects_url))
        output_callback(response.content[0:1000])
        raise e

    set_project_data(project_data, domain=domain, output_callback=output_callback)

    return project_data


def get_user_id(domain='timeclock.concentricsky.com', api_key=None, output_callback=message_void):
    if api_key is None:
        raise ValueError("API key required to continue.")

    request_url = 'https://{}/api/v1/timeentry/'.format(domain)
    response = requests.get(request_url, headers=get_request_headers(config={'api_key': api_key}))
    if response.status_code != 200:
        output_callback("Unexpected API Response {}: '{}'".format(
            response.status_code, response.content[0:200].decode('utf-8')
        ))
        raise ValueError("Could not obtain user id with domain and API key.")

    data = response.json()
    if len(data['results']) == 0:
        raise ValueError("Enter at least one time entry manually on website before using this utility.")

    return data['results'][0]['user']


def recent_time_entries(domain='timeclock.concentricsky.com', output_callback=message_void, num=None):
    request_url = 'https://{}/api/v1/timeentry/'.format(domain)
    response = requests.get(request_url, headers=get_request_headers())

    if response.status_code != 200:
        output_callback("Unexpected API Response {}: '{}'".format(
            response.status_code, response.content[0:200].decode('utf-8')
        ))
        return

    output_callback("Latest {} timeclock entries:".format(num or "day's"))
    try:
        data = response.json()
    except json.decoder.JSONDecodeError:
        output_callback("Could not parse recent time entries API response.")
        output_callback("Unexpected API Response {}: '{}'".format(
            response.status_code, response.content[0:200].decode('utf-8')
        ))

    if not len(data['results']):
        output_callback("No entries found.")

    first_date = datetime.strptime(data['results'][0]['date'], "%Y-%m-%d").strftime("%a %b %d")
    entry_count = 0
    for entry in data['results']:
        date = datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%a %b %d")
        if num is None and date != first_date or num is not None and entry_count >= num:
            break

        try:
            timestring = entry['start'][0:5]
        except TypeError:
            duration = timedelta(minutes=entry['duration'])
            timestring = "( {}h{}m )".format(duration.seconds//3600, (duration.seconds//60)%60)
        output_callback(
            "  - {} {} - {} {}".format(date, timestring, entry.get('note', ''), entry.get('ticket', ''))
        )
        entry_count += 1


def submit_time_entries(entries, domain='timeclock.concentricsky.com', output_callback=message_void, dry_run=False):
    request_url = 'https://{}/api/v1/timeentry/'.format(domain)

    processed_count = 0
    processed_entries = []
    logger = get_logger()
    logger.begin()
    output_callback('Submitting {} time entries to {}'.format(len(entries), request_url))

    def _do_entry(entry):
        endline = ',\n' if len(entries) > (1 + processed_count) else '\n'
        if dry_run is False:
            output_callback("Submitting entry: {}...".format(entry.get('note', entry.get('ticket', ''))), nl=False)
            response = requests.post(request_url, data=entry, headers=get_request_headers())
            if response.status_code == 201:
                logger.write(response.content.decode('utf-8') + endline)
                output_callback("Success")
                response_data = response.json()
            else:
                output_callback("Got unexpected status {}: {}".format(
                    response.status_code, response.content[0:200].decode('utf-8')
                ))
                try:
                    response_data = {}
                    response_data['error'] = response.json()
                    response_data['post_data'] = entry
                    response_data['status'] = response.status_code
                except (TypeError, ValueError):
                    response_data = entry.copy()
                    response_data['error'] = response.content
                    response_data['status'] = response.status_code
                logger.write(json.dumps(response_data) + endline)
        else:
            output_callback("DRY RUN. Not submitting entry: {}".format(entry.get('note', entry.get('ticket', ''))))
            response_data = entry.copy()
            response_data['error'] = "DRY RUN. Not Submitted."
            log.write(json.dumps(response_data) + endline)
        return response_data

    try:
        for entry in entries:
            processed_entry = _do_entry(entry)
            processed_count += 1
            processed_entries.append(processed_entry)
    except Exception as e:
        log.write(str(e))
        return
    finally:
        logger.close()

    return processed_entries
