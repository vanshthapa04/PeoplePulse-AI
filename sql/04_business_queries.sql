-- ============================================================
-- PEOPLEPULSE AI
-- BUSINESS ANALYSIS QUERIES
-- ============================================================

---------------------------------------------------------------
-- 1. Total Employees
---------------------------------------------------------------

SELECT COUNT(*) AS total_employees
FROM employees;


---------------------------------------------------------------
-- 2. Overall Attrition Rate
---------------------------------------------------------------

SELECT
ROUND(
100.0 *
SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END)
/
COUNT(*),2
) AS attrition_rate
FROM employees;


---------------------------------------------------------------
-- 3. Employees by Department
---------------------------------------------------------------

SELECT
department,
COUNT(*) employees
FROM employees
GROUP BY department
ORDER BY employees DESC;


---------------------------------------------------------------
-- 4. Attrition by Department
---------------------------------------------------------------

SELECT
department,
COUNT(*) employees,
SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) attrition_count,
ROUND(
100.0*
SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END)
/COUNT(*),2
) attrition_rate
FROM employees
GROUP BY department
ORDER BY attrition_rate DESC;


---------------------------------------------------------------
-- 5. Average Salary by Department
---------------------------------------------------------------

SELECT
department,
ROUND(AVG(monthly_income),2) avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;


---------------------------------------------------------------
-- 6. Top Paying Job Roles
---------------------------------------------------------------

SELECT
job_role,
ROUND(AVG(monthly_income),2) avg_salary
FROM employees
GROUP BY job_role
ORDER BY avg_salary DESC;


---------------------------------------------------------------
-- 7. Average Experience by Department
---------------------------------------------------------------

SELECT
department,
ROUND(AVG(total_working_years),2) avg_experience
FROM employees
GROUP BY department
ORDER BY avg_experience DESC;


---------------------------------------------------------------
-- 8. Employees Not Promoted for 5+ Years
---------------------------------------------------------------

SELECT
employee_id,
department,
job_role,
years_since_last_promotion
FROM employees
WHERE years_since_last_promotion>=5
ORDER BY years_since_last_promotion DESC;


---------------------------------------------------------------
-- 9. Highest Salary Employees
---------------------------------------------------------------

SELECT
employee_id,
job_role,
monthly_income
FROM employees
ORDER BY monthly_income DESC
LIMIT 10;


---------------------------------------------------------------
-- 10. Job Satisfaction Distribution
---------------------------------------------------------------

SELECT
job_satisfaction,
COUNT(*) employees
FROM employee_surveys
GROUP BY job_satisfaction
ORDER BY job_satisfaction;


---------------------------------------------------------------
-- 11. Performance Rating Distribution
---------------------------------------------------------------

SELECT
performance_rating,
COUNT(*) employees
FROM manager_surveys
GROUP BY performance_rating;


---------------------------------------------------------------
-- 12. Employees with Low Satisfaction
---------------------------------------------------------------

SELECT
employee_id,
job_satisfaction,
environment_satisfaction,
work_life_balance
FROM employee_surveys
WHERE
job_satisfaction<=2
OR environment_satisfaction<=2
OR work_life_balance<=2;


---------------------------------------------------------------
-- 13. Gender Distribution
---------------------------------------------------------------

SELECT
gender,
COUNT(*) employees
FROM employees
GROUP BY gender;


---------------------------------------------------------------
-- 14. Attrition by Gender
---------------------------------------------------------------

SELECT
gender,
SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END) attrition,
COUNT(*) employees
FROM employees
GROUP BY gender;


---------------------------------------------------------------
-- 15. Employees Traveling Frequently
---------------------------------------------------------------

SELECT
business_travel,
COUNT(*) employees
FROM employees
GROUP BY business_travel;


---------------------------------------------------------------
-- 16. Department Metrics View
---------------------------------------------------------------

SELECT *
FROM vw_department_metrics;


---------------------------------------------------------------
-- 17. Highest Risk Employees
---------------------------------------------------------------

SELECT *
FROM vw_employee_risk
WHERE risk_level='High Risk'
ORDER BY risk_score DESC;


---------------------------------------------------------------
-- 18. Average Performance by Department
---------------------------------------------------------------

SELECT
department,
ROUND(AVG(performance_rating),2) avg_rating
FROM vw_employee_summary
GROUP BY department
ORDER BY avg_rating DESC;


---------------------------------------------------------------
-- 19. Salary vs Performance
---------------------------------------------------------------

SELECT
performance_rating,
ROUND(AVG(monthly_income),2) avg_salary
FROM vw_employee_summary
GROUP BY performance_rating
ORDER BY performance_rating;


---------------------------------------------------------------
-- 20. Top Departments with Highest Attrition Risk
---------------------------------------------------------------

SELECT
department,
AVG(risk_score) avg_risk
FROM vw_employee_risk
GROUP BY department
ORDER BY avg_risk DESC;