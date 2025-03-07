import streamlit as st
import pandas as pd
from datetime import datetime

# 제목
st.title("OT Reporting Tool")

# 파일명
FILE_NAME = "work_log.csv"

# 날짜 선택
selected_date = st.date_input("Select Date", datetime.today())

# 근무 일지 입력
work_log = st.text_area("Working Description")

# 현재 시간 기록 (초 제외)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# 30분 단위 OT 시간 선택
ot_start_time = st.select_slider(
    "Select Start Time",
    options=[f"{hour:02d}:{minute:02d}" for hour in range(6, 24) for minute in [0, 30]],
    value="18:00"  # 기본값 18시
)

ot_end_time = st.select_slider(
    "Select End Time",
    options=[f"{hour:02d}:{minute:02d}" for hour in range(6, 24) for minute in [0, 30]],
    value="20:00"  # 기본값 20시
)

# 데이터프레임 불러오기 또는 생성
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    # 최초 데이터프레임 생성 시 칼럼 이름을 정확히 지정
    df = pd.DataFrame(columns=["Date", "Work Log", "Start Time", "End Time", "Created At", "Updated At", 
                               "Updated Work Log", "Updated Start", "Updated End"])


# 저장 버튼
if st.button("Save"):
    if work_log:
        # 선택한 날짜의 로그가 이미 있는지 확인
        existing_log = df[df["Date"] == str(selected_date)]

        if not existing_log.empty:
            # 기존 로그 업데이트 (OT 시작/종료 시간은 그대로 두고, 변경된 내용만 업데이트)
            df.loc[df["Date"] == str(selected_date), ["Updated Work Log", "Updated Start", "Updated End", "Updated At"]] = [work_log, ot_start_time, ot_end_time, current_time]
            st.success("근무 일지가 업데이트되었습니다.")
        else:
            # 새로운 로그 추가 (최초로 OT Start/End Time을 기록)
            new_log = pd.DataFrame({
                "Date": [selected_date],
                "Work Log": [work_log],
                "Start Time": [ot_start_time],
                "End Time": [ot_end_time],
                "Created At": [current_time],
                "Updated At": [current_time],
                "Updated Work Log": [""],  # 최초 입력 시 업데이트된 Work Log는 빈 문자열
                "Updated Start": [""],  # 최초 입력 시 업데이트된 Start Time은 빈 문자열
                "Updated End": [""],   # 최초 입력 시 업데이트된 End Time은 빈 문자열
            })
            df = pd.concat([df, new_log], ignore_index=True)
            st.success("근무 일지가 저장되었습니다.")

        # CSV 파일로 저장
        df.to_csv(FILE_NAME, index=False)
    else:
        st.warning("근무 일지를 입력하세요.")

# 삭제 버튼
if st.button("Delete"):
    df = df[df["Date"] != str(selected_date)]
    df.to_csv(FILE_NAME, index=False)
    if df.empty:
        st.warning("삭제할 근무 일지가 없습니다.")
    else:
        st.success("근무 일지가 삭제되었습니다.")

# 저장된 근무 일지 보기
if st.checkbox("저장된 근무 일지 보기"):
    st.write(df if not df.empty else "저장된 근무 일지가 없습니다.")

# CSV 파일 다운로드 버튼
if st.checkbox("CSV 파일 다운로드"):
    st.download_button(
        label="CSV 파일 다운로드",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=FILE_NAME,
        mime="text/csv"
    )
    
