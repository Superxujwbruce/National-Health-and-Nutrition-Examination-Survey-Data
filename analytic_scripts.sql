/* 1. How many patients are being treated for Type 2 Diabetes? */

SELECT COUNT(patient_id) AS diabetes_patients, (SELECT COUNT(patient_id) FROM patients) AS all_patients
FROM patients p
WHERE patient_id IN (	SELECT patient_id 
						FROM prescription_reasons 
						WHERE reason_for_prescription ILIKE '%Type 2 Diabetes%' );
						

						
/* 2. What are the most commonly prescribed medications for patients with Type 2 Diabetes */

SELECT *
FROM (SELECT medication_id, COUNT(*) 
	  FROM prescription_reasons p 
	  WHERE reason_for_prescription ILIKE '%Type 2 Diabetes%'
	  GROUP BY medication_id) AS prescription_count
NATURAL JOIN medications
ORDER BY count DESC



/* 3. What is the average mg of Sodium (diet_types: DR1TSODI) consumed by patients with Type 2 Diabetes? */

SELECT AVG(value)
FROM diet
WHERE diet_id = 'DR1TSODI'
AND patient_id IN (SELECT patient_id 
				   FROM prescription_reasons 
				   WHERE reason_for_prescription ILIKE '%Type 2 Diabetes%');



/* 4. What percent of patients are married/divorced/separated etc. ? */ 

select maritalstatus_value,count(patient_id)/((select count(*) from patients)/100)as percentage      
from maritalstatus_lookup m left join patients p on m.maritalstatus_id=p.maritalstatus_id      
where m.maritalstatus_id=3 or m.maritalstatus_id=4 or  m.maritalstatus_id=1       
group by m.maritalstatus_id   



/* 5. What's the ethnicity of patients who have diabetes? */

select el.ethnicity_value,count(el.ethnicity_id)      
from ethnicity_lookup el join patients on el.ethnicity_id= patients.ethnicity_id      
join prescription_reasons pr on patients.patient_id= pr.patient_id      
where reason_for_prescription ilike '%type 2 diabetes%'      
group by el.ethnicity_id   



/* 6. What are the names and values of all examination information for patient 75262? */

SELECT examination_id, examination_name, value 
FROM examinations NATURAL JOIN examination_types
WHERE patient_id = 75262



/* 7. For the 2nd most prescribed medication in the dataset, what are the top reasons for prescription? */ 

SELECT reason_for_prescription, COUNT(*) 
FROM prescription_reasons
WHERE medication_id = 	(SELECT medication_id
						 FROM (SELECT medication_id,
								 RANK () OVER (
								 ORDER BY c.med_count DESC) as top_med
	  						   FROM (SELECT medication_id, COUNT(*) AS med_count
			 						 FROM patient_medications pm
			 						 GROUP BY medication_id) AS c) AS rr
						 WHERE rr.top_med = 2)
GROUP BY reason_for_prescription
ORDER BY count DESC
LIMIT 5; 



/* 8. For those patients who have taken medicine for 100 days, how many are married?  */

select count(*) from  patient_medications m left join patients p on m.patient_id=p.patient_id    
where m.days_taken>100 and p.maritalstatus_id=1   



/* 9. What is the income level for patients who are being treated for diabetes */

select p.patient_id,i.income_value 
from income_lookup as i left join patients as p on i.income_id=p.income_id  
where p.patient_id in (select patient_id from prescription_reasons where  reason_for_prescription LIKE 'Type 2 diabetes%' )
order by i.income_id



/* 10. What are the top 10 labs patients who developed diabetes conducted? */

select count(t.lab_name) count,t.lab_name    
from lab_types t left join labs l on  t.lab_id=l.lab_id    
where l.patient_id in (select patient_id from prescription_reasons where reason_for_prescription  ilike '%type 2 diabetes%')    
group by t.lab_name    
order by count desc limit 10




