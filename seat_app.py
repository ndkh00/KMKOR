import streamlit as st

# 예시 사용자 리스트 (맨 앞에 "🔴 Check-out" 옵션 추가)
user_names = ["🔴 Check-out", "Key", "Yu Min", "Gi Yoon", "KK", "Chan Wook", "Ji Hee"]

# 초기 좌석 상태
if 'seats' not in st.session_state:
    st.session_state.seats = {f"{row}{col}": "🔴 Check-out"
                              for row in ['A', 'B', 'C', 'D']
                              for col in range(1, 5)}

st.title("💺 Office Seating Check-in App (Name Select)")

cols = st.columns(4)
for idx, (seat_id, occupant) in enumerate(st.session_state.seats.items()):
    col = cols[idx % 4]
    with col:
        st.markdown(f"### {seat_id}")

        is_vacant = occupant == "🔴 Check-out"
        color = "green" if is_vacant else "red"
        display_name = "Vacant" if is_vacant else occupant

        st.markdown(
            f"**Status:** <span style='color:{color}; font-weight:bold'>{display_name}</span>",
            unsafe_allow_html=True
        )

        # 이름 선택 드롭다운
        selected_name = st.selectbox(
            f"Select user",
            options=user_names,
            index=user_names.index(occupant) if occupant in user_names else 0,
            key=f"select_{seat_id}"
        )

        # 상태가 바뀌었을 때만 갱신
        if selected_name != occupant:
            st.session_state.seats[seat_id] = selected_name
            st.rerun()
