# -*- coding: utf-8 -*-

import os
import tempfile
import requests

from agents.utils import run, safely_load_agent_file, home_dir
from agents.utils import authorization_bearer
from agents.metadata import GITHUB_STRING


MASTER_SERVER_UPDATED       = 0x0000  # noqa: E221
UNREACHABLE_MASTER_LOCATION = 0x0001  # noqa: E221
UPDATE_MASTER_SERVER_LOCKED = 0x0002  # noqa: E221
ACTION_COMPLETED            = 0x0000  # noqa: E221
ACTION_ALREADY_COMPLETED    = 0x0003  # noqa: E221
ACTION_FAILED               = 0x0004  # noqa: E221
ACTION_UNAVAILABLE          = 0x0005  # noqa: E221

WATCHMAN_DEPLOYS_FOLDER = '.watchman-deploys'


class Action(object):
    CREATED = 'created'
    RUNNING = 'running'
    FINISHED = 'finished'
    FAILED = 'failed'


def update_agent(version):
    install_str = GITHUB_STRING.format(version)
    run('pip3 install --user {0}'.format(install_str))


def update_master_server(available_version):
    agent_data = safely_load_agent_file()
    master_location = agent_data['master'].get(
        'location', '/should/not/be/a/valid/path')
    master_location_exists = os.path.exists(master_location)
    if not master_location_exists:
        return UNREACHABLE_MASTER_LOCATION
    os.chdir(master_location)
    if os.path.exists('./lock-deployment'):
        return UPDATE_MASTER_SERVER_LOCKED
    run('touch ./lock-deployment')
    run('git fetch --all')
    run('git checkout tags/{0}'.format(available_version))
    run('bin/deploy.sh -u')
    run('rm -f ./lock-deployment')
    return MASTER_SERVER_UPDATED


def executor(action, agent_data):
    # A001 Deploy
    if action['type'] == 'A001':
        project = action['project_full_name'].split('/', 1)[1]
        # process_name = action['process_name']
        configuration_file_name = action['configuration_file_name'] or ''
        application_id = action['application_id']
        full_path = os.path.join(home_dir(), WATCHMAN_DEPLOYS_FOLDER, project)
        if os.path.exists(full_path):
            return (ACTION_ALREADY_COMPLETED,
                    None,
                    'The application folder already exists; skipped')
        if agent_data.get('github_token', None) is None:
            return (ACTION_FAILED,
                    None,
                    'GitHub token is not available')
        os.chdir(os.path.join(home_dir(), WATCHMAN_DEPLOYS_FOLDER))
        git_url = 'https://{0}@github.com/{1}.git'.format(
            agent_data['github_token'], action['project_full_name'])
        run('git clone {0} {1}'.format(git_url, project))
        os.chdir(full_path)
        if len(configuration_file_name) > 0:
            configuration_file_path = os.path.join(home_dir(),
                                                   WATCHMAN_DEPLOYS_FOLDER,
                                                   project,
                                                   configuration_file_name)
            if os.path.exists(configuration_file_path):
                run('run -f {0}'.format(configuration_file_name))
            with open(configuration_file_path) as configuration_file:
                response = requests.post(
                    '{0}/api/applications/{1}/view/configuration_file'.format(
                        agent_data['watchman_backdoor'],
                        application_id))
                if response.status_code >= 200 and response.status_code < 300:
                    configuration_file.write(response.text)
                else:
                    return (ACTION_FAILED,
                            None,
                            'Could not download configuration file')
        result = run('docker-compose up -d --build')
        return (ACTION_COMPLETED,
                result['stdout'],
                'Successfully completed')
    else:
        return (ACTION_UNAVAILABLE,
                None,
                'Action is not available in the server yet')


def perform_actions(actions):
    agent_data = safely_load_agent_file()
    authorization = authorization_bearer(
        agent_data['client_key'],
        agent_data['client_secret'])
    headers = {'Authorization': 'Bearer {0}'.format(authorization)}
    os.chdir(home_dir())
    run('mkdir -p {0}'.format(WATCHMAN_DEPLOYS_FOLDER))
    for action in actions:
        os.chdir(home_dir())
        if os.path.exists('./lock-action-{0}'.format(action['action_id'])):
            continue
        run('touch ./lock-action-{0}'.format(action['action_id']))
        update_action_url = '{0}/api/applications/{1}/actions/{2}/executor'
        update_action_url = update_action_url.format(
            agent_data['watchman_backdoor'],
            action['application_id'],
            action['action_id'])
        requests.put(update_action_url,
                     headers=headers,
                     json={'action': {'current_status': Action.RUNNING}})
        code, report, reason = executor(action, agent_data)
        status = Action.CREATED
        if code in [Action.ACTION_COMPLETED, Action.ACTION_ALREADY_COMPLETED]:
            status = Action.FINISHED
        elif code != ACTION_UNAVAILABLE:
            status = Action.FAILED
        if report is not None:
            tmpfile = tempfile.NamedTemporaryFile("w")
            tmpfile.write(report)
            tmpfile.flush()
            tmpfile.seek(0)
            requests.put(update_action_url,
                         headers=headers,
                         data={
                             'action[current_status]': status,
                             'action[reason]': reason,
                         },
                         files={
                             'action[report]': open(tmpfile.name),
                         })
        else:
            requests.put(update_action_url,
                         headers=headers,
                         json={
                             'action': {
                                 'current_status': status,
                                 'reason': reason,
                             },
                         })
        os.chdir(home_dir())
        run('rm -f ./lock-action-{0}'.format(action['action_id']))
