import streamlit as st
import pandas as pd

st.set_page_config(page_title="작업목록표 입력기", layout="wide")

st.title("작업목록표 입력 시스템")

with st.form("entry_form"):
    회사명 = st.text_input("회사명")
    단위작업명 = st.text_input("단위작업명")
    작업자 = st.text_input("작업자 이름")
    특이사항 = st.text_area("특이사항 입력")

    submitted = st.form_submit_button("✅ 저장하고 종료")
    if submitted:
        df = pd.DataFrame({
            "회사명": [회사명],
            "단위작업명": [단위작업명],
            "작업자": [작업자],
            "특이사항": [특이사항],
        })
        df.to_excel(f"작업목록표_{회사명}_{단위작업명}.xlsx", index=False)
        st.success("입력 내용이 저장되었습니다.")
        st.download_button("엑셀 파일 다운로드", df.to_csv(index=False).encode("utf-8-sig"), file_name=f"작업목록표_{회사명}_{단위작업명}.csv")

