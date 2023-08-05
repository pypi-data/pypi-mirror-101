import json
import os

from timeclock.logs import message_void

CONFIG_DIR = os.path.join(os.path.expanduser("~"), '.timeclock')


def get_configuration(domain='timeclock.concentricsky.com'):
    """
    Reads configuration from user home directory.
    Raises FileNotFoundError if missing.
    Raises TypeError if configuration file is corrupted.
    Raises KeyError if required values are missing.
    """
    with open(os.path.join(CONFIG_DIR, 'configuration.{}.json'.format(domain)), 'r') as f:
        data = json.loads(f.read())

    # Ensures required values are present.
    return {
        'domain': domain,
        'api_key': data['api_key'],
        'user_id': data['user_id']
    }


def set_configuration(domain='timeclock.concentricsky.com', **kwargs):
    data = kwargs.copy()
    data['domain'] = domain
    output = json.dumps(data, indent=4)

    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    with open(os.path.join(CONFIG_DIR, 'configuration.{}.json').format(domain), 'w') as f:
        f.truncate()
        f.write(output)

    return data


def get_project_data(domain='timeclock.concentricsky.com', output_callback=message_void):
    filename = os.path.join(CONFIG_DIR, 'cached_projects.{}.json'.format(domain))
    try:
        with open(filename, 'r') as f:
            return json.loads(f.read())
    except (json.decoder.JSONDecodeError, TypeError, ValueError, IOError,):
        return None


def set_project_data(project_data, domain='timeclock.concentricsky.com', output_callback=message_void):
    filename = os.path.join(CONFIG_DIR, 'cached_projects.{}.json'.format(domain))
    with open(filename, 'w') as f:
        f.truncate()
        f.write(json.dumps(project_data, indent=4))

    output_callback("Stored project data in {}".format(filename))
