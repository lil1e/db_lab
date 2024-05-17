import pymysql



# 创建数据库连接
def create_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host="localhost", 
            user="root", 
            passwd="123456",
            db="lab2"
        )
        
    except Exception as e:
        # 如果发生错误则回滚
        connection.rollback()
        print(f"连接发生错误. Error: {e}")
    return connection



#################################################################患者信息操作####################################################

# 插入患者信息
def insert_patient(name, gender, age):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Patients (Name, Gender, Age) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, gender, age))
        connection.commit()
        print("Patient inserted successfully.")
    finally:
        connection.close()

#查询患者信息
def query_patient(name):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Patients WHERE Name = %s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
            if result:
                return result
            # if result:
            #     print(f"Patient Information: ID={result[0]}, Name={result[1]}, Gender={result[2]}, Age={result[3]}")
            # else:
            #     print(f"No patient found with name {name}.")
    finally:
        connection.close()


#修改患者信息
def update_patient(patient_id, name=None, gender=None, age=None):
    connection = create_connection()
    cursor = connection.cursor()

    # 构建SQL更新语句
    sql = "UPDATE Patients SET "
    params = []
    if name:
        sql += "Name = %s, "
        params.append(name)
    if gender:
        sql += "Gender = %s, "
        params.append(gender)
    if age:
        sql += "Age = %s, "
        params.append(age)

    # 移除最后一个多余的逗号和空格
    sql = sql.rstrip(', ')
    sql += " WHERE PatientID = %s"
    params.append(patient_id)

    # 执行SQL语句
    cursor.execute(sql, tuple(params))
    connection.commit()
    print("Patient updated successfully.")



#删除患者信息
def delete_patient_by_name(name):
    connection = create_connection()
    cursor = connection.cursor()
    
    # 获取患者ID
    cursor.execute("SELECT PatientID FROM Patients WHERE Name = %s", (name,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError("Patient with name {} does not exist.".format(name))
    patient_id = result[0]

    # 删除关联的病历记录
    cursor.execute("DELETE FROM MedicalRecords WHERE PatientID = %s", (patient_id,))
    # 删除患者记录
    cursor.execute("DELETE FROM Patients WHERE PatientID = %s", (patient_id,))

    # 提交事务
    connection.commit()
    






# 示例: 插入患者信息
#insert_patient('李6', '男', 40)

# 示例: 查询患者信息
#query_patient('李6')

# # 示例: 修改患者信息
#update_patient(1, name='李四', gender='男', age=35)

# 示例: 删除患者信息及其病历
#delete_patient_by_name('王五')

#################################################################病历信息操作####################################################


#录入病历信息
def insert_medical_record(patient_name, admission_date, discharge_date, admission_status, admission_diagnosis, treatment_process, discharge_diagnosis, discharge_advice):
    connection = create_connection()
    cursor = connection.cursor()

    # 获取患者ID
    cursor.execute("SELECT PatientID FROM Patients WHERE Name = %s", (patient_name,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError("Patient with name {} does not exist.".format(patient_name))
    patient_id = result[0]

    # 插入医疗记录的SQL语句
    sql = """INSERT INTO MedicalRecords 
                (PatientID, AdmissionDate, DischargeDate, AdmissionStatus, AdmissionDiagnosis, TreatmentProcess, DischargeDiagnosis, DischargeAdvice) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    # 执行SQL语句
    cursor.execute(sql, (patient_id, admission_date, discharge_date, admission_status, admission_diagnosis, treatment_process, discharge_diagnosis, discharge_advice))
    # 提交到数据库执行
    connection.commit()
    #print("Medical record inserted successfully.")

#查询病历信息
def query_medical_record(name):
    connection = create_connection()
    cursor = connection.cursor()
   
        # 获取患者ID
    cursor.execute("SELECT PatientID FROM Patients WHERE Name = %s", (name,))
    result = cursor.fetchone()
    if result is None:
        print(f"No patient found with name {name}.")
        return
    patient_id = result[0]

    # 查询病历信息的SQL语句
    sql = """SELECT * FROM MedicalRecords WHERE PatientID = %s"""
    # 执行SQL语句
    cursor.execute(sql, (patient_id,))
    # 获取查询结果
    results = cursor.fetchall()
    if not results:
            raise ValueError(f"No medical records found for patient with name {name}.")
    return results


#修改病历信息
def update_medical_record(record_id, admission_date=None, discharge_date=None, admission_status=None, admission_diagnosis=None, treatment_process=None, discharge_diagnosis=None, discharge_advice=None):
    connection = create_connection()
    cursor = connection.cursor()
    
    # 构建SQL更新语句
    sql = "UPDATE MedicalRecords SET "
    params = []
    if admission_date:
        sql += "AdmissionDate = %s, "
        params.append(admission_date)
    if discharge_date:
        sql += "DischargeDate = %s, "
        params.append(discharge_date)
    if admission_status:
        sql += "AdmissionStatus = %s, "
        params.append(admission_status)
    if admission_diagnosis:
        sql += "AdmissionDiagnosis = %s, "
        params.append(admission_diagnosis)
    if treatment_process:
        sql += "TreatmentProcess = %s, "
        params.append(treatment_process)
    if discharge_diagnosis:
        sql += "DischargeDiagnosis = %s, "
        params.append(discharge_diagnosis)
    if discharge_advice:
        sql += "DischargeAdvice = %s, "
        params.append(discharge_advice)

    # 移除最后一个多余的逗号和空格
    sql = sql.rstrip(', ')
    sql += " WHERE RecordID = %s"
    params.append(record_id)

    # 执行SQL语句
    cursor.execute(sql, tuple(params))
    connection.commit()
    #print("Medical record updated successfully.")

#删除病历信息
def delete_medical_record_by_id(record_id):
    connection = create_connection()
    cursor = connection.cursor()

    # 检查病历是否存在
    cursor.execute("SELECT * FROM MedicalRecords WHERE RecordID = %s", (record_id,))
    result = cursor.fetchone()
    if result is None:
        raise ValueError("Medical record with ID {} does not exist.".format(record_id))

    # 删除病历记录
    cursor.execute("DELETE FROM MedicalRecords WHERE RecordID = %s", (record_id,))
    # 提交事务
    connection.commit()
    print("Medical record deleted successfully.")








# 示例: 插入医疗记录
#insert_medical_record('李6', '2024-05-01', '2024-05-15', '胸痛、呼吸困难', '心肌梗死', '急诊PCI手术', '病情稳定', '定期复查，按时服药')

# 示例: 查询病历信息
#query_medical_record('李6')

# # 示例: 修改病历信息
#update_medical_record(1, admission_status='发热、咳嗽', discharge_advice='多喝水，注意休息')

# # 示例: 删除病历信息
#delete_medical_record_by_id(1)

##############################################################################################################################

# 展示查询结果
def fetch_query(query):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        # 如果发生错误则回滚
        connection.rollback()
        print(f"展示发生错误. Error: {e}")
        return None
    finally:
        connection.close()

