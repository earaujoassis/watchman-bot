# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import shlex
import socket
import fcntl
import struct
import base64
import json


class ConsoleColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_error(message):
    sys.stderr.write(ConsoleColors.FAIL + message + ConsoleColors.END + '\n')


def print_success(message):
    sys.stdout.write(ConsoleColors.GREEN + message + ConsoleColors.END + '\n')


def print_step(message):
    sys.stdout.write(ConsoleColors.BOLD + message + ConsoleColors.END + '\n')


def call(c, shell=True):
    return subprocess.call(c, shell=shell)


def run(c):
    process = subprocess.Popen(
        shlex.split(c),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    retcode = process.poll()
    return {"retcode": retcode, "stdout": stdout, "stderr": stderr}


def assert_step(r):
    if r != 0:
        sys.stdout.write('> Something went wrong, aborting...\n')
        sys.exit(1)


def get_agent_file_path(die=False):
    agent_options_filepath = os.path.join(home_dir(), '.watchman-agent.json')
    if not os.path.isfile(agent_options_filepath) and die:
        sys.stdout.write('> Missing watchman-agent.json file; exiting\n')
        sys.exit(1)
    return agent_options_filepath


def safely_load_agent_file():
    agent_filepath = get_agent_file_path(die=False)
    agent_file = open(agent_filepath, 'r')
    try:
        agent_data = json.load(agent_file)
        return agent_data
    except:  # noqa: E722
        sys.stdout.write('> Could not load agent file; exiting\n')
        sys.exit(1)


def home_dir():
    return os.path.expanduser("~")


def get_ip_address_for_interface(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    st = struct.Struct('256s')
    try:
        address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            st.pack(ifname[:15].encode('utf-8'))
        )[20:24])
    except OSError:
        address = 'unavailable'
    return address


def authorization_bearer(client_key, client_secret):
    authorization_clear = '{0}:{1}'.format(
        client_key, client_secret).encode('utf-8')
    return base64.b64encode(bytearray(authorization_clear)).decode('utf-8')
