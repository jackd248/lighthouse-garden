# Lighthouse garden

Aggregate [lighthouse](https://github.com/GoogleChrome/lighthouse) performance data on predefined targets. 

## Install/Config

```bash
# Start DDEV container
ddev start
```

```bash
# Copy/edit config.json
mv config.json.dist config.json
```

## Update data

```bash
# Run python script
python generate.py
```

Open `http://lighthouse-garden.ddev.site/`

*ToDo*