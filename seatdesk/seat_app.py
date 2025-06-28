import streamlit as st
from airtable_utils import fetch_seat_data, update_seat
from datetime import datetime
import pytz

user_names = ["🔓Check-out", "Ki-Mac", "Chan Wook", "Ji Hee", "Superman", "Jong Ho"]
kst = pytz.timezone("Asia/Seoul")

st.markdown("""
    <style>
    div[data-baseweb="select"] div {
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER + REFRESH BUTTON ----------
col1, col2 = st.columns([6, 1])

with col1:
    st.title("💺 Office Check-In")
    st.image("f34.jpg", use_container_width=True)

with col2:
    if st.button("🔃 Refresh Now"):
        # 캐시 비우고 데이터 새로 불러오기
        st.session_state.seats = fetch_seat_data()
        st.rerun()

# ---------- LOAD SEAT DATA ----------
if "seats" not in st.session_state:
    st.session_state.seats = fetch_seat_data()

floor_map = {
    "4층": [f"4{zone}-{str(i).zfill(2)}" for zone in ["A", "B"] for i in range(1, 7)],
    "3층": [f"3{zone}-{str(i).zfill(2)}" for zone in ["A", "B"] for i in range(1, 7)],
}

# 행(row)로 좌석을 4개씩 잘라서 출력
def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

for floor_name, seat_ids in floor_map.items():
    st.subheader(f"📍 {floor_name}")
    for row in chunk_list(seat_ids, 4):
        cols = st.columns(4)
        for idx, seat_id in enumerate(row):
            data = st.session_state.seats.get(seat_id, {
                "occupant": "🔓Check-out",
                "updated": "",
                "id": None
            })
            occupant = data["occupant"]
            updated_raw = data["updated"]
            record_id = data["id"]

            try:
                updated_dt = datetime.fromisoformat(updated_raw.replace("Z", "+00:00")).astimezone(kst)
                updated_str = updated_dt.strftime("%m-%d %H:%M")
            except Exception:
                updated_str = "N/A"

            is_vacant = occupant == "🔓Check-out"
            color = "green" if is_vacant else "red"
            status_icon = "🟢" if is_vacant else "🔴"

            with cols[idx]:
                st.markdown(
                    f"<span style='font-weight:bold; font-size:16px'>[{seat_id}]</span> "
                    f"<span style='color:{color}; font-weight:bold; font-size:16px'>{status_icon}</span> "
                    f"<span style='color:gray; font-size:12px'>{updated_str}</span>",
                    unsafe_allow_html=True
                )

                selected = st.selectbox(
                    label="Seat User Selector",
                    options=user_names,
                    index=user_names.index(occupant) if occupant in user_names else 0,
                    key=f"select_{seat_id}",
                    label_visibility="collapsed"
                )

                if selected != occupant and record_id:
                    try:
                        update_seat(record_id, selected)
                        st.session_state.seats = fetch_seat_data()
                        st.rerun()
                    except Exception as e:
                        st.error(f"좌석 업데이트 중 오류 발생: {e}")
