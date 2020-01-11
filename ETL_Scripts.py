## ------ CONNECT TO TEAM SERVER -------##

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
conn_url = 'postgresql://postgres:rjxklxet@f19server.apan5310.com:50203/nhanes_g3'

engine = create_engine(conn_url)
connection = engine.connect()



## ------ CREATE TABLE STATEMENTS -------##

stmt = """


CREATE TABLE MaritalStatus_lookup (
        maritalStatus_id 		int,
        maritalStatus_value 	varchar(50) NOT NULL,
        PRIMARY KEY(maritalStatus_id)
);

CREATE TABLE Ethnicity_lookup(
        ethnicity_id 		int,
        ethnicity_value 	varchar(50) NOT NULL,
        PRIMARY KEY(ethnicity_id)
);

CREATE TABLE Country_lookup(
        country_id  	int,
        country_value 	varchar(50) NOT NULL,
        PRIMARY KEY(country_id)
);

CREATE TABLE Income_lookup(
        income_id  		int,
        income_value 	varchar(50) NOT NULL,
        PRIMARY KEY(income_id)
);



CREATE TABLE Patients (
        patient_id			int,
        maritalStatus_id	int NOT NULL,
        ethnicity_id		int NOT NULL,
        country_id			int NOT NULL,
        income_id			int NOT NULL,
        PRIMARY KEY (patient_id),
        FOREIGN KEY (maritalStatus_id) REFERENCES MaritalStatus_lookup (maritalStatus_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (ethnicity_id) REFERENCES Ethnicity_lookup (ethnicity_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (country_id) REFERENCES Country_lookup (country_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (income_id) REFERENCES Income_lookup (income_id)
                ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE Medications (
        medication_id		varchar(10),
        medication_name		varchar(100) NOT NULL,
        PRIMARY KEY (medication_id)
);

CREATE TABLE Prescription_Reasons (
		patient_id					int,
		medication_id				varchar(10),
		prescription_number			int,
		reason_number				int,
		reason_for_prescription		varchar(150) NOT NULL,
		PRIMARY KEY (patient_id, medication_id, prescription_number, reason_number),
		FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
			ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY (medication_id) REFERENCES Medications (medication_id)
			ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Patient_Medications (
        patient_id				int,
        medication_id			varchar(10),
        prescription_number		int,
        days_taken				int NOT NULL,
        PRIMARY KEY (patient_id, medication_id, prescription_number),
        FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (medication_id) REFERENCES Medications (medication_id)
                ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE Examination_Categories (
		examination_category_id		int,
		examination_category_name	varchar(150) NOT NULL,
		PRIMARY KEY (examination_category_id)
);

CREATE TABLE Examination_Types (
		examination_id				varchar(10),
		examination_name			varchar(300) NOT NULL,
		examination_category_id		int NOT NULL,
		PRIMARY KEY (examination_id),
		FOREIGN KEY (examination_category_id) REFERENCES Examination_Categories (examination_category_id)
				ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Examinations (
        patient_id		int,
        examination_id	varchar(10) NOT NULL,
		value			varchar(20) NOT NULL,
        PRIMARY KEY (patient_id, examination_id),
        FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY (examination_id) REFERENCES Examination_Types (examination_id)
				ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE Lab_Categories (
		lab_category_id		int,
		lab_category_name	varchar(150) NOT NULL,
		PRIMARY KEY (lab_category_id)
);

CREATE TABLE Lab_Types (
		lab_id				varchar(10),
		lab_name			varchar(300) NOT NULL,
		lab_category_id		int NOT NULL,
		PRIMARY KEY (lab_id),
		FOREIGN KEY (lab_category_id) REFERENCES Lab_Categories (lab_category_id)
				ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Labs (
        patient_id		int,
        lab_id			varchar(10) NOT NULL,
		value			int NOT NULL,
        PRIMARY KEY (patient_id, lab_id),
        FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY (lab_id) REFERENCES Lab_Types (lab_id)
				ON UPDATE CASCADE ON DELETE CASCADE
);



CREATE TABLE Diet_Types (
		diet_id		varchar(10),
		diet_name	varchar(300) NOT NULL,
		PRIMARY KEY (diet_id)
);

CREATE TABLE Diet (
        patient_id		int,
        diet_id			varchar(10) NOT NULL,
		value			int NOT NULL,
        PRIMARY KEY (patient_id, diet_id),
        FOREIGN KEY (patient_id) REFERENCES Patients (patient_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY (diet_id) REFERENCES Diet_Types (diet_id)
				ON UPDATE CASCADE ON DELETE CASCADE
);


"""
connection.execute(stmt)



## ------ LOAD DEMOGRAPHICS LOOKUP TABLES -------##

stmt1 = """
    INSERT INTO maritalstatus_lookup (maritalstatus_id, maritalstatus_value)
    VALUES (0, 'Missing'),
    (1, 'Married'),
    (2, 'Widowed'),
    (3, 'Divorced'),
    (4, 'Separated'),
    (5, 'Never married'),
    (6, 'Living with partner'),
    (77, 'Refused'),
    (99, 'Do not Know');
    
    INSERT INTO ethnicity_lookup (ethnicity_id, ethnicity_value)
    VALUES (0, 'Missing'),
    (1, 'Mexican American'),
    (2, 'Other Hispanic'),
    (3, 'Non-Hispanic White'),
    (4, 'Non-Hispanic Black'),
    (6, 'Non-Hispanic Asian'),
    (7, 'Other Race - Including Multi-Racial');

    INSERT INTO country_lookup (country_id, country_value)
    VALUES (0, 'Missing'),
    (1, 'Born in 50 US states or Washington, DC'),
    (2, 'Others'),
    (77, 'Refused'),
    (99, 'Do not Know');

    INSERT INTO income_lookup (income_id, income_value)
    VALUES (0, 'Missing'),
    (1, '$ 0 to $ 4,999'),
    (2, '$ 5,000 to $ 9,999'),
    (3, '$10,000 to $14,999'),
    (4, '$15,000 to $19,999'),
    (5, '$20,000 to $24,999'),
    (6, '$25,000 to $34,999'),
    (7, '$35,000 to $44,999'),
    (8, '$45,000 to $54,999'),
    (9, '$55,000 to $64,999'),
    (10, '$65,000 to $74,999'),
    (12, '$20,000 and Over'),
    (13, 'Under $20,000'),
    (14, '$75,000 to $99,999'),
    (15, '$100,000 and Over'),
    (77, 'Refused'),
    (99, 'Do not Know');

"""
connection.execute(stmt1)


## ------ EXTRACT ALL TABULAR DATA -------##


demographics = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/national-health-and-nutrition-examination-survey/demographic.csv')

meds = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/national-health-and-nutrition-examination-survey/medications.csv', encoding='cp1252')

diet = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/national-health-and-nutrition-examination-survey/diet.csv')
diet_types_t1 = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/diet_types.csv', encoding = 'UTF-8')

exams = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/national-health-and-nutrition-examination-survey/examination.csv')
examination_types_t1 = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/examination_types.csv', encoding = 'UTF-8')

labs = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/national-health-and-nutrition-examination-survey/labs.csv')
lab_types_t1 = pd.read_csv('/Users/jamesgilson/Desktop/Columbia/S3_Fall 2019/SQL/Assignments/Group Project/lab_types.csv', encoding = 'UTF-8')



## ------ TRANSFORM PATIENTS TABLE -------##

# The Demographics table looks to be inclusive of all patients
# Joining SEQN from all tables together anyway, just in case
patients_t1 = pd.DataFrame(set(pd.concat(objs = [demographics.SEQN, diet.SEQN, exams.SEQN, labs.SEQN])), columns = ['SEQN'])
patients_t2 = pd.merge(left = patients_t1, right = demographics)

# Select and rename relevant columns
patients = patients_t2[['SEQN', 'DMDMARTL', 'RIDRETH3', 'DMDHRBR4', 'INDHHIN2']]
patients.rename(columns= {"SEQN": "patient_id",
                          "DMDMARTL": "maritalstatus_id", 
                          "RIDRETH3": "ethnicity_id",
                          "DMDHRBR4": "country_id",
                          "INDHHIN2": "income_id"}, inplace = True)

# replace missing values with appropriate code
patients.fillna(0, inplace = True)


## ------ TRANSFORM MEDICATIONS TABLES -------##

# Truncate to relevant variables, drop duplicate medications, remove NAs, and rename columns
medications = meds[['RXDDRGID','RXDDRUG']].drop_duplicates().dropna().reset_index(drop=True).rename(columns={"RXDDRGID": "medication_id","RXDDRUG": "medication_name"})


### Prescription_Reasons and Patient_Medications joint transformations 

med_transform = meds.dropna(subset = ['RXDDRGID'])

# Create a counter for duplicate prescriptions for the same patient
unique_key = np.array(med_transform['SEQN'].map(str) + med_transform['RXDDRGID'])

prescription_number = []

for idx, item in enumerate(unique_key):
    array_slice = unique_key[:idx]
    
    count = (array_slice == item).sum() + 1

    prescription_number.append(count)
    
med_transform['prescription_number'] = prescription_number

### Prescriotion_Reasons Transformations
# Isolate relevant columns and rename id variable
prescription_reasons_t1 = med_transform[['SEQN', 'RXDDRGID','RXDRSD1','RXDRSD2','RXDRSD3', 'prescription_number']].rename(columns = {'SEQN':'patient_id','RXDDRGID': 'medication_id','RXDRSD1':'1', 'RXDRSD2':'2', 'RXDRSD3':'3'})
# Convert from wide to long
prescription_reasons_t2 = pd.melt(prescription_reasons_t1, id_vars=['patient_id', 'medication_id', 'prescription_number'],var_name='reason_number', value_name='reason_for_prescription')

# Convert reason_number column to integer, drop 
prescription_reasons_t2['reason_number'] = prescription_reasons_t2['reason_number'].astype(int)
prescription_reasons = prescription_reasons_t2.drop_duplicates(keep='first').dropna()

### Patient_medications Transformations

Patient_Medications_t1 = med_transform[['SEQN', 'RXDDRGID','RXDDAYS', 'prescription_number']]
Patient_Medications_t1.dropna(inplace=True)

Patient_Medications_t1 = med_transform[['SEQN', 'RXDDRGID','RXDDAYS', 'prescription_number']]
Patient_Medications_t2 = Patient_Medications_t1.dropna().reset_index(drop=True)
patient_medications = Patient_Medications_t2.rename(columns={'SEQN':'patient_id','RXDDAYS':'days_taken','RXDDRGID':'medication_id'})

## ------ TRANSFORM EXAMINATIONS TABLES -------##

# new examinations format
examinations = pd.melt(exams,id_vars=['SEQN'],var_name='examination_id', value_name='value')
examinations = examinations.dropna().reset_index(drop=True)
examinations.rename(columns = {'SEQN': 'patient_id'}, inplace = True)

# there are a number of duplicated 'examination_id' rows in our dictionary
# these rows arent relevant to our examinations data, but we'll remove them, anyway
examination_types_t2 = examination_types_t1.drop_duplicates(subset='examination_id', keep = 'first')

# Isolate a list of examinations whose definitions we need, and join that list with the definitions from dictionary
relevant_exams = list(set(examinations.examination_id))
relevant_exams = pd.DataFrame(relevant_exams, columns=['examination_id'])

examination_types_t3 = pd.merge(left = relevant_exams, right = examination_types_t2, how = 'inner')

# it looks like there are examination_id codes in the examinations table that arent in the data dictionary
# We'll have to remove them or add them into dictionary manually -- in this case, going to remove for simplicity
key_diff = set(examinations.examination_id).difference(examination_types_t3.examination_id)
examinations['where_diff'] = examinations.examination_id.isin(key_diff)

examinations = examinations[examinations['where_diff'] == False]

examinations.drop(columns = 'where_diff', inplace = True)

# Now we need to create a table for the broader examination_categories
exam_cat = list(set(examination_types_t3['examination_type']))
examination_categories = pd.DataFrame(exam_cat, columns = ['examination_category_name'])

# create id for examination_categories
examination_categories['examination_category_id'] = range(1,len(examination_categories)+1)

# merge examinaion_types with new examination_category_id column
examination_types = pd.merge(left = examination_types_t3, left_on = 'examination_type', right = examination_categories, right_on = 'examination_category_name', how = 'inner')
examination_types.drop(columns = ['examination_type', 'examination_category_name'], inplace = True)


## ------ TRANSFORM LABS AND DIET TABLES -------##

# This is the same process as was used for the examinations tables.  

### LABS ###
labs = pd.melt(labs,id_vars=['SEQN'],var_name='lab_id', value_name='value')
labs = labs.dropna().reset_index(drop=True)
labs.rename(columns = {'SEQN': 'patient_id'}, inplace = True)

lab_types_t2 = lab_types_t1.drop_duplicates(subset='lab_id', keep = 'first')

relevant_labs = list(set(labs.lab_id))
relevant_labs = pd.DataFrame(relevant_labs, columns=['lab_id'])

lab_types_t3 = pd.merge(left = relevant_labs, right = lab_types_t2, how = 'inner')

key_diff = set(labs.lab_id).difference(lab_types_t3.lab_id)
labs['where_diff'] = labs.lab_id.isin(key_diff)

labs = labs[labs['where_diff'] == False]

labs.drop(columns = 'where_diff', inplace = True)

lab_cat = list(set(lab_types_t3['lab_category']))
lab_categories = pd.DataFrame(lab_cat, columns = ['lab_category_name'])

lab_categories['lab_category_id'] = range(1,len(lab_categories)+1)

lab_types = pd.merge(left = lab_types_t3, left_on = 'lab_category', right = lab_categories, right_on = 'lab_category_name', how = 'inner')
lab_types.drop(columns = ['lab_category', 'lab_category_name'], inplace = True)

### DIET ###
diet = pd.melt(diet,id_vars=['SEQN'],var_name='diet_id', value_name='value')
diet = diet.dropna().reset_index(drop=True)
diet.rename(columns = {'SEQN': "patient_id"}, inplace = True)

diet_types_t2 = diet_types_t1.drop_duplicates(subset='diet_id', keep = 'first')

relevant_diet = list(set(diet.diet_id))
relevant_diet = pd.DataFrame(relevant_diet, columns=['diet_id'])

diet_types_t3 = pd.merge(left = relevant_diet, right = diet_types_t2, how = 'inner')

key_diff = set(diet.diet_id).difference(diet_types_t3.diet_id)
diet['where_diff'] = diet.diet_id.isin(key_diff)

diet = diet[diet['where_diff'] == False]

diet.drop(columns = 'where_diff', inplace = True)

diet_cat = list(set(diet_types_t3['diet_category']))
diet_categories = pd.DataFrame(diet_cat, columns = ['diet_category_name'])

diet_categories['diet_category_id'] = range(1,len(diet_categories)+1)

diet_types = pd.merge(left = diet_types_t3, left_on = 'diet_category', right = diet_categories, right_on = 'diet_category_name', how = 'inner')
diet_types.drop(columns = ['diet_category', 'diet_category_name'], inplace = True)

# There is only one diet_category left in our diet table, after cleaning
# So no immediate need for a diet_categories, table
diet_types.drop(columns=['diet_category_id'], inplace = True)



## ------ LOAD TRANSFORMED TABLES INTO TEAM DATABASE -------##

'''
--- LOAD PLAN --- 

patients

medications
prescription_reasons
patient_medications

examination_categories
examination_types
examinations

lab_categories
lab_types
labs

diet_types
diet


'''

load_plan = [patients, 
             medications, prescription_reasons, patient_medications, 
             examination_categories, examination_types, examinations, 
             lab_categories, lab_types, labs, 
             diet_types, diet]

for table in load_plan:
	table_name = str(table)

	table.to_sql(name = table_name, con = engine, if_exists = append, index = False)

