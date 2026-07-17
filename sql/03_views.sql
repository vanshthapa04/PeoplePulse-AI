-- ============================================================
-- PEOPLEPULSE AI
-- ANALYTICAL VIEWS
-- ============================================================

-- ============================================================
-- Remove existing views
-- ============================================================

DROP VIEW IF EXISTS vw_employee_summary CASCADE;
DROP VIEW IF EXISTS vw_department_metrics CASCADE;
DROP VIEW IF EXISTS vw_attrition_analysis CASCADE;
DROP VIEW IF EXISTS vw_performance_analysis CASCADE;
DROP VIEW IF EXISTS vw_employee_risk CASCADE;

-- ============================================================
-- 1. EMPLOYEE SUMMARY
-- ============================================================

CREATE VIEW vw_employee_summary AS

SELECT

    e.employee_id,
    e.age,
    e.gender,
    e.department,
    e.job_role,
    e.job_level,
    e.monthly_income,
    e.business_travel,
    e.distance_from_home,
    e.total_working_years,
    e.years_at_company,
    e.years_since_last_promotion,
    e.attrition,

    s.environment_satisfaction,
    s.job_satisfaction,
    s.work_life_balance,

    m.job_involvement,
    m.performance_rating

FROM employees e

LEFT JOIN employee_surveys s
ON e.employee_id = s.employee_id

LEFT JOIN manager_surveys m
ON e.employee_id = m.employee_id;

-- ============================================================
-- 2. DEPARTMENT METRICS
-- ============================================================

CREATE VIEW vw_department_metrics AS

SELECT

    department,

    COUNT(*) AS employee_count,

    ROUND(AVG(monthly_income),2) AS avg_salary,

    ROUND(AVG(total_working_years),2) AS avg_experience,

    ROUND(AVG(environment_satisfaction),2) AS avg_environment_satisfaction,

    ROUND(AVG(job_satisfaction),2) AS avg_job_satisfaction,

    ROUND(AVG(work_life_balance),2) AS avg_work_life_balance,

    ROUND(AVG(performance_rating),2) AS avg_performance,

    SUM(
        CASE
            WHEN attrition='Yes' THEN 1
            ELSE 0
        END
    ) AS attrition_count,

    ROUND(
        100.0 *
        SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS attrition_rate

FROM vw_employee_summary

GROUP BY department;

-- ============================================================
-- 3. ATTRITION ANALYSIS
-- ============================================================

CREATE VIEW vw_attrition_analysis AS

SELECT

    department,
    job_role,
    gender,

    COUNT(*) AS employees,

    SUM(
        CASE
            WHEN attrition='Yes'
            THEN 1
            ELSE 0
        END
    ) AS attrition,

    ROUND(
        100.0 *
        SUM(CASE WHEN attrition='Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS attrition_rate

FROM vw_employee_summary

GROUP BY
department,
job_role,
gender;

-- ============================================================
-- 4. PERFORMANCE ANALYSIS
-- ============================================================

CREATE VIEW vw_performance_analysis AS

SELECT

    performance_rating,

    COUNT(*) AS employees,

    ROUND(AVG(monthly_income),2) AS avg_salary,

    ROUND(AVG(job_satisfaction),2) AS avg_job_satisfaction,

    ROUND(AVG(work_life_balance),2) AS avg_worklife,

    ROUND(AVG(total_working_years),2) AS avg_experience

FROM vw_employee_summary

GROUP BY performance_rating

ORDER BY performance_rating;

-- ============================================================
-- 5. EMPLOYEE RISK VIEW
-- ============================================================

CREATE VIEW vw_employee_risk AS

SELECT

    employee_id,

    department,

    job_role,

    attrition,

    environment_satisfaction,

    job_satisfaction,

    work_life_balance,

    performance_rating,

    years_since_last_promotion,

    distance_from_home,

    business_travel,

    (
        CASE WHEN job_satisfaction <= 2 THEN 1 ELSE 0 END +

        CASE WHEN work_life_balance <= 2 THEN 1 ELSE 0 END +

        CASE WHEN environment_satisfaction <= 2 THEN 1 ELSE 0 END +

        CASE WHEN years_since_last_promotion >= 5 THEN 1 ELSE 0 END +

        CASE WHEN distance_from_home >= 15 THEN 1 ELSE 0 END +

        CASE WHEN business_travel='Travel_Frequently' THEN 1 ELSE 0 END

    ) AS risk_score,

    CASE

        WHEN
        (
            CASE WHEN job_satisfaction <=2 THEN 1 ELSE 0 END +

            CASE WHEN work_life_balance <=2 THEN 1 ELSE 0 END +

            CASE WHEN environment_satisfaction <=2 THEN 1 ELSE 0 END +

            CASE WHEN years_since_last_promotion>=5 THEN 1 ELSE 0 END +

            CASE WHEN distance_from_home>=15 THEN 1 ELSE 0 END +

            CASE WHEN business_travel='Travel_Frequently' THEN 1 ELSE 0 END

        ) >= 4

        THEN 'High Risk'

        WHEN
        (
            CASE WHEN job_satisfaction <=2 THEN 1 ELSE 0 END +

            CASE WHEN work_life_balance <=2 THEN 1 ELSE 0 END +

            CASE WHEN environment_satisfaction <=2 THEN 1 ELSE 0 END +

            CASE WHEN years_since_last_promotion>=5 THEN 1 ELSE 0 END +

            CASE WHEN distance_from_home>=15 THEN 1 ELSE 0 END +

            CASE WHEN business_travel='Travel_Frequently' THEN 1 ELSE 0 END

        ) >=2

        THEN 'Medium Risk'

        ELSE 'Low Risk'

    END AS risk_level

FROM vw_employee_summary;

-- ============================================================
-- SUCCESS
-- ============================================================

SELECT 'All analytical views created successfully!' AS status;