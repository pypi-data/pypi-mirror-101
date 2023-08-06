# pytest-rocketchat
Pytest to [RocketChat](https://github.com/RocketChat) reporting plugin.

___Inspired by [pytest-slack](https://pypi.org/project/pytest-slack/) & [pytest-messenger](https://pypi.org/project/pytest-messenger/).___

## Usage
```
$ pytest --rocketchat_server_url=https://your.chat --rocketchat_username=username_or_a_botname --rocketchat_password=passowrord_of_user_or_of_a_bot
```
Options:
- --rocketchat_server_url* (Required)
- --rocketchat_username* (Required)
- --rocketchat_password* (Required)
- --rocketchat_report_link
- --rocketchat_message_prefix
- --rocketchat_timeout
- --rocketchat_success_emoji
- --rocketchat_failed_emoji
- --ssl_verify

## Requirements
- Python >= 3.6

## Installation
You can install "pytest-rocketchat" via [pip](https://pypi.python.org/pypi/pip/):
```
$ pip install pytest-rocketchat
```
If you encounter any problems, please file an [issue](https://github.com/aleksandr-kotlyar/pytest-rocketchat/issues) along with a detailed description.
