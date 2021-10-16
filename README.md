# pi_temp_monitoring

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Remotely monitoring the temperature on a Raspberry Pi and recieve warnings if the temperature exceeds a limit via a matrix-element client. Basically the pi texts you if it gets hot.


## Set up

Run the following commands:

```zsh
cd pi_temp_monitoring
```
```zsh
pip install -r requirements.txt
```

to install the necessary packages in order for the scripts to run.

As far as the [matrix-element](https://element.io/) client; I recommend creating 2 accounts. The first account being your own personal account that you can use to sign in in your phone for example, and another account that will be the bot account. This will allow you to create a room that the aforementioned will join, such that they can text each other. The account credentials that are needed for the script if this is followed, are the bot account credentials.

The credentials should be in environment variables. An example files is included in `creds`.
After this is filled in (in the same directory), run:

```zsh
source creds
```

## Usage

```zsh
python3 monitor.py
```

for normal runs,

```zsh
python3 monitor.py -h
```

for usage details, or

```zsh
python3 monitor.py -l 90 # or python3 monitor.py --limit=90
```

to set a limit. If no limit is provided it defaults to 80.
