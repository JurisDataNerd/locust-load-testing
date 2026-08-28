import json
import logging
from locust import HttpUser, task, between, tag, events

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("locust-test")


class WebsiteUser(HttpUser):
    """
    Simulates a user browsing and interacting with the target website/API.
    """
    # Think time between tasks: random wait between 1 and 3 seconds
    wait_time = between(1.0, 3.0)

    # Optional default target host (can be overridden via CLI, web UI, or locust.conf)
    host = "https://example.com"

    def on_start(self):
        """
        Executed when a simulated user starts.
        Ideal for login, setting auth tokens, or session setup.
        """
        logger.info("New simulated user spawned. Initializing session...")
        # Example: Set common request headers
        self.client.headers.update({
            "User-Agent": "LocustLoadTest/1.0",
            "Accept": "application/json, text/html, */*",
        })
        
        # Example: Mock authentication (uncomment & adapt if needed)
        # response = self.client.post("/api/auth/login", json={"username": "user1", "password": "password"})
        # if response.status_code == 200:
        #     token = response.json().get("token")
        #     self.client.headers["Authorization"] = f"Bearer {token}"

    def on_stop(self):
        """
        Executed when a simulated user stops / is removed.
        Ideal for logout or cleanup.
        """
        logger.info("Simulated user shutting down.")

    @tag("read", "home")
    @task(3)
    def load_homepage(self):
        """
        Loads the homepage with weight 3 (runs 3x more frequently than weight 1 tasks).
        """
        with self.client.get("/", name="[Page] Home", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code {response.status_code}")

    @tag("read", "browse")
    @task(2)
    def browse_endpoint(self):
        """
        Simulates browsing an endpoint or performing a search query.
        """
        params = {"query": "test", "page": 1}
        with self.client.get("/search", params=params, name="[API] Search", catch_response=True) as response:
            if response.status_code in (200, 404):
                # Valid response (even empty results)
                response.success()
            else:
                response.failure(f"Search failed with code {response.status_code}")

    @tag("write", "submit")
    @task(1)
    def submit_data(self):
        """
        Simulates submitting a form or sending a POST request with payload.
        """
        payload = {
            "title": "Performance Test Item",
            "body": "Automated load test entry",
            "userId": 1
        }
        with self.client.post(
            "/api/items",
            json=payload,
            name="[API] Create Item",
            catch_response=True
        ) as response:
            if response.status_code in (200, 201):
                response.success()
            elif response.status_code == 404:
                # If endpoint does not exist yet on test server, avoid false alarms in demo
                response.failure("Endpoint /api/items not found (404)")
            else:
                response.failure(f"POST request failed: {response.text}")


# --- Optional Event Listeners for Custom Metrics / Logging ---

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("=== Load test run is starting ===")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("=== Load test run has completed ===")
