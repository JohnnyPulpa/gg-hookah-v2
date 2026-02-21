"""Seed default settings from Section 6.11 of the spec."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://gg_hookah:Benxow-ziqpir-1duqbi@localhost/gg_hookah"

DEFAULTS = [
    ("work_days", "3,4,5,6,0", "Working days: 0=Sun..6=Sat. Wed-Sun"),
    ("work_start", "18:00", "Opening time (Asia/Tbilisi)"),
    ("work_end", "02:00", "Closing time (crosses midnight)"),
    ("timezone", "Asia/Tbilisi", "Business timezone"),
    ("late_order_cutoff_time", "01:30", "Orders after this are LATE"),
    ("after_hours_disable_time", "02:00", "No extensions/rebowls after this"),
    ("base_bowl_price", "70", "Base hookah price GEL"),
    ("rebowl_price", "50", "New bowl price GEL"),
    ("deposit_amount", "100", "Cash deposit GEL"),
    ("session_duration", "120", "Session duration minutes"),
    ("rebowl_duration", "120", "Rebowl extension minutes"),
    ("free_extension", "60", "Free return extension minutes"),
    ("free_extension_max_uses", "1", "Max free extensions per order"),
    ("drinks_enabled", "true", "Enable drinks add-on"),
    ("drinks_max_total_qty", "8", "Max total drinks per order"),
    ("discount_hookah_only", "true", "Discount applies to hookah only"),
    ("promo_enabled", "true", "Enable promo codes"),
    ("promo_per_phone_limit", "1", "Max uses of same promo per phone"),
    ("pause_orders", "false", "Pause new orders"),
    ("pause_reason_text", "", "Reason shown when paused"),
    ("board_games_enabled", "true", "Show board games promo"),
    ("board_games_available_now", "true", "Board games in stock"),
    ("passport_retention_days", "365", "Days to keep passport photos"),
    ("default_language", "ru", "Default language for new users"),
    ("total_hookahs", "5", "Total hookah units in inventory"),
    ("max_hookahs_regular", "3", "Max hookahs per regular order"),
    ("max_hookahs_event", "5", "Max hookahs per event order"),
]

def seed():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        for key, value, desc in DEFAULTS:
            conn.execute(text(
                "INSERT INTO settings (key, value, description, updated_at) "
                "VALUES (:k, :v, :d, now()) ON CONFLICT (key) DO NOTHING"
            ), {"k": key, "v": value, "d": desc})
        conn.commit()
    print(f"Seeded {len(DEFAULTS)} default settings.")

if __name__ == "__main__":
    seed()
