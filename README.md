# Development
## Loading `.env` file
Adding *Poetry* plugin to load `.env` file: visit [here](https://stackoverflow.com/questions/67107007/how-do-i-set-an-environment-variable-dynamically-when-using-poetry-shell).


## Starting the app
The app can be started with the following command
```shell
python -m com.dkgndianko.telegram.bot.web_relay.entry_point
```

## Common tasks
### Remove pycache directories
Use this command to remove *Pycache* directories
```shell
find . -type d -name __pycache__ -exec rm -rf {} \;
```