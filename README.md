# Web Load Testing with Locust

This project contains an initialization template for load and performance testing your website/web service using [Locust](https://locust.io/).

## Project Structure

- [`locustfile.py`](file:///home/fauzan/Projects/Locust/locustfile.py): Main Locust test script defining user behaviors, HTTP requests, weights, and hooks.
- [`locust.conf`](file:///home/fauzan/Projects/Locust/locust.conf): Default settings (target host, users count, spawn rate, test duration).
- [`requirements.txt`](file:///home/fauzan/Projects/Locust/requirements.txt): Python dependencies.

---

## Getting Started

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Load Tests

### Mode A: Interactive Web UI (Recommended for Exploration)

1. Start Locust:
   ```bash
   locust
   ```
2. Open your browser and navigate to: **[http://localhost:8089](http://localhost:8089)**
3. Specify your Target Host (e.g. `https://your-website.com`), Number of Users, and Spawn Rate, then click **Start Swarming**.

---

### Mode B: Headless (CLI / CI-CD Mode)

Run automated load tests without the UI and generate an HTML report:

```bash
locust --headless \
  --host https://your-website.com \
  -u 50 \
  -r 5 \
  -t 2m \
  --html report.html
```

*Flags breakdown:*
- `-u 50`: 50 simulated concurrent users.
- `-r 5`: Spawn rate (5 new users per second).
- `-t 2m`: Test duration (2 minutes).
- `--html report.html`: Export performance charts and stats into an HTML report.

---

### Mode C: Filter by Tags

Execute only specific types of tasks:

```bash
# Run only read/GET tasks
locust --tags read

# Run only write/POST tasks
locust --tags write
```

---

## Customizing Test Scenarios

Edit [`locustfile.py`](file:///home/fauzan/Projects/Locust/locustfile.py) to add your custom user workflows:

- **Change wait time**: Adjust `wait_time = between(1.0, 3.0)` to simulate real user think time.
- **Authentication**: Add login requests inside `on_start()` and attach authorization tokens to `self.client.headers`.
- **Custom endpoints**: Add new `@task(weight)` methods with `self.client.get()` or `self.client.post()`.
- **Response assertions**: Use `with self.client.get(..., catch_response=True) as response:` to validate response bodies and status codes.
