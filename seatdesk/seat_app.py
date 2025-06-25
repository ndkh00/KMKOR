import streamlit as st
from airtable_utils import fetch_seat_data, update_seat
from datetime import datetime
import pytz

# 사용자 리스트
user_names = ["🔴 Check-out", "Key", "Yu Min", "Gi Yoon", "KK", "Chan Wook", "Ji Hee"]
kst = pytz.timezone("Asia/Seoul")

st.title("💺 Office Seating Check-in")

# 좌석 정보 불러오기
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

        # 상태 정보
        is_vacant = occupant == "🔴 Check-out"
        status_text = "Vacant" if is_vacant else "Occupied"
        color = "green" if is_vacant else "red"

        st.markdown(
            f"**Status:** <span style='color:{color}; font-weight:bold'>{status_text}</span>",
            unsafe_allow_html=True
        )

        # 시간만 표시 (라벨 제거)
        st.caption(updated_str)

        # 사용자 선택
        selected = st.selectbox(
            "Select user",
            options=user_names,
            index=user_names.index(occupant) if occupant in user_names else 0,
            key=f"select_{seat_id}"
        )

        # 선택값 변경 시 업데이트
        if selected != occupant:
            update_seat(seat_id, selected)
            st.session_state.seats = fetch_seat_data()
            st.rerun()
