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
        occupant = fields.get("SeatUser", "Check-out")   # 바뀐 컬럼명
        updated = fields.get("Updated Time", "")
        record_id = record.get("id")

        if seat:
            seat_data[seat] = {
                "occupant": occupant,
                "updated": updated,
                "id": record_id
            }
    return seat_data

# 좌석 상태 업데이트 (에러시 콘솔 로그, 예외전파)
def update_seat(record_id, occupant):
    kst = pytz.timezone("Asia/Seoul")
    now_kst = datetime.now(kst).isoformat()
    patch_url = f"{AIRTABLE_URL}/{record_id}"

    data = {
        "fields": {
            "SeatUser": occupant,             # 바뀐 컬럼명
            "Updated Time": now_kst
        }
    }
    print(f"PATCH DATA: {data}")
    response = requests.patch(patch_url, headers=HEADERS, json=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("PATCH error:", response.text)
        raise e
