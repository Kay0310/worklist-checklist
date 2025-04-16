
import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="작업목록표 입력 시스템", layout="wide")

st.title("📋 작업목록표 입력 시스템")

with st.form("worklist_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        company = st.text_input("회사명")
    with col2:
        task_unit = st.text_input("단위작업명")
    with col3:
        workers = st.number_input("실작업 인원", min_value=1, step=1)

    names = []
    for i in range(int(workers)):
        names.append(st.text_input(f"{i+1}번 작업자 이름"))

    st.markdown("---")

    st.subheader("📌 3. 신체부담 및 특이사항")
    posture = st.multiselect("작업자세 (복수 선택 가능)", ["쪼그려 앉는 자세", "몸통을 비트는 자세", "팔이 어깨위로 올라가는 자세", "고정된 자세로 서서 작업", "해당없음"])
    
    weights = []
    num_weights = st.number_input("중량물 개수", min_value=0, step=1)
    for i in range(int(num_weights)):
        wtype = st.text_input(f"중량물 {i+1} 종류")
        wkg = st.text_input(f"중량물 {i+1} 무게 (kg)")
        weights.append((wtype, wkg))

    tools = []
    num_tools = st.number_input("수공구 개수", min_value=0, step=1)
    for i in range(int(num_tools)):
        ttype = st.text_input(f"수공구 {i+1} 종류")
        tkg = st.text_input(f"수공구 {i+1} 무게 (kg)")
        tools.append((ttype, tkg))

    repeats = st.text_input("반복작업 (분당 회수 또는 시간당 횟수)")
    work_hour = st.number_input("작업 시간 (시)", min_value=0)
    work_min = st.number_input("작업 시간 (분)", min_value=0)

    submitted = st.form_submit_button("저장하고 종료")

    if submitted:
        df = pd.DataFrame({
            "회사명": [company],
            "단위작업명": [task_unit],
            "작업자 수": [workers],
            "작업자 이름": [", ".join(names)],
            "작업자세": [", ".join(posture)],
            "중량물": [", ".join([f"{w[0]}({w[1]}kg)" for w in weights])],
            "수공구": [", ".join([f"{t[0]}({t[1]}kg)" for t in tools])],
            "반복작업": [repeats],
            "작업시간": [f"{int(work_hour)}시간 {int(work_min)}분"]
        })

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"작업목록표_{company}_{task_unit}_{now}.xlsx"

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="작업목록표")

        st.success("✅ 저장이 완료되었습니다!")
        st.download_button("📥 엑셀파일 다운로드", data=buffer.getvalue(), file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
