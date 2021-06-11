# -*- coding: utf-8 -*-

import sys
import os
import tempfile
import subprocess
import requests
import socket

from pkg_resources import parse_version
from mako.template import Template
from agents.utils import safely_load_agent_file, get_agent_file_path
from agents.utils import get_ip_address_for_interface
from agents.utils import authorization_bearer
from agents.metadata import VERSION
from agents import actions


def init():
    watchman_backdoor = ""
    client_key = ""
    client_secret = ""

    print("> All right, let's initiate an agent instance")
    while len(watchman_backdoor) == 0:
        watchman_backdoor = input(
                "What is the base URL for the Watchman-Backdoor server: ") \
            .strip() \
            .rstrip("/")
    while len(client_key) == 0:
        client_key = input(
                "What is the client key for that backdoor server: ") \
            .strip()
    while len(client_secret) == 0:
        client_secret = input(
                "And what is the client secret for that backdoor server: ") \
            .strip()

    agent_file_path = get_agent_file_path(die=False)
    with open(agent_file_path, 'w') as agent_file:
        current_project_path = os.path.dirname(__file__)
        template_filepath = os.path.join(
            current_project_path,
            'templates',
            'watchman-agent.json')
        template = Template(filename=template_filepath)
        template_render = template.render(**{
            'watchman_backdoor': watchman_backdoor,
            'client_key': client_key,
            'client_secret': client_secret,
        })
        agent_file.write(template_render)


def notify():
    agent_data = safely_load_agent_file()
    authorization = authorization_bearer(
        agent_data['client_key'],
        agent_data['client_secret'])
    response = requests.put('{0}/api/servers/notify'.format(
        agent_data['watchman_backdoor']),
        headers={
            'Authorization': 'Bearer {0}'.format(
                authorization),
        },
        json={
            'server': {
                'hostname': socket.gethostname(),
                'ip': get_ip_address_for_interface('eth0'),
                'latest_version': VERSION,
            },
        })
    if response.status_code >= 200 and response.status_code < 300:
        sys.stdout.write('> Successfully notified\n')
        remote_data = response.json()
        # 1. Update the agent binary if a new version is available
        if parse_version(remote_data['version']) > parse_version(VERSION):
            sys.stdout.write('> Version mismatch; updating agent\n')
            actions.update_agent(remote_data['version'])
            sys.stdout.write('> Agent updated\n')
        else:
            sys.stdout.write('> No update available\n')
        # 2. Update the master server if:
        #  2.a a new tag/version is available (from GitHub releases/tags);
        #  2.b the master location is available
        available_version = remote_data['available_tag']
        current_version = 'v{0}'.format(remote_data['version'])
        is_master_container = agent_data.get('master', None) is not None
        is_there_a_mismatch = current_version != available_version
        if is_there_a_mismatch and is_master_container:
            sys.stdout.write(
                '> A new master server version is available; updating\n')
            result = actions.update_master_server(available_version)
            if result is actions.UNREACHABLE_MASTER_LOCATION:
                sys.stdout.write(
                    '> The master location is unreachable; skipping\n')
            if result is actions.UPDATE_MASTER_SERVER_LOCKED:
                sys.stdout.write('> Deployment locked; skipping\n')
            if result is actions.MASTER_SERVER_UPDATED:
                sys.stdout.write('> Successfully deployed\n')
        else:
            sys.stdout.write('> No new tag available; skipping\n')
        # 3. Perform pending actions
        pending_actions = remote_data['pending_actions']
        if len(pending_actions) > 0:
            sys.stdout.write('> Performing actions\n')
            actions.perform_actions(pending_actions)
            sys.stdout.write('\n> Actions completed\n')
        sys.exit(0)
    else:
        sys.stdout.write('> Oops! Notification failed\n')
        sys.stdout.write('> Error: {0}\n'.format(response.content))
        sys.exit(1)


def report(subject, command):
    agent_data = safely_load_agent_file()
    authorization = authorization_bearer(
        agent_data['client_key'],
        agent_data['client_secret'])
    headers = {'Authorization': 'Bearer {0}'.format(authorization)}

    # 1. Create a new report and receive an ID to upload file
    response = requests.post('{0}/api/servers/report'.format(
        agent_data['watchman_backdoor']),
        headers=headers,
        json={
            'server': {
                'hostname': socket.gethostname(),
                'ip': get_ip_address_for_interface('eth0'),
                'latest_version': VERSION,
            },
            'report': {
                'subject': subject,
            },
        })

    if response.status_code >= 200 and response.status_code < 300:
        remote_data = response.json()
    else:
        sys.stdout.write('> Oops! Report failed\n')
        sys.stdout.write('> Error: {0}\n'.format(response.content))
        sys.exit(1)

    # 2. Upload the file with the report data
    report_id = remote_data['report']['id']
    message_body = subprocess.Popen(
        command, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    tmpfile = tempfile.NamedTemporaryFile("w")
    tmpfile.write(message_body)
    tmpfile.flush()
    tmpfile.seek(0)

    response = requests.put('{0}/api/servers/report/{1}'.format(
        agent_data['watchman_backdoor'],
        report_id),
        headers=headers,
        files={
            'report[body]': open(tmpfile.name),
        })

    if response.status_code >= 200 and response.status_code < 300:
        sys.stdout.write('> Successfully reported\n')
        sys.exit(0)
    else:
        sys.stdout.write('> Oops! Report failed\n')
        sys.stdout.write('> Error: {0}\n'.format(response.content))
        sys.exit(1)
