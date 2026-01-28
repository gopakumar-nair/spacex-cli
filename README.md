# SpaceX Launch Data CLI

A Python command-line tool to fetch and analyze SpaceX launch data from the [SpaceX API](https://api.spacexdata.com/v4/launches).

## Requirements

- Python 3.x
- Internet connection (for initial API fetch)


## Usage

### Basic Syntax

```bash
python3 spacex.py --action <action_name> [options]
```

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--action` | string | Yes | - | Action to perform. Choices: `report`, `payloads`, `launchpads` |
| `--cache` | string | No | `./cache/launches.json` | Path to cache file for storing API data |
| `--refresh` | flag | No | - | Force refresh from API, bypass cache |
| `--verbose` | flag | No | - | Enable verbose debug logging |



## Examples

### Basic Usage

Generate a report with default settings:
```bash
python3 spacex.py --action report
```

### With Verbose Logging

Enable detailed debug logging to see the data processing flow:
```bash
python3 spacex.py --verbose --action report
```

### Force Refresh from API

Bypass cache and fetch fresh data from the API:
```bash
python3 spacex.py --refresh --action report
```

### Custom Cache Location

Use a custom cache file location:
```bash
python3 spacex.py --cache ./cache/launches.json --verbose --action report
```

### Payloads Analysis

Calculate average payloads per launch:
```bash
python3 spacex.py --action payloads
```

### Launchpads Analysis

Group launches by launchpad:
```bash
python3 spacex.py --action launchpads
```


## Exit Codes

After calling spacex.py use the following command to see exit code or use the --verbose flag.
```bash
echo $?  
```

The script exits with the following codes:
- `0`: Success
- `1`: Timeout error
- `2`: Non-200 HTTP response
- `3`: Unexpected error

## Caching

By default, the script caches API responses to reduce network calls. The cache is stored in `./cache/launches.json` (or your specified path). 

- Cache is automatically used if the file exists and `--refresh` is not specified
- Use `--refresh` to force a fresh API call
- Cache directory is created automatically if it doesn't exist

## Verbose Mode

When `--verbose` is enabled, you'll see detailed debug logs including:
- Data fetching operations (cache vs API)
- Filter application and results
- Action execution details
- HTTP retry attempts and status codes
- Error details

## Notes

- The script currently filters launches for the year **2022** by default
- Missing or invalid dates are skipped during filtering
- Missing payloads are treated as zero in payload calculations
- The script uses a 15-second HTTP timeout with 1 retry attempt
- Retries are automatically attempted for HTTP status codes 404 and 503
