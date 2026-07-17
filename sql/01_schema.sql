-- ============================================================
-- PEOPLEPULSE AI
-- DATABASE SCHEMA
-- ============================================================

-- ============================================================
-- DROP TABLES (Optional for Development)
-- ============================================================

DROP TABLE IF EXISTS employee_master CASCADE;
DROP TABLE IF EXISTS manager_surveys CASCADE;
DROP TABLE IF EXISTS employee_surveys CASCADE;
DROP TABLE IF EXISTS employees CASCADE;

-- ============================================================
-- EMPLOYEES
-- ============================================================

CREATE TABLE employees (

    employee_id                 INT PRIMARY KEY,

    age                         INT,
    attrition                   VARCHAR(10),
    business_travel             VARCHAR(50),
    department                  VARCHAR(100),
    distance_from_home          INT,
    education                   INT,
    education_field             VARCHAR(100),
    gender                      VARCHAR(20),
    job_level                   INT,
    job_role                    VARCHAR(100),
    marital_status              VARCHAR(50),
    monthly_income              INT,
    num_companies_worked        INT,
    percent_salary_hike         INT,
    total_working_years         INT,
    training_times_last_year    INT,
    years_at_company            INT,
    years_since_last_promotion  INT,
    years_with_curr_manager     INT
);

-- ============================================================
-- EMPLOYEE SURVEYS
-- ============================================================

CREATE TABLE employee_surveys (

    employee_id INT PRIMARY KEY,

    environment_satisfaction INT,
    job_satisfaction INT,
    work_life_balance INT,

    CONSTRAINT fk_employee_surveys
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE
);

-- ============================================================
-- MANAGER SURVEYS
-- ============================================================

CREATE TABLE manager_surveys (

    employee_id INT PRIMARY KEY,

    job_involvement INT,
    performance_rating INT,

    CONSTRAINT fk_manager_surveys
        FOREIGN KEY(employee_id)
        REFERENCES employees(employee_id)
        ON DELETE CASCADE
);

-- ============================================================
-- EMPLOYEE MASTER
-- Analytics Table
-- ============================================================

CREATE TABLE employee_master (

    employee_id                 INT PRIMARY KEY,

    age                         INT,
    attrition                   VARCHAR(10),
    business_travel             VARCHAR(50),
    department                  VARCHAR(100),
    distance_from_home          INT,
    education                   INT,
    education_field             VARCHAR(100),
    gender                      VARCHAR(20),
    job_level                   INT,
    job_role                    VARCHAR(100),
    marital_status              VARCHAR(50),
    monthly_income              INT,
    num_companies_worked        INT,
    percent_salary_hike         INT,
    total_working_years         INT,
    training_times_last_year    INT,
    years_at_company            INT,
    years_since_last_promotion  INT,
    years_with_curr_manager     INT,

    environment_satisfaction    INT,
    job_satisfaction            INT,
    work_life_balance           INT,
    job_involvement             INT,
    performance_rating          INT,

    age_group                   VARCHAR(20),
    income_band                 VARCHAR(20),
    experience_level            VARCHAR(20),
    promotion_status            VARCHAR(30),
    frequent_traveler           VARCHAR(10),
    long_commute                VARCHAR(10),
    high_salary_hike            VARCHAR(10),
    attrition_flag              INT
);

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================

SELECT 'PeoplePulse AI schema created successfully!' AS status;