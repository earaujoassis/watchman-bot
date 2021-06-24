# -*- coding: utf-8 -*-

import argparse

from agents import tasks,  utils


parser = argparse.ArgumentParser(
    description='Agent CLI tool and running instace')
subparsers = parser.add_subparsers(dest='parent')
init_command = subparsers.add_parser(
    'init',
    help='create configuration file for the current user')
notify_command = subparsers.add_parser(
    'notify',
    help='notify master-server and obtain actions to perform')
report_command = subparsers.add_parser(
    'report',
    help='send a report to the master-server')
report_command.add_argument('subject', action='store')
report_command.add_argument(
    'command',
    action='store',
    nargs=argparse.REMAINDER)


class AgentCLI(object):
    def __init__(self, namespace=None):
        self.namespace = namespace

    def get_module_attribute_safely(self, reference, module):
        namespace = self.namespace
        if hasattr(namespace, reference):
            attr = getattr(namespace, reference)
            attrname = attr.replace('-', '_')
            if hasattr(module, attrname):
                return getattr(module, attrname)
        return None

    def get_task_arguments(self):
        args = vars(self.namespace)
        args.pop('parent')
        return args

    def action(self):
        task_function = self.get_module_attribute_safely('parent', tasks)
        if task_function is None:
            utils.print_error('# Command is not implemented yet')
            return
        args = self.get_task_arguments()
        return task_function(**args)

    @staticmethod
    def apply(argv):
        namespace = parser.parse_args(argv[1:])
        return AgentCLI(namespace).action()
