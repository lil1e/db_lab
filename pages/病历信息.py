import streamlit as st
from db_utils import  fetch_query,insert_medical_record,query_medical_record,update_medical_record,delete_medical_record_by_id
import pandas as pd
# 使用 markdown 添加 CSS
st.markdown(
    """
    <style>
    body {
        background-color: #e0f7fa; /* 背景颜色 */
        font-family: 'Helvetica', sans-serif;
    }
    .main {
        background: #e0f7fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 20px auto;
    }
    h1 {
        color: #00796b;
    }
    p {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)



#################################################################显示所有病历信息####################################################
st.title("病历信息")
if st.button("显示所有病历信息"):
    medicalrecords = fetch_query("SELECT * FROM Medicalrecords")
    if medicalrecords:
        # for patient in patients:
        #     st.write(patient)

        column = ["病历ID","患者ID","入院时间","出院时间","入院情况","入院诊断","诊疗经过","出院诊断","出院医嘱"]

        data_df=pd.DataFrame(list(medicalrecords),columns=column)
        st.write(data_df)




##################################################################操作####################################################

st.title("病历信息操作")


st.subheader("录入病历信息")
# 创建病历信息表单
with st.form(key='medical_record_form'):
    patient_name = st.text_input('患者姓名')
    admission_date = st.date_input('入院日期')
    discharge_date = st.date_input('出院日期')
    admission_status = st.text_area('入院情况')
    admission_diagnosis = st.text_area('入院诊断')
    treatment_process = st.text_area('诊疗经过')
    discharge_diagnosis = st.text_area('出院诊断')
    discharge_advice = st.text_area('出院医嘱')

    submit_button = st.form_submit_button(label='提交')

    if submit_button:
        try:
            insert_medical_record(patient_name, admission_date, discharge_date, admission_status, admission_diagnosis, treatment_process, discharge_diagnosis, discharge_advice)
            st.success("病历信息已成功录入")
        except Exception as e:
            st.error(f"录入失败：{e}")





st.subheader("查询病历信息")

with st.form(key='query_patient_form'):
    # 输入姓名
    name = st.text_input('请输入患者姓名')
    # 提交按钮
    submit_button = st.form_submit_button(label='查询')
    # 处理表单提交
    if submit_button:
        try:
            # 查询患者信息
            records = query_medical_record(name)
            
            # 显示查询结果
            if records:
                # 如果找到患者信息，创建数据框并显示
                column = ["病历ID","患者ID","入院时间","出院时间","入院情况","入院诊断","诊疗经过","出院诊断","出院医嘱"]
                data_df1 = pd.DataFrame(records, columns=column)
                st.write(data_df1)
            else:
                st.error("未找到匹配的病历信息")
        
        except ValueError as e:
            st.error(f"错误：{e}")
        
        except Exception as e:
            st.error(f"查询过程中出现错误：{e}")


st.subheader("修改病历信息")

# 创建修改病历信息表单
with st.form(key='update_medical_record_form'):
    record_id = st.number_input('病历记录ID', min_value=1)
    admission_date = st.date_input('新入院日期')
    discharge_date = st.date_input('新出院日期')
    admission_status = st.text_area('新入院情况')
    admission_diagnosis = st.text_area('新入院诊断')
    treatment_process = st.text_area('新诊疗经过')
    discharge_diagnosis = st.text_area('新出院诊断')
    discharge_advice = st.text_area('新出院医嘱')

    submit_button = st.form_submit_button(label='提交')

    if submit_button:
        try:
            update_medical_record(record_id, admission_date, discharge_date, admission_status, admission_diagnosis, treatment_process, discharge_diagnosis, discharge_advice)
            st.success("病历信息已成功更新")
        except Exception as e:
            st.error(f"更新失败：{e}")


st.subheader("删除病历信息")

with st.form(key='delete_medical_record_form'):
    record_id = st.number_input('请输入要删除的病历信息ID', min_value=1)
    submit_button = st.form_submit_button(label='删除')

    if submit_button:
        try:
            delete_medical_record_by_id(record_id)
            st.success("病历信息已成功删除")
        except Exception as e:
            st.error(f"删除失败：{e}")
            if "RecordID" in str(e) and "does not exist" in str(e):
                st.error("病历信息不存在")