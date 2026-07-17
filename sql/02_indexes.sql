-- ============================================================
-- PEOPLEPULSE AI
-- INDEXES
-- ============================================================

-- ============================
-- EMPLOYEES
-- ============================

CREATE INDEX idx_emp_department
ON employees(department);

CREATE INDEX idx_emp_job_role
ON employees(job_role);

CREATE INDEX idx_emp_attrition
ON employees(attrition);

CREATE INDEX idx_emp_gender
ON employees(gender);

CREATE INDEX idx_emp_income
ON employees(monthly_income);

CREATE INDEX idx_emp_age
ON employees(age);

-- ============================
-- EMPLOYEE SURVEYS
-- ============================

CREATE INDEX idx_survey_job_satisfaction
ON employee_surveys(job_satisfaction);

CREATE INDEX idx_survey_environment
ON employee_surveys(environment_satisfaction);

CREATE INDEX idx_survey_worklife
ON employee_surveys(work_life_balance);

-- ============================
-- MANAGER SURVEYS
-- ============================

CREATE INDEX idx_manager_performance
ON manager_surveys(performance_rating);

CREATE INDEX idx_manager_involvement
ON manager_surveys(job_involvement);

-- ============================
-- EMPLOYEE MASTER
-- ============================

CREATE INDEX idx_master_department
ON employee_master(department);

CREATE INDEX idx_master_job_role
ON employee_master(job_role);

CREATE INDEX idx_master_attrition
ON employee_master(attrition);

CREATE INDEX idx_master_income_band
ON employee_master(income_band);

CREATE INDEX idx_master_age_group
ON employee_master(age_group);

CREATE INDEX idx_master_experience
ON employee_master(experience_level);

CREATE INDEX idx_master_promotion
ON employee_master(promotion_status);

CREATE INDEX idx_master_attrition_flag
ON employee_master(attrition_flag);

-- ============================================================
-- SUCCESS
-- ============================================================

SELECT 'Indexes created successfully!' AS status;
