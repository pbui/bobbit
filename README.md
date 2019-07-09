# Bobbit

**bobbit** is a simple and modular IRC bot written in [Python].  The current
version uses [Tornado] as its core networking and event processing backend.

The previous ad-hoc version can be found at
[https://bitbucket.org/pbui/bobbit/](https://bitbucket.org/pbui/bobbit/).

## Requirements

- [Python]  3.X
- [Tornado] 4.X
- [PyYAML]

## Configuration
Bobbit requires a configuration YAML file to run, which should be in the
directory specified by `config-dir` (default: `~/.config/bobbit`). An example
config file looks like this:

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
  
## Slack

https://medium.com/@andrewarrow/how-to-get-slack-api-tokens-with-client-scope-e311856ebe9

## Execution
Just run `bobbit.py`. Optionally, you can specify `config-dir`.

[Python]:   https://python.org
[Tornado]:  http://www.tornadoweb.org/en/stable/
[PyYAML]:   http://pyyaml.org/
