import streamlit as st
import requests

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
        occupant = fields.get("SeatUser", "Check-out")
        updated = fields.get("Updated Time", "")
        record_id = record.get("id")

        if seat:
            seat_data[seat] = {
                "occupant": occupant,
                "updated": updated,
                "id": record_id
            }
    return seat_data

# 좌석 상태 업데이트 (SeatUser만 PATCH)
def update_seat(record_id, occupant):
    patch_url = f"{AIRTABLE_URL}/{record_id}"

    data = {
        "fields": {
            "SeatUser": occupant
        }
    }
    print(f"PATCH DATA: {data}")
    response = requests.patch(patch_url, headers=HEADERS, json=data)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("PATCH error:", response.text)
        raise e

# ---------- MAIN APP ----------

st.title("💺 Office Seating App")

# Refresh 버튼
if st.button("🔃 Refresh Now"):
    st.cache_data.clear()
    st.rerun()

# 항상 fresh data 가져오기
seat_data = fetch_seat_data()

# 좌석 데이터 출력
st.write(seat_data)
