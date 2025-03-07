import random
import streamlit as st

def generate_lotto():
    # 5개의 로또 번호를 생성
    return [sorted(random.sample(range(1, 46), 6)) for _ in range(5)]

# Streamlit UI 구성
st.title("🎉 로또 번호 생성기")
st.write("아래 버튼을 눌러 5개의 행운 번호를 생성하세요!")

# 버튼 생성
if st.button("로또 번호 생성"):
    lotto_numbers = generate_lotto()
    st.subheader("✨ 행운 번호 ✨")
    for i, nums in enumerate(lotto_numbers, start=1):
        st.write(f"행운 번호 {i}: {', '.join(map(str, nums))}")
else:
    st.write("버튼을 눌러 로또 번호를 생성해보세요!")