# Bobbit

**bobbit** is a simple and modular *asynchronous* IRC / Slack bot written in
[Python].  The current version uses [asyncio] as its core networking and event
processing backend.

## Requirements

- [Python]  3.6+
- [PyYAML]
- [aiohttp]

## Configuration

Bobbit requires a configuration YAML file (`bobbit.yaml`) to run, which should
be in the directory specified by `config-dir` (default: `~/.config/bobbit`). An
example config file looks like this:

```
nick:       "bobbit"
password:   <password>
owners:
    - <owner>
host:       <irc server>
port:       6667
channels:
    - <channel>
```

The following modules also require configuration files (in `config-dir`):

- lookup: requires `lookup.yaml`. Here's an example:

  ```
  cool kids:
  - I wish that I could be like the cool kids \\ 'Cause all the cool kids, they seem to fit in
  ```

- weather: requires `weather.yaml`. Here's an example:

  ```
  appid:      <api-key>
  default:    <zipcode>
  ```

### Slack

TODO: Describe how to get Slack token.

https://medium.com/@andrewarrow/how-to-get-slack-api-tokens-with-client-scope-e311856ebe9

## Execution

To start the the bot, run `bin/bobbit`:

```
$ ./bin/bobbit -h
usage: bobbit [--config-dir CONFIG_DIR] [--log-path LOG_PATH] [--debug]
              [--local] [-h]

Simple Asynchronous IRC/Slack Bot

optional arguments:
  --config-dir CONFIG_DIR  Configuration directory (default: ~/.config/bobbit)
  --log-path LOG_PATH      Path to log file (default: None)
  --debug                  Enable debug logging (default: False)
  --local                  Enable local client (default: False)
  -h, --help               Show this help message and exit
```

**Note**: The *local* client (ie. `--local`) allows you to test the modules
directly in the terminal by using *standard input* rather than connecting to an
actual IRC or Slack network.

[Python]:   https://python.org
[PyYAML]:   http://pyyaml.org/
[aiohttp]:  https://docs.aiohttp.org/en/stable/
[asyncio]:  https://docs.python.org/3/library/asyncio.html


### Docker

You can also start application using docker:

Building container

```
docker build --no-cache -t 'bobbit' .
```

Running:

```
docker run -it bobbit
```

You can pass args to application directly, also you can mount your config file using docker volumes, for example:

```
docker run -v /my-config-dir:/tmp/my-config-dir bobbit --config-dir /tmp/config-dir
```

And change default user with using --env argument, for example:

```
docker run -e USER=MYFANCYUSER bobbit --config-dir /tmp/config-dir
```