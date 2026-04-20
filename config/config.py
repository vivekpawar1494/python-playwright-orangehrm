import json
import os

ENV = os.getenv("ENV", "QA")

config_path = os.path.join(os.path.dirname(__file__), "environments.json")
with open(config_path) as f:
    env_data = json.load(f)[ENV]

BASE_URL = env_data["base_url"]
BROWSER = env_data["browser"]
TIMEOUT = env_data["timeout"]

# Allow CI to force headless mode via environment variable
# regardless of what environments.json says
_headless_env = os.getenv("HEADLESS", "").lower()
if _headless_env in ("true", "1", "yes"):
    HEADLESS = True
elif _headless_env in ("false", "0", "no"):
    HEADLESS = False
else:
    HEADLESS = env_data["headless"]
