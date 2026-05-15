# Stock Tracking and Alerts (small)

A small Python utility to fetch stock quotes from Yahoo Finance and notify users when targets are reached.

Requirements
- Python 3.8+
- requests, yfinance

Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Usage

- Quick check a single symbol:

```bash
python -m src.cli check AAPL
```

- Run a full polling cycle (reads `src/config.json` by default):

```bash
python -m src.cli run --config src/config.json
```

Cron / Scheduled runs

A wrapper script is provided to run under cron: `run_stock_checker.sh`. It activates the virtualenv, loads the config, prevents overlapping runs with a lock, and writes timestamped logs to `logs/`.

Example crontab (run every 2 hours at minute 0):

```cron
0 */2 * * * /Users/xzmao10/code/stock_tracking_and_alerts/run_stock_checker.sh
```

The wrapper uses an absolute path to the project — edit the script to match your installation if needed. The script also supports environment variables for secrets (e.g., Twilio credentials).

Twilio (optional)

To send real SMS messages via Twilio, install the Twilio SDK and set credentials in the environment or in a secure config:

```bash
pip install twilio
export TWILIO_ACCOUNT_SID="AC..."
export TWILIO_AUTH_TOKEN="..."
```

Then configure `src/config.json` to use the `twilio` provider under `notifiers.sms.provider`.

Testing

Run unit tests:

```bash
python -m unittest discover -v
```

Configuration

See `config.sample.json` for a sample configuration. Copy it to `src/config.json` and update values. The runner persists last-notified state to `state.json` by default; change the path in config if desired.
