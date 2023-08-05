#!python

import click
from datetime import datetime
import json
import os
import re
import six
import sys

from timeclock.api import cache_project_data, get_user_id, recent_time_entries, submit_time_entries
from timeclock.logs import message_void
from timeclock.config import CONFIG_DIR, get_configuration, set_configuration, get_project_data


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, '__version__'), 'r') as f:
        version = f.read().strip()
    click.echo('Concentric Sky Timeclock Client, version v{}'.format(version))
    ctx.exit()


def process_stdin_content(stdin_iterable):
    """
    Content might be piped as multiple lines or a single string with newlines in it.
    Return a list of lines for parsing.

    TODO: This is gross, and there is surely a better way to do this.
    """
    output = []
    line = ''
    for element in stdin_iterable:
        if isinstance(element, six.string_types) and len(element) == 1:
            if element == '\n':
                output.append(line)
                line = ''
            else:
                line += element
        else:
            output.append(element)

    if len(line):
        output.append(line)  # Catch the last element

    return output


def parse_scheduled_time(schedule_line):
    """
    Takes a schedule line string as input and returns dict representing the duration.
    Does not support events crossing starting and ending on different dates.
    Keys: date, start, finish, duration. Either start & finish or duration is returned
    Example 24hr input: "Scheduled: Sep 20, 2020 at 08:00 to 09:00"
    Example 12hr input: "Scheduled: Sep 20, 2020 at 8:00 AM to 9:00 AM"
    Example output: {"date": "2020-09-20", "start":"08:00:00", "finish":"09:00:00"}
    """
    pattern24 = re.compile(
        r'Scheduled: (?P<date>[^\s]+ \d{1,2}, \d{4}) at (?P<start>\d{1,2}:\d{2}) to (?P<end>\d{1,2}:\d{2})'
    )
    time_strp = '%H:%M'
    pattern12 = re.compile(
        r'Scheduled: (?P<date>[^\s]+ \d{1,2}, \d{4}) at (?P<start>\d{1,2}:\d{2} [AP]M) to (?P<end>\d{1,2}:\d{2} [AP]M)'
    )

    p = pattern24.match(schedule_line)
    if p is None:
        p = pattern12.match(schedule_line)
        time_strp = '%I:%M %p'
    if p is None:
        raise ValueError("Could not parse time entry {}".format(schedule_line))

    date = datetime.strptime(p.group('date'), '%b %d, %Y')
    starttime = datetime.strptime(p.group('start'), time_strp)
    endtime = datetime.strptime(p.group('end'), time_strp)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "start": starttime.strftime("%H:%M:%S"),
        "finish": endtime.strftime("%H:%M:%S")
    }


def parse_event_info(activity_line):
    """
    Takes a project line string as input and returns dict representing the
    project, activity, and ticket and/or note.
    Keys: note, ticket, projectName, activityName. Note and/or ticket will be present.
    Example input "Standup #product/meetings"
    Example output: {"note": "Standup", "ticket": None, "projectName": "product", "activityName": "meetings"}
    """
    parsed = re.match(r'(?P<desc>[^#]+)#(?P<proj>[^\/]+)\/(?P<activity>.+)$', activity_line)
    if parsed is None:
        raise ValueError("Could not parse activity line '{}'".format(activity_line))
    ticket_match = re.match(r'(.+)?(\s|^)(?P<ticket>[A-Za-z]{1,12}\-\d+)(\s|$)', parsed.group('desc'))
    ticket = None if ticket_match is None else ticket_match.group('ticket')

    return {
        "note": parsed.group('desc').strip(),
        "ticket": ticket,
        "projectName": parsed.group('proj').strip(),
        "activityName": parsed.group('activity').strip()
    }


def parse_raw_events(events, project_config, config=None):
    """
    Takes input list of event dicts with projectName and activityName keys
    Returns list of event dicts with project id and activity ids.
    """
    def _match(text, items, item_type='project'):
        for item in items:
            """ Returns item for the first item with a matching name """
            if text.lower() in item['name'].lower():
                return item
        raise ValueError(
            "Could not match {} name '{}' for entry {} #{}/{}".format(
                item_type, text, event['note'], event['projectName'], event['activityName']
            )
        )

    if config is None:
        config = get_configuration()

    output = []
    for event in events:
        ev = event.copy()
        try:
            project = _match(event['projectName'], project_config)
            activity = _match(event['activityName'], project['activities'], 'activity')
        except ValueError as e:
            ev['error'] = str(e)
        else:
            ev['project'] = project['id']
            ev['projectName'] = project['name']
            ev['activity'] = activity['id']
            ev['activityName'] = activity['name']
            ev['user'] = config['user_id']
        output.append(ev)

    return output


def events_from_timelines(timelines, output_callback=message_void):
    """
    Takes input as an iterable of text lines with each time entry split
    across two or more lines and outputs a list of dicts suitable for making requests
    to the timeclock API.
    """
    events = []
    current_event = {}
    for line in timelines:
        try:
            if len(line) and not line.startswith("Location"):
                # Throw away the empty lines and operate on the rest,
                # which are either a title or a scheduled time
                if line.startswith('Scheduled'):
                    current_event.update(parse_scheduled_time(line))
                    events.append(current_event)
                    current_event = {}
                else:
                    current_event.update(parse_event_info(line))
        except ValueError as e:
            current_event['error'] = str(e)

    project_data = get_project_data()

    if not project_data:
        project_data = cache_project_data(output_callback=output_callback)

    if not project_data:
        raise ValueError("Could not obtain project data. Check configuration, run setup and try again.")

    return parse_raw_events(events, project_data)


def filter_project_data(project='', domain='timeclock.concentricsky.com', output_callback=message_void):
    project_data = get_project_data(domain=domain)
    if not project_data:
        output_callback("No project data. Run setup first.")
        return []

    if project:
        project_data = [p for p in project_data if project.lower() in p['name'].lower()]

    return project_data


def summarize_events(events, output_callback=message_void):
    output_callback("Entries prepared for submission:")
    for event in events:
        line1_items = [i for i in (
            event.get('projectName'), event.get('activityName'), event.get('ticket'), event.get('note'),
        ) if i]
        output_callback(": ".join(line1_items))
        output_callback("{} from {} to {}".format(event.get('date'), event.get('start'), event.get('finish')))
        output_callback("")


###
#   Command Line Interface
###


@click.group()
@click.option(
    '--dry-run/--real-run', default=False,
    help="Dry-run to echo request data  without sending it to the server"
)
@click.option(
    '--force/--prompt', default=False,
    help="Skip confirmation prompt"
)
@click.option(
    '--domain', default='timeclock.concentricsky.com',
    help="domain of the timeclock environment, e.g. timeclock.concentricsky.com"
)
@click.option(
    '--version', is_flag=True, callback=print_version,
    expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx, dry_run, force, domain):
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run
    ctx.obj['force'] = force
    ctx.obj['domain'] = domain

    try:
        ctx.obj['config'] = get_configuration(domain)
    except FileNotFoundError:
        api_key = click.prompt(
            "Config not found. Please enter your API key obtained from https://{}/token/ to continue".format(domain)
        )
        if not re.match(r'^[a-z0-9]{40}$', api_key):
            click.echo("Could not interpret api_key from input. Please run 'timeclock setup' to continue.")
            raise click.Abort()

        click.echo("You entered '{}'".format(api_key))
        try:
            user_id = get_user_id(domain=domain, api_key=api_key, output_callback=click.echo)
        except ValueError as e:
            click.echo("Error getting User ID: {}".format(str(e)))

        ctx.obj['config'] = set_configuration(domain=domain, api_key=api_key, user_id=user_id)
        cache_project_data(ctx.obj['domain'], click.echo, config=ctx.obj['config'])

        click.echo("Timeclock is ready to use.")


@cli.command()
@click.pass_context
def setup(ctx):
    """
    Fetch the Project and Activity data and overwrite the local cache.
    """
    cache_project_data(ctx.obj['domain'], click.echo)


@cli.command()
@click.pass_context
def submit(ctx):
    """
    Posts a set of time entries to the Concentric Sky timeclock API.

    Use this event format in your Apple Calendar or text input:
    Event Title #project unique string/activity unique string
    Scheduled: Sep 16, 2020 at 10:00 to 11:00

    Pipe Apple Calendar event data from your clipboard to the program to post.
    `pbpaste | timeclock.py submit`

    Configure your API_KEY in settings_local obtained from https://timeclock.concentricsky.com/token/
    """
    input = process_stdin_content(sys.stdin)

    events = events_from_timelines(input, output_callback=click.echo)
    parse_errors = [e['error'] for e in events if e.get('error') is not None]
    if len(parse_errors):
        click.echo("{} error(s) found. Please correct input and try again:".format(len(parse_errors)))
        for error in parse_errors:
            click.echo(error)
        return
    if not len(events):
        click.echo("No event data could be parsed from input. Aborting.")
        return

    summarize_events(events, output_callback=click.echo)

    if ctx.obj['force']:
        response = 'y'
    else:
        click.echo('Do you want to continue? [y/N]')
        response = click.getchar()
    if response.lower() == 'y':
        results = submit_time_entries(
            events, domain=ctx.obj['domain'], output_callback=click.echo, dry_run=ctx.obj['dry_run']
        )


@cli.command()
@click.pass_context
@click.argument('project', default='')
def projects(ctx, project):
    """
    Prints a list of project names and activity names, optionally filtered.
    """
    project_data = filter_project_data(project)

    if len(project):
        click.echo("List of projects matching keyword '{}':".format(project))
    else:
        click.echo("List of Projects:")

    for project in project_data:
        click.echo('')
        activities = [a.get('name') for a in project['activities']]
        activity_lines = []
        current_line = ''

        for activity in activities:
            if len(current_line) and len(current_line) + len(activity) < 78:
                current_line = ", ".join([current_line, activity])
            elif not len(activity_lines) and not len(current_line):
                current_line = '    - {}'.format(activity)
            else:
                activity_lines.append(current_line)
                current_line = '    - {}'.format(activity)

        activity_lines.append(current_line)

        # * Project Name
        #     - Activity Name 1, Activity Name 2, Activity Name 3
        #     - Activity Name 4, Activity Name 5, Activity Other Name
        click.echo("* {}".format(project['name']))
        for line in activity_lines:
            click.echo(line)


@cli.command()
@click.pass_context
@click.option('--num', type=int, default=None)
def recent(ctx, num):
    """
    Prints a list of the most recently entered date's time entries.

    Pass in a --num option to get some specific number of entries.
    Note that they are returned as most recent day first, earliest in the day first,
    so you might get a partial day's results.
    """
    recent_time_entries(output_callback=click.echo, num=num)


if __name__ == '__main__':
    cli()
