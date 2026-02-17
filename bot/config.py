"""Bot configuration — loads environment variables."""

import os
from dotenv import load_dotenv

# Load from /etc/gg-hookah/.env
load_dotenv("/etc/gg-hookah/.env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DOMAIN = os.getenv("DOMAIN", "gghookah.delivery")

# Mini App URL (used for WebApp buttons)
# Until DNS+SSL are ready, use IP-based URL
MINI_APP_URL = "https://gghookah.delivery"

# Fallback: if no domain with SSL, bot WebApp button won't work
# TODO: set real HTTPS URL once SSL is configured