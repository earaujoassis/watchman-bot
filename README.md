# Watchman (Bot or Agents) [![Build Status](https://travis-ci.com/earaujoassis/watchman-bot.svg?branch=master)](https://travis-ci.com/earaujoassis/watchman-bot)

> Watchman helps to keep track of automating services; a tiny bot

## Robots

Robots are running processes inside continuous integration services. They create actions to be
performed by the Watchman Server or Watchman Agents.

```sh
$ docker build -t earaujoassis/watchman-bot .
$ docker run -i --rm --name bot --env WATCHMAN_BOT_BASE_URL=${BOT_URL} --env WATCHMAN_BOT_CLIENT_KEY=${BOT_KEY} --env WATCHMAN_BOT_CLIENT_SECRET=${BOT_SECRET} earaujoassis/watchman-bot:latest ci help
```

## Agents

Agents are running services inside each deployable server. They listen to the Watchman-Backdoor
server in order to receive instructions for deployment, for instance.

### Installing & Running

This is a Python `pip` package, so you're able to `pip install` it in your work environment. Basically,
it will make available an `agent` binary, which should be helpful to setup new projects and deploy
them in that running space (a server).

```sh
$ pip install --user https://github.com/earaujoassis/watchman/archive/v0.2.4.zip
```

If you need any help, please run `agent --help`.

### Developing agents (under tools)

In order to create a sandbox (virtual environment) and install it for development or testing, you may
run the following commands:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .
$ agent --help
```

The `agent` binary will be available in the current shell session.

## Issues

Please take a look at [/issues](https://github.com/earaujoassis/watchman/issues)

## License

[MIT License](http://earaujoassis.mit-license.org/) &copy; Ewerton Assis
