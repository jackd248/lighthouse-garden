# Lighthouse garden

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

## Update data

```bash
# Run python script
ddev exec web python generate.py
```

Register optionally a cronjob for regulary updates

```bash
0 5 * * * python /var/www/html/generate.py
```

*ToDo: Further documentation*