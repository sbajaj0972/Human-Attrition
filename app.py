import pickle
import pandas as pd
from flask import Flask, render_template, request
from sklearn import metrics

app = Flask(__name__)

@app.route('/')
def base():
    return render_template('index.html')

@app.route('/predict', methods = ['post'])
def predictattr():

    model = pickle.load (open ('model.pkl','rb'))

    Age =	request.form.get('age')
    BusinessTravel	= request.form.get('bt')
    DailyRate	= request.form.get('dr')
    Department	= request.form.get('dept')
    DistanceFromHome = request.form.get('dfh')	
    Education	= request.form.get('edu')
    EducationField	= request.form.get('eduf')
    # EmployeeCount	= request.form.get('educ')
    #EmployeeNumber	= request.form.get('empno')
    EnvironmentSatisfaction	= request.form.get('envsat')
    Gender	= request.form.get('gender')
    HourlyRate	= request.form.get('hr')
    JobInvolvement	= request.form.get('jobinv')
    JobLevel = request.form.get('joblev')
    JobRole	= request.form.get('jobrol')
    JobSatisfaction	= request.form.get('jobsat')
    MaritalStatus	= request.form.get('maristatus')
    MonthlyIncome = request.form.get('moninc')
   # MonthlyRate	= request.form.get('monrat')
    NumCompaniesWorked	= request.form.get('numcomp')
    # Over18	= request.form.get('numcomp')
    OverTime = request.form.get('over18')
    #PercentSalaryHike = request.form.get('overtime')
    PerformanceRating	= request.form.get('perrat')
    RelationshipSatisfaction = request.form.get('relsat')	
    #StandardHours	= request.form.get('stahrs')
    StockOptionLevel = request.form.get('stopt')
    TotalWorkingYears	= request.form.get('twkhrs')
    TrainingTimesLastYear	= request.form.get('tratim')
    WorkLifeBalance	= request.form.get('wrklifbal')
    YearsAtCompany	= request.form.get('yrsatcomp')
    YearsInCurrentRole	= request.form.get('yrsincurrole')
    YearsSinceLastPromotion	= request.form.get('yrssinlasprom')
    YearsWithCurrManager = request.form.get('yrswitcurman')

    dict = {
        'Age': int (Age),
        'BusinessTravel': str (BusinessTravel),
        'DailyRate': int (DailyRate),
        'Department': Department,
        'DistanceFromHome': int (DistanceFromHome),
        'Education': Education,
        'EducationField': str (EducationField),
        'EnvironmentSatisfaction': int (EnvironmentSatisfaction),
        'Gender': str (Gender),
        'HourlyRate': int (HourlyRate),
        'JobInvolvement': int (JobInvolvement),
        'JobLevel': int (JobLevel),
        'JobRole': JobRole,
        'JobSatisfaction': int (JobSatisfaction),
        'MaritalStatus': str (MaritalStatus),
        'MonthlyIncome': int (MonthlyIncome),
        'NumCompaniesWorked': int (NumCompaniesWorked),
        'OverTime': str (OverTime),
        'PerformanceRating': int (PerformanceRating),
        'RelationshipSatisfaction': int (RelationshipSatisfaction),
        'StockOptionLevel': StockOptionLevel,
        'TotalWorkingYears': int (TotalWorkingYears),
        'TrainingTimesLastYear': TrainingTimesLastYear,
        'WorkLifeBalance': int (WorkLifeBalance),
        'YearsAtCompany': int (YearsAtCompany),
        'YearsInCurrentRole': int (YearsInCurrentRole),
        'YearsSinceLastPromotion': int (YearsSinceLastPromotion),
        'YearsWithCurrManager': int (YearsWithCurrManager)
    }

    df = pd.DataFrame ([dict])

    df['Total_Satisfaction'] = (df['EnvironmentSatisfaction'] +
                                df['JobInvolvement'] +
                                df['JobSatisfaction'] +
                                df['RelationshipSatisfaction'] +
                                df['WorkLifeBalance']) / 5

    # Drop Columns
    df.drop (
        ['EnvironmentSatisfaction','JobInvolvement','JobSatisfaction','RelationshipSatisfaction','WorkLifeBalance'],
        axis=1,inplace=True)

    # Convert Total satisfaction into boolean
    df['Total_Satisfaction_bool'] = df['Total_Satisfaction'].apply (lambda x: 1 if x >= 2.8 else 0)
    df.drop ('Total_Satisfaction',axis=1,inplace=True)

    # It can be observed that the rate of attrition of employees below age of 35 is high
    df['Age_bool'] = df['Age'].apply (lambda x: 1 if x < 35 else 0)
    df.drop ('Age',axis=1,inplace=True)

    # It can be observed that the employees are more likey the drop the job if dailyRate less than 800
    df['DailyRate_bool'] = df['DailyRate'].apply (lambda x: 1 if x < 800 else 0)
    df.drop ('DailyRate',axis=1,inplace=True)

    # Employees working at R&D Department have higher attrition rate
    df['Department_bool'] = df['Department'].apply (lambda x: 1 if x == 'Research & Development' else 0)
    df.drop ('Department',axis=1,inplace=True)

    # Rate of attrition of employees is high if DistanceFromHome > 10
    df['DistanceFromHome_bool'] = df['DistanceFromHome'].apply (lambda x: 1 if x > 10 else 0)
    df.drop ('DistanceFromHome',axis=1,inplace=True)

    # Employees are more likey to drop the job if the employee is working as Laboratory Technician
    df['JobRole_bool'] = df['JobRole'].apply (lambda x: 1 if x == 'Laboratory Technician' else 0)
    df.drop ('JobRole',axis=1,inplace=True)

    # Employees are more likey to the drop the job if the employee's hourly rate < 65
    df['HourlyRate_bool'] = df['HourlyRate'].apply (lambda x: 1 if x < 65 else 0)
    df.drop ('HourlyRate',axis=1,inplace=True)

    # Employees are more likey to the drop the job if the employee's MonthlyIncome < 4000
    df['MonthlyIncome_bool'] = df['MonthlyIncome'].apply (lambda x: 1 if x < 4000 else 0)
    df.drop ('MonthlyIncome',axis=1,inplace=True)

    # Rate of attrition of employees is high if NumCompaniesWorked < 3
    df['NumCompaniesWorked_bool'] = df['NumCompaniesWorked'].apply (lambda x: 1 if x > 3 else 0)
    df.drop ('NumCompaniesWorked',axis=1,inplace=True)

    # Employees are more likey to the drop the job if the employee's TotalWorkingYears < 8
    df['TotalWorkingYears_bool'] = df['TotalWorkingYears'].apply (lambda x: 1 if x < 8 else 0)
    df.drop ('TotalWorkingYears',axis=1,inplace=True)

    # Employees are more likey to the drop the job if the employee's YearsAtCompany < 3
    df['YearsAtCompany_bool'] = df['YearsAtCompany'].apply (lambda x: 1 if x < 3 else 0)
    df.drop ('YearsAtCompany',axis=1,inplace=True)

    # Employees are more likey to the drop the job if the employee's YearsInCurrentRole < 3
    df['YearsInCurrentRole_bool'] = df['YearsInCurrentRole'].apply (lambda x: 1 if x < 3 else 0)
    df.drop ('YearsInCurrentRole',axis=1,inplace=True)

    # Employees are more likely to the drop the job if the employee's YearsSinceLastPromotion < 1
    df['YearsSinceLastPromotion_bool'] = df['YearsSinceLastPromotion'].apply (lambda x: 1 if x < 1 else 0)
    df.drop ('YearsSinceLastPromotion',axis=1,inplace=True)

    # Employees are more likely to the drop the job if the employee's YearsWithCurrManager < 1
    df['YearsWithCurrManager_bool'] = df['YearsWithCurrManager'].apply (lambda x: 1 if x < 1 else 0)
    df.drop ('YearsWithCurrManager',axis=1,inplace=True)

    # Convert Categorical to Numerical
    # Buisness Travel
    if BusinessTravel == 'Rarely':
        df['BusinessTravel_Rarely'] = 1
        df['BusinessTravel_Frequently'] = 0
        df['BusinessTravel_No_Travel'] = 0
    elif BusinessTravel == 'Frequently':
        df['BusinessTravel_Rarely'] = 0
        df['BusinessTravel_Frequently'] = 1
        df['BusinessTravel_No_Travel'] = 0
    else:
        df['BusinessTravel_Rarely'] = 0
        df['BusinessTravel_Frequently'] = 0
        df['BusinessTravel_No_Travel'] = 1
    df.drop ('BusinessTravel',axis=1,inplace=True)

    # Education
    if Education == 1:
        df['Education_1'] = 1
        df['Education_2'] = 0
        df['Education_3'] = 0
        df['Education_4'] = 0
        df['Education_5'] = 0
    elif Education == 2:
        df['Education_1'] = 0
        df['Education_2'] = 1
        df['Education_3'] = 0
        df['Education_4'] = 0
        df['Education_5'] = 0
    elif Education == 3:
        df['Education_1'] = 0
        df['Education_2'] = 0
        df['Education_3'] = 1
        df['Education_4'] = 0
        df['Education_5'] = 0
    elif Education == 4:
        df['Education_1'] = 0
        df['Education_2'] = 0
        df['Education_3'] = 0
        df['Education_4'] = 1
        df['Education_5'] = 0
    else:
        df['Education_1'] = 0
        df['Education_2'] = 0
        df['Education_3'] = 0
        df['Education_4'] = 0
        df['Education_5'] = 1
    df.drop ('Education',axis=1,inplace=True)

    # EducationField
    if EducationField == 'Life Sciences':
        df['EducationField_Life_Sciences'] = 1
        df['EducationField_Medical'] = 0
        df['EducationField_Marketing'] = 0
        df['EducationField_Technical_Degree'] = 0
        df['Education_Human_Resources'] = 0
        df['Education_Other'] = 0
    elif EducationField == 'Medical':
        df['EducationField_Life_Sciences'] = 0
        df['EducationField_Medical'] = 1
        df['EducationField_Marketing'] = 0
        df['EducationField_Technical_Degree'] = 0
        df['Education_Human_Resources'] = 0
        df['Education_Other'] = 0
    elif EducationField == 'Marketing':
        df['EducationField_Life_Sciences'] = 0
        df['EducationField_Medical'] = 0
        df['EducationField_Marketing'] = 1
        df['EducationField_Technical_Degree'] = 0
        df['Education_Human_Resources'] = 0
        df['Education_Other'] = 0
    elif EducationField == 'Technical Degree':
        df['EducationField_Life_Sciences'] = 0
        df['EducationField_Medical'] = 0
        df['EducationField_Marketing'] = 0
        df['EducationField_Technical_Degree'] = 1
        df['Education_Human_Resources'] = 0
        df['Education_Other'] = 0
    elif EducationField == 'Human Resources':
        df['EducationField_Life_Sciences'] = 0
        df['EducationField_Medical'] = 0
        df['EducationField_Marketing'] = 0
        df['EducationField_Technical_Degree'] = 0
        df['Education_Human_Resources'] = 1
        df['Education_Other'] = 0
    else:
        df['EducationField_Life_Sciences'] = 0
        df['EducationField_Medical'] = 0
        df['EducationField_Marketing'] = 0
        df['EducationField_Technical_Degree'] = 0
        df['Education_Human_Resources'] = 1
        df['Education_Other'] = 1
    df.drop ('EducationField',axis=1,inplace=True)

    # Gender
    if Gender == 'Male':
        df['Gender_Male'] = 1
        df['Gender_Female'] = 0
    else:
        df['Gender_Male'] = 0
        df['Gender_Female'] = 1
    df.drop ('Gender',axis=1,inplace=True)

    # Marital Status
    if MaritalStatus == 'Married':
        df['MaritalStatus_Married'] = 1
        df['MaritalStatus_Single'] = 0
        df['MaritalStatus_Divorced'] = 0
    elif MaritalStatus == 'Single':
        df['MaritalStatus_Married'] = 0
        df['MaritalStatus_Single'] = 1
        df['MaritalStatus_Divorced'] = 0
    else:
        df['MaritalStatus_Married'] = 0
        df['MaritalStatus_Single'] = 0
        df['MaritalStatus_Divorced'] = 1
    df.drop ('MaritalStatus',axis=1,inplace=True)

    # Overtime
    if OverTime == 'Yes':
        df['OverTime_Yes'] = 1
        df['OverTime_No'] = 0
    else:
        df['OverTime_Yes'] = 0
        df['OverTime_No'] = 1
    df.drop ('OverTime',axis=1,inplace=True)

    # Stock Option Level
    if StockOptionLevel == 0:
        df['StockOptionLevel_0'] = 1
        df['StockOptionLevel_1'] = 0
        df['StockOptionLevel_2'] = 0
        df['StockOptionLevel_3'] = 0
    elif StockOptionLevel == 1:
        df['StockOptionLevel_0'] = 0
        df['StockOptionLevel_1'] = 1
        df['StockOptionLevel_2'] = 0
        df['StockOptionLevel_3'] = 0
    elif StockOptionLevel == 2:
        df['StockOptionLevel_0'] = 0
        df['StockOptionLevel_1'] = 0
        df['StockOptionLevel_2'] = 1
        df['StockOptionLevel_3'] = 0
    else:
        df['StockOptionLevel_0'] = 0
        df['StockOptionLevel_1'] = 0
        df['StockOptionLevel_2'] = 0
        df['StockOptionLevel_3'] = 1
    df.drop ('StockOptionLevel',axis=1,inplace=True)

    # Training Time Last Year
    if TrainingTimesLastYear == 0:
        df['TrainingTimesLastYear_0'] = 1
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 0
    elif TrainingTimesLastYear == 1:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 1
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 0
    elif TrainingTimesLastYear == 2:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 1
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 0
    elif TrainingTimesLastYear == 3:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 1
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 0
    elif TrainingTimesLastYear == 4:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 1
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 0
    elif TrainingTimesLastYear == 5:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 1
        df['TrainingTimesLastYear_6'] = 0
    else:
        df['TrainingTimesLastYear_0'] = 0
        df['TrainingTimesLastYear_1'] = 0
        df['TrainingTimesLastYear_2'] = 0
        df['TrainingTimesLastYear_3'] = 0
        df['TrainingTimesLastYear_4'] = 0
        df['TrainingTimesLastYear_5'] = 0
        df['TrainingTimesLastYear_6'] = 1
    df.drop ('TrainingTimesLastYear',axis=1,inplace=True)
    print(df.columns)
    data = model.predict(df)

    if data == 1:
        output = 'Candidate may leave the job'

    else:
        output = 'Candidate may not leave the job'

    return render_template('output.html',data=output)

if __name__ == "main":
    app.run(debug=True)
