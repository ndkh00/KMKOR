import streamlit as st

# 앱 제목
st.title('시간당 급여 계산기')

# 사용자가 시간을 입력하도록 안내 (기본값 공란)
hours_input = st.text_input('일한 시간을 입력하세요 (최소 4시간):')

# 시간당 급여 설정
hourly_rate = 10000  # 1시간에 만 원

# 입력값이 비어 있지 않고 유효한 값이면 계산
if hours_input and hours_input.isdigit():  # 입력값이 숫자일 때만 계산
    hours = int(hours_input)
    if hours >= 4:
        total_payment = hours * hourly_rate
        st.write(f'Total Hour : {hours} Hour')
        st.write(f'Total Amount : US {total_payment:,}')
    else:
        st.write('최소 4시간 이상을 입력해주세요.')
else:
    st.write('유효한 시간을 입력해주세요.')