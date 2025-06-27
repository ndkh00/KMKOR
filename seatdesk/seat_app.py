import streamlit as st
from airtable_utils import fetch_seat_data, update_seat
from datetime import datetime
import pytz
import os

# -------------------------------
# 사전 정의
# -------------------------------

# 사용자 목록
user_names = ["🔓Check-out", "Ki-Mac", "Chan Wook", "Ji Hee", "Superman", "Jong Ho"]

# KST timezone
kst = pytz.timezone("Asia/Seoul")

# Selectbox 글자 크기 CSS
st.markdown("""
    <style>
    div[data-baseweb="select"] div {
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💺 Office Check-in")

# -------------------------------
# 최초 실행 시 좌석 데이터 불러오기
# -------------------------------

if "seats" not in st.session_state:
    st.session_state.seats = fetch_seat_data()

# -------------------------------
# 층별 좌석 목록 정의
# -------------------------------

floor_map = {
    "4층": [f"4{zone}-{str(i).zfill(2)}" for zone in ["A", "B"] for i in range(1, 7)],
    "3층": [f"3{zone}-{str(i).zfill(2)}" for zone in ["A", "B"] for i in range(1, 7)],
}

# -------------------------------
# 층별 이미지 경로 정의
# -------------------------------

floor_images = {
    "4층": "4F.PNG",
    "3층": "3F.PNG"
}

# -------------------------------
# 리스트를 n개씩 자르는 함수
# -------------------------------

def chunk_list(lst, n):
    """리스트를 n개씩 잘라서 반환"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# -------------------------------
# 층별 출력
# -------------------------------

for floor_name, seat_ids in floor_map.items():
    st.subheader(f"📍 {floor_name}")

    # ---------------------------
    # 해당 층의 이미지 출력
    # ---------------------------
    img_path = floor_images.get(floor_name)
    
    if img_path and os.path.exists(img_path):
        # 작은 크기로 표시 (가로 300픽셀로 고정)
        st.image(img_path, width=300)
    else:
        st.warning(f"{floor_name} 이미지가 존재하지 않거나 경로가 잘못되었습니다.")

    # ---------------------------
    # 좌석 배치 출력
    # ---------------------------
    for row in chunk_list(seat_ids, 4):  # 4개씩 끊어 표시
        cols = st.columns(4)

        for idx, seat_id in enumerate(row):
            # 좌석 데이터 가져오기
            data = st.session_state.seats.get(seat_id, {
                "occupant": "🔓Check-out",
                "updated": "",
                "id": None
            })

            occupant = data["occupant"]
            updated_raw = data["updated"]
            record_id = data["id"]

            # 시간 변환
            try:
                updated_dt = datetime.fromisoformat(updated_raw.replace("Z", "+00:00")).astimezone(kst)
                updated_str = updated_dt.strftime("%m-%d %H:%M")
            except Exception:
                updated_str = "N/A"

            # 상태 색상 결정
            is_vacant = occupant == "🔓Check-out"
            color = "green" if is_vacant else "red"
            status_icon = "🟢" if is_vacant else "🔴"

            with cols[idx]:
                # 좌석 정보 출력
                st.markdown(
                    f"<span style='font-weight:bold; font-size:16px'>[{seat_id}]</span> "
                    f"<span style='color:{color}; font-weight:bold; font-size:16px'>{status_icon}</span> "
                    f"<span style='color:gray; font-size:12px'>{updated_str}</span>",
                    unsafe_allow_html=True
                )

                # 사용자 선택 UI
                selected = st.selectbox(
                    label="Seat User Selector",
                    options=user_names,
                    index=user_names.index(occupant) if occupant in user_names else 0,
                    key=f"select_{seat_id}",
                    label_visibility="collapsed"
                )

                # 선택 변경 시 업데이트
                if selected != occupant and record_id:
                    try:
                        update_seat(record_id, selected)
                        st.session_state.seats = fetch_seat_data()
                        st.rerun()
                    except Exception as e:
                        st.error(f"좌석 업데이트 중 오류 발생: {e}")

