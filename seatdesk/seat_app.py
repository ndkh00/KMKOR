import streamlit as st
from airtable_utils import fetch_seat_data, update_seat
from datetime import datetime
import pytz

# 사용자 리스트
user_names = ["🔴 Check-out", "Key", "Yu Min", "Gi Yoon", "KK", "Chan Wook", "Ji Hee"]
kst = pytz.timezone("Asia/Seoul")

st.title("💺 Office Seating Check-in")

# 좌석 정보 가져오기
if "seats" not in st.session_state:
    st.session_state.seats = fetch_seat_data()

cols = st.columns(4)
for idx, (seat_id, data) in enumerate(sorted(st.session_state.seats.items())):
    occupant = data["occupant"]
    updated_raw = data["updated"]

    # 한국 시간으로 변환
    try:
        updated_dt = datetime.fromisoformat(updated_raw.replace("Z", "+00:00")).astimezone(kst)
        updated_str = updated_dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        updated_str = "N/A"

    col = cols[idx % 4]
    with col:
        st.markdown(f"### {seat_id}")
        color = "green" if occupant == "🔴 Check-out" else "red"
        display_name = "Vacant" if occupant == "🔴 Check-out" else occupant

        st.markdown(
            f"**Status:** <span style='color:{color}; font-weight:bold'>{display_name}</span>",
            unsafe_allow_html=True
        )
        st.caption(f"🕒 Last updated: {updated_str}")

        selected = st.selectbox(
            "Select user",
            options=user_names,
            index=user_names.index(occupant) if occupant in user_names else 0,
            key=f"select_{seat_id}"
        )

        if selected != occupant:
            update_seat(seat_id, selected)
            st.session_state.seats = fetch_seat_data()
            st.rerun()