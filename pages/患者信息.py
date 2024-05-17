import streamlit as st
from db_utils import insert_patient, fetch_query,query_patient,update_patient,delete_patient_by_name
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



#################################################################显示所有患者信息####################################################
st.title("患者信息")
if st.button("显示所有患者信息"):
    patients = fetch_query("SELECT * FROM Patients")
    if patients:
        # for patient in patients:
        #     st.write(patient)

        column = ["患者ID","患者姓名","性别","年龄"]

        data_df=pd.DataFrame(list(patients),columns=column)
        st.write(data_df)



#################################################################操作####################################################

st.title("患者信息操作")
st.subheader("录入患者信息")
with st.form(key='insert_patient_form'):
    name = st.text_input('姓名')
    gender = st.selectbox('性别', ['男', '女', '其他'])
    age = st.number_input('年龄', min_value=0, max_value=120)
    submit_button = st.form_submit_button(label='提交')

    if submit_button:
        try:
            insert_patient(name, gender, age)
            st.success("患者信息已添加")
        except Exception as e:
            st.error(f"添加失败：{e}")


st.subheader("查询患者信息")

with st.form(key='query_patient_form'):
    # 输入姓名
    name = st.text_input('请输入患者姓名')
    # 提交按钮
    submit_button = st.form_submit_button(label='查询')
    # 处理表单提交
    if submit_button:
        try:
            # 查询患者信息
            patient_info = query_patient(name)
            
            # 显示查询结果
            if patient_info:
                # 如果找到患者信息，创建数据框并显示
                column = ["患者ID", "患者姓名", "性别", "年龄"]
                data_df1 = pd.DataFrame([patient_info], columns=column)
                st.write(data_df1)
            else:
                st.error("未找到匹配的患者信息")
        
        except ValueError as e:
            st.error(f"错误：{e}")
        
        except Exception as e:
            st.error(f"查询过程中出现错误：{e}")



st.subheader("更新患者信息")

with st.form(key='update_patient_form'):
    name = st.text_input('姓名')
    gender = st.selectbox('性别', ['男', '女', '其他'])
    age = st.number_input('年龄', min_value=0, max_value=120)
    patient_id = st.number_input('输入患者ID', min_value=1, step=1)
    submit_button = st.form_submit_button(label='提交')
    
    if submit_button:
        # 调用更新函数
        try:
            update_patient(patient_id, name, gender, age)
            st.success("患者信息已更新")
        except Exception as e:
            st.error(f"更新失败：{e}")



st.subheader("删除患者信息")

with st.form(key='delete_patient_form'):
    name = st.text_input('姓名')
    submit_button = st.form_submit_button(label='提交')
    
    if submit_button:
        if name:
            try:
                delete_patient_by_name(name)
                st.success(f"患者 '{name}' 的信息已删除")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"删除失败：{e}")
        else:
            st.error("请输入患者姓名")