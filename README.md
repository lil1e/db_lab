## 实验二运行示例

+ 在python==3.8的环境下，安装requirements.txt文件中的安装包

+ 配置数据库

  ```
              host="localhost", 
              user="root", 
              passwd="123456",
              db="lab2"
  ```

  

+ 创建数据库代码

  ```
  CREATE TABLE Patients (
      PatientID INT AUTO_INCREMENT PRIMARY KEY,
      Name VARCHAR(100) NOT NULL UNIQUE,
      Gender ENUM('男', '女', '其他') NOT NULL,
      Age INT NOT NULL
  );
  
  CREATE TABLE MedicalRecords (
      RecordID INT AUTO_INCREMENT PRIMARY KEY,
      PatientID INT NOT NULL,
      AdmissionDate DATE NOT NULL,
      DischargeDate DATE,
      AdmissionStatus TEXT NOT NULL,
      AdmissionDiagnosis TEXT NOT NULL,
      TreatmentProcess TEXT NOT NULL,
      DischargeDiagnosis TEXT NOT NULL,
      DischargeAdvice TEXT NOT NULL,
      FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
  );
  ```

  

+ 使用命令行cd 到项目文件夹下

+ 使用`streamlit run home.py`在命令行中运行文件即可在网页显示
