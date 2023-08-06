# ProBot.DB
### ProBot embed messages feature based database, lol.

Store your data in ProBot database easily, using the embed messages feature, for free :).

## Installation

pip install ProBotDB

## Usage
Now all you need is a server ID with ProBot, and your auth token from probot.io.
```py
from ProbotDB import ProBotDB

database = ProBotDB('auth token', 'server ID', 'embed name')

database.set('foo', 'bar')
database.get('foo') # bar
database.push('foo', 'ok')
database.delete('foo')
database.clear()
```