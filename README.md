<h1 align="center">Lighthouse Garden</h1>

<p align="center"><img src="./assets/tower.svg" alt="Lighthouse" width="150">
</p>

Aggregate a performance overview for various target pages using the [lighthouse](https://github.com/GoogleChrome/lighthouse) service. 

## Install/Config

```bash
# Copy/edit config.json
mv config.json.dist config.json
```

Adding target pages

```json
{
    "title": "Google",
    "identifier": "google",
    "url": "https://google.com"
}
```

Starting the container

```bash
# Start DDEV container
ddev start
```

Open `http://lighthouse-garden.ddev.site/`

## Usage

```bash
# Connect into the container
ddev ssh
```

```bash
# Run python script
python illuminate.py
```

```bash
# Options
-h, --help          Show help
-v, --verbose       Enable console output
-e, --export        Exporting stored data to a web page
-g, --gardening     Fetching data by the lighthouse service
-s, --not-saved     Disable the persistence of received data
-c, --config        Path to config file
-ep, --exportpath   Path to export files
-u, --url           Providing an URL to check
-n, --run           Number of runs
-p, --performance   Only measure performance data
```

Register optionally a cronjob for regulary updates

```bash
0 5 * * * python /var/www/html/illuminate.py -v 1 -g 1 -e 1
```

## Credits

- performance analysis by [lighthouse](https://github.com/GoogleChrome/lighthouse)
- graph visualization by [plot.ly](https://plot.ly/javascript/)
- icon made by [freepik](https://www.flaticon.com/authors/freepik)

*ToDo: Further documentation*