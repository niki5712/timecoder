# timecoder
The utility to generate timestamps for the last YouTube stream based on information from the site https://www.streamersonglist.com/.

## How to build
### Requirements
* Python 3.11.0

```shell
pip install -r requirements.txt
pyinstaller --clean --onefile --python-option u src\timecoder.py
```

## How to use
```shell
timecoder [<TWITCH_CHANNEL_NAME>]
```
You can also set the environment variable `TWITCH_CHANNEL_NAME` to avoid passing an argument to the utility.
