import streamlit as st
import requests

# Airtable secrets
TOKEN = st.secrets["api_key"]
BASE_ID = st.secrets["base_id"]
TABLE_NAME = st.secrets["table_name"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# 🔍 좌석 정보 가져오기
def fetch_seat_data():
    response = requests.get(AIRTABLE_URL, headers=HEADERS)
    response.raise_for_status()
    records = response.json().get("records", [])

    seat_data = {}
    for record in records:
        fields = record.get("fields", {})
        seat = fields.get("Seat")
        occupant = fields.get("Occupant", "🔴 Check-out")
        updated = fields.get("Updated Time", "")
        if seat:
            seat_data[seat] = {
                "occupant": occupant,
                "updated": updated
            }
    return seat_data

# ✏️ 좌석 정보 업데이트
def update_seat(seat_id, occupant):
    query = {
        "filterByFormula": f"{{Seat}} = '{seat_id}'"
    }
    get_response = requests.get(AIRTABLE_URL, headers=HEADERS, params=query)
    get_response.raise_for_status()
    records = get_response.json().get("records", [])

    if records:
        record_id = records[0]["id"]
        data = {
            "fields": {
                "Seat": seat_id,
                "Occupant": occupant
            }
        }
        patch_url = f"{AIRTABLE_URL}/{record_id}"
        patch_response = requests.patch(patch_url, headers=HEADERS, json=data)
        patch_response.raise_for_status()
