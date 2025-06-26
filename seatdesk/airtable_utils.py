import requests
from datetime import datetime
import pytz
import streamlit as st

# Airtable 시크릿 정보
TOKEN = st.secrets["api_key"]
BASE_ID = st.secrets["base_id"]
TABLE_NAME = st.secrets["table_name"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# 좌석 데이터 불러오기
def fetch_seat_data():
    response = requests.get(AIRTABLE_URL, headers=HEADERS)
    response.raise_for_status()
    records = response.json().get("records", [])

    seat_data = {}
    for record in records:
        fields = record.get("fields", {})
        seat = fields.get("Seat")
        occupant = fields.get("Occupant", "Check-out")
        updated = fields.get("Updated Time", "")
        record_id = record.get("id")

        if seat:
            seat_data[seat] = {
                "occupant": occupant,
                "updated": updated,
                "id": record_id
            }
    return seat_data

# 좌석 상태 업데이트 (단일 PATCH, 권장)
def update_seat(record_id, occupant):
    kst = pytz.timezone("Asia/Seoul")
    now_kst = datetime.now(kst).isoformat()

    patch_url = f"{AIRTABLE_URL}/{record_id}"  # record_id로 PATCH

    data = {
        "fields": {
            "Occupant": occupant,
            "Updated Time": now_kst
        }
    }

 


