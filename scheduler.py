"""
Daily Cadence Scheduler for TimberCraft Automation
Enforces strict anti-bot cadence:
- Slot 1: 05:30 AM IST (8:00 PM EDT prev day / 00:00 UTC)
- Slot 2: 09:30 PM IST (12:00 PM EDT / 16:00 UTC)
- Anti-Bot Jitter: Automated random +1 to +10 minute delay
"""

import time
import random
import argparse
import sys
from datetime import datetime, timedelta
import zoneinfo
from typing import Tuple

# UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from queue_manager import QueueManager
from config import AUDITED_ACCOUNTS

# Daily Slots in IST (India Standard Time)
SLOT_1_IST_HOUR = 5   # 05:30 AM IST (8:00 PM EDT prev day / 00:00 UTC)
SLOT_1_IST_MIN = 30

SLOT_2_IST_HOUR = 21  # 09:30 PM IST (12:00 PM EDT / 16:00 UTC)
SLOT_2_IST_MIN = 30

TZ_EDT = zoneinfo.ZoneInfo("America/New_York")
TZ_IST = zoneinfo.ZoneInfo("Asia/Kolkata")


class DailyScheduler:
    def __init__(self):
        self.qm = QueueManager()

    def get_current_times(self) -> Tuple[datetime, datetime]:
        """Returns current time in EDT and IST."""
        now_utc = datetime.now(zoneinfo.ZoneInfo("UTC"))
        now_edt = now_utc.astimezone(TZ_EDT)
        now_ist = now_utc.astimezone(TZ_IST)
        return now_edt, now_ist

    def get_next_upload_slot(self) -> Tuple[datetime, str, int]:
        """
        Calculates next upload slot (Slot 1 or Slot 2) with 1-10 min random anti-bot jitter.
        Returns: (target_time_ist, slot_name, jitter_minutes)
        """
        _, now_ist = self.get_current_times()
        today = now_ist.date()

        # Slot 1 today (05:30 AM IST)
        slot1 = datetime(today.year, today.month, today.day, SLOT_1_IST_HOUR, SLOT_1_IST_MIN, tzinfo=TZ_IST)
        # Slot 2 today (09:30 PM IST)
        slot2 = datetime(today.year, today.month, today.day, SLOT_2_IST_HOUR, SLOT_2_IST_MIN, tzinfo=TZ_IST)

        jitter_min = random.randint(1, 10)

        if now_ist < slot1:
            target = slot1 + timedelta(minutes=jitter_min)
            return target, "Slot 1 (Morning - 05:30 AM IST)", jitter_min
        elif now_ist < slot2:
            target = slot2 + timedelta(minutes=jitter_min)
            return target, "Slot 2 (Night - 09:30 PM IST)", jitter_min
        else:
            # Tomorrow Slot 1
            tomorrow = today + timedelta(days=1)
            target = datetime(tomorrow.year, tomorrow.month, tomorrow.day, SLOT_1_IST_HOUR, SLOT_1_IST_MIN, tzinfo=TZ_IST) + timedelta(minutes=jitter_min)
            return target, "Slot 1 (Tomorrow Morning - 05:30 AM IST)", jitter_min

    def print_status(self):
        now_edt, now_ist = self.get_current_times()
        next_slot_ist, slot_name, jitter = self.get_next_upload_slot()
        next_slot_edt = next_slot_ist.astimezone(TZ_EDT)
        wait_seconds = (next_slot_ist - now_ist).total_seconds()
        wait_hours = wait_seconds / 3600.0

        print("=" * 80)
        print("[*] TIMBERCRAFT GOLDEN SCHEDULE STATUS")
        print("=" * 80)
        print(f"- Current Time (US Eastern EDT): {now_edt.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
        print(f"- Current Time (India IST)     : {now_ist.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
        print("-" * 80)
        print(f"- Next Target Slot             : {slot_name}")
        print(f"- Scheduled Run Time (EDT)     : {next_slot_edt.strftime('%Y-%m-%d %I:%M:%S %p')}")
        print(f"- Scheduled Run Time (IST)     : {next_slot_ist.strftime('%Y-%m-%d %I:%M:%S %p')}")
        print(f"- Anti-Bot Organic Jitter      : +{jitter} minutes added")
        print(f"- Countdown Remaining          : {wait_hours:.2f} hours ({int(wait_seconds)} seconds)")
        print("-" * 80)
        pending = self.qm.list_queue()
        print(f"- Queued Videos Ready          : {len(pending)} pending items")
        for idx, item in enumerate(pending[:3], 1):
            print(f"  {idx}. [{item['account']}] {item['title_theme']} (ID: {item['item_id']})")
        print("=" * 80)

    def run_daemon(self):
        """Continuous background daemon that executes jobs exactly at target slots."""
        print("[*] Starting TimberCraft Scheduler Daemon...")
        while True:
            now_edt, _ = self.get_current_times()
            next_slot_edt, slot_name, jitter = self.get_next_upload_slot()
            wait_sec = (next_slot_edt - now_edt).total_seconds()

            print(f"[*] Sleeping for {wait_sec/3600.0:.2f} hours until {slot_name}...")
            time.sleep(min(wait_sec, 300))  # Heartbeat every 5 mins or sleep full duration

            now_edt, _ = self.get_current_times()
            if now_edt >= next_slot_edt:
                print(f"[!] Golden Slot Triggered: {slot_name}")
                # Execute next pending queue item
                item = self.qm.get_next_pending()
                if item:
                    print(f"[*] Processing Queue Item: {item['title_theme']} ({item['item_id']})")
                    # In full integration, calls pipeline.py or uploader.py
                else:
                    print("[!] No pending items in queue. Waiting for next batch.")
                time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TimberCraft Daily US Timezone Scheduler")
    parser.add_argument("--status", action="store_true", help="Display current schedule status and next slot")
    parser.add_argument("--daemon", action="store_true", help="Run background scheduler daemon")
    args = parser.parse_args()

    scheduler = DailyScheduler()
    if args.daemon:
        scheduler.run_daemon()
    else:
        scheduler.print_status()
