#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from agents.cli import AgentCLI
from agents.metadata import VERSION, NAME  # noqa: F401


def main():
    code = AgentCLI.apply(sys.argv)
    sys.exit(code)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
