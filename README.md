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

Just run `bobbit.sh`:

```
$ ./bobbit.sh -h 
usage: bobbit [--config-dir CONFIG_DIR] [--log-path LOG_PATH] [--debug] [-h]

Simple Asynchronous IRC/Slack Bot

optional arguments:
  --config-dir CONFIG_DIR  Configuration directory
  --log-path LOG_PATH      Path to log file (default: disabled)
  --debug                  Enable debug logging (default: disabled)
  -h, --help               Show this help message and exit
```

[Python]:   https://python.org
[PyYAML]:   http://pyyaml.org/
[aiohttp]:  https://docs.aiohttp.org/en/stable/
[asyncio]:  https://docs.python.org/3/library/asyncio.html
