
[![pipeline status](https://gitlab.com/mediatech15/python-postx/badges/main/pipeline.svg)](https://gitlab.com/mediatech15/python-postx/-/commits/main) 
[![coverage report](https://gitlab.com/mediatech15/python-postx/badges/main/coverage.svg)](https://gitlab.com/mediatech15/python-postx/-/commits/main)
[![PyPI version](https://badge.fury.io/py/python-postx.svg)](https://badge.fury.io/py/python-postx)

# Python PostX

PostX is a package that provides a simple interface for posting messages to multiple platforms.
The user has the ability to send the same message to multiple services or to an indivdual service. 
The same message is translated to the appropriate calls for the each platform.

Full Docs: [Here](https://mediatech15.gitlab.io/python-postx/)

## Getting Started

Installing via pip

`pip install python-postx`

## Quick Start

```python
from postx import Broker
from postx.message import Message

# Create the broker
broker = Broker()

# You can register as many endpoints as you wish of any combination
broker.register('slack', 'your slack webhook url')
broker.register('teams', 'your teams webhook url')

# Make your message
message = Message()
message.title('My Awesome Update')
message.sub_title('This is an awesome update')
message.text('The update is for all people to see and affects everything')
message.list_unordered(['item 1', 'item 2'])
message.link('Read More Here', 'link to more information')

# Or a shorter way
message = Message()
message.title('My Awesome Update')
    .sub_title('This is an awesome update')
    .text('The update is for all people to see and affects everything')
    .list_unordered(['item 1', 'item 2'])
    .link('Read More Here', 'link to more information')

# Or even shorter
message = Message()
message.title('My Awesome Update')
    .sub('This is an awesome update')
    .text('The update is for all people to see and affects everything')
    .ul(['item 1', 'item 2'])
    .link('Read More Here', 'link to more information')

# Send the message to all
broker.send(message)

# Send the message to slack only
broker.send_single_service(message, 'slack')

# Send the message to a single endpoint
broker.send_single_link(message, 'your registered endpoint url')
```

## Supported targets

- Microsoft Teams
- Slack

## Meta

Kyle Mason - [Mediatech15 - Gitlab](https://gitlab.com/mediatech15)

Distributed under the MIT license. See LICENSE for more information.