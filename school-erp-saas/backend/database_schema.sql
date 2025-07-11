-- SaaS School ERP System Database Schema
-- Multi-tenant structure with role-based access

-- Schools (Tenants) Table
CREATE TABLE schools (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    subscription_plan ENUM('basic', 'premium', 'enterprise') DEFAULT 'basic',
    subscription_status ENUM('active', 'suspended', 'cancelled') DEFAULT 'active',
    subscription_start_date DATE,
    subscription_end_date DATE,
    monthly_fee DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_subdomain (subdomain),
    INDEX idx_subscription_status (subscription_status)
);

-- Branches Table
CREATE TABLE branches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    is_main_branch BOOLEAN DEFAULT FALSE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    INDEX idx_school_branch (school_id, status)
);

-- Users Table (Multi-role support)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    role ENUM('superadmin', 'admin', 'teacher', 'parent', 'student') NOT NULL,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE SET NULL,
    INDEX idx_user_school_role (school_id, role, status),
    INDEX idx_user_branch (branch_id),
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- Academic Years Table
CREATE TABLE academic_years (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    INDEX idx_school_year (school_id, is_current)
);

-- Classes Table
CREATE TABLE classes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    grade_level INT NOT NULL,
    capacity INT DEFAULT 30,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
    INDEX idx_school_class (school_id, branch_id, status)
);

-- Sections Table (Class sections per academic year)
CREATE TABLE sections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT NOT NULL,
    class_id INT NOT NULL,
    academic_year_id INT NOT NULL,
    section_name VARCHAR(10) NOT NULL, -- A, B, C, etc.
    teacher_id INT,
    max_students INT DEFAULT 30,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_section (class_id, academic_year_id, section_name),
    INDEX idx_section_school (school_id, branch_id)
);

-- Subjects Table
CREATE TABLE subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(20),
    description TEXT,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    INDEX idx_school_subject (school_id, status)
);

-- Class Subjects (Many-to-many relationship)
CREATE TABLE class_subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    class_id INT NOT NULL,
    subject_id INT NOT NULL,
    teacher_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_class_subject (class_id, subject_id),
    INDEX idx_class_teacher (class_id, teacher_id)
);

-- Students Table
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT NOT NULL,
    user_id INT NOT NULL,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    admission_date DATE,
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    blood_group VARCHAR(5),
    address TEXT,
    emergency_contact VARCHAR(20),
    medical_conditions TEXT,
    status ENUM('active', 'graduated', 'transferred', 'dropped') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_student_school (school_id, branch_id, status),
    INDEX idx_student_id (student_id)
);

-- Student Enrollments (Students in sections)
CREATE TABLE student_enrollments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    academic_year_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    status ENUM('active', 'transferred', 'dropped') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_year (student_id, academic_year_id),
    INDEX idx_enrollment_section (section_id, status)
);

-- Parents Table
CREATE TABLE parents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    user_id INT NOT NULL,
    relationship ENUM('father', 'mother', 'guardian', 'other') NOT NULL,
    occupation VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_parent_school (school_id)
);

-- Student Parent Relationships
CREATE TABLE student_parents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    student_id INT NOT NULL,
    parent_id INT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES parents(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_parent (student_id, parent_id),
    INDEX idx_student_parents (student_id)
);

-- Employees Table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT NOT NULL,
    user_id INT NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    designation VARCHAR(255),
    department VARCHAR(255),
    hire_date DATE,
    salary DECIMAL(10,2) DEFAULT 0.00,
    salary_type ENUM('monthly', 'hourly', 'daily') DEFAULT 'monthly',
    bank_account VARCHAR(50),
    account_type ENUM('bank', 'evc', 'cash') DEFAULT 'bank',
    status ENUM('active', 'inactive', 'terminated') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_employee_school (school_id, branch_id, status),
    INDEX idx_employee_id (employee_id)
);

-- Attendance Tables
CREATE TABLE student_attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'excused') NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    remarks TEXT,
    recorded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_student_date (student_id, date),
    INDEX idx_attendance_date (school_id, date),
    INDEX idx_attendance_section (section_id, date)
);

CREATE TABLE employee_attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    employee_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'half_day', 'sick_leave', 'vacation') NOT NULL,
    check_in_time TIME,
    check_out_time TIME,
    total_hours DECIMAL(4,2) DEFAULT 0.00,
    overtime_hours DECIMAL(4,2) DEFAULT 0.00,
    remarks TEXT,
    approved_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_employee_date (employee_id, date),
    INDEX idx_emp_attendance_date (school_id, date),
    INDEX idx_emp_attendance_employee (employee_id, date)
);

-- Payroll Tables
CREATE TABLE payroll_periods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status ENUM('draft', 'processed', 'paid') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    INDEX idx_payroll_period (school_id, status)
);

CREATE TABLE payroll_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    payroll_period_id INT NOT NULL,
    employee_id INT NOT NULL,
    basic_salary DECIMAL(10,2) NOT NULL,
    days_worked INT DEFAULT 0,
    total_days INT DEFAULT 0,
    overtime_hours DECIMAL(4,2) DEFAULT 0.00,
    overtime_rate DECIMAL(6,2) DEFAULT 0.00,
    gross_salary DECIMAL(10,2) DEFAULT 0.00,
    deductions DECIMAL(10,2) DEFAULT 0.00,
    bonuses DECIMAL(10,2) DEFAULT 0.00,
    paye_tax DECIMAL(10,2) DEFAULT 0.00,
    net_salary DECIMAL(10,2) DEFAULT 0.00,
    payment_status ENUM('pending', 'paid', 'cancelled') DEFAULT 'pending',
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (payroll_period_id) REFERENCES payroll_periods(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    UNIQUE KEY unique_payroll_employee (payroll_period_id, employee_id),
    INDEX idx_payroll_employee (employee_id, payment_status)
);

-- Deductions and Bonuses
CREATE TABLE employee_deductions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    employee_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type ENUM('fixed', 'percentage') DEFAULT 'fixed',
    is_recurring BOOLEAN DEFAULT TRUE,
    effective_date DATE,
    end_date DATE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    INDEX idx_deduction_employee (employee_id, status)
);

CREATE TABLE employee_bonuses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    employee_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type ENUM('fixed', 'percentage') DEFAULT 'fixed',
    award_date DATE,
    payroll_period_id INT,
    status ENUM('pending', 'paid') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (payroll_period_id) REFERENCES payroll_periods(id) ON DELETE SET NULL,
    INDEX idx_bonus_employee (employee_id, status)
);

-- Exams and Assessments
CREATE TABLE exams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    branch_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    type ENUM('online', 'offline') NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status ENUM('draft', 'published', 'ongoing', 'completed') DEFAULT 'draft',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES branches(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_exam_school (school_id, branch_id, status)
);

CREATE TABLE exam_subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    exam_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    max_marks INT DEFAULT 100,
    pass_marks INT DEFAULT 40,
    exam_date DATE,
    start_time TIME,
    duration_minutes INT DEFAULT 60,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_exam_subject_class (exam_id, subject_id, class_id)
);

CREATE TABLE student_exam_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    exam_subject_id INT NOT NULL,
    student_id INT NOT NULL,
    marks_obtained DECIMAL(5,2) DEFAULT 0.00,
    grade VARCHAR(5),
    remarks TEXT,
    recorded_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_subject_id) REFERENCES exam_subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE KEY unique_student_exam (exam_subject_id, student_id),
    INDEX idx_result_student (student_id)
);

-- Messaging System
CREATE TABLE messaging_providers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    type ENUM('sms', 'email', 'whatsapp') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE school_messaging_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    provider_id INT NOT NULL,
    api_key VARCHAR(500),
    sender_id VARCHAR(50),
    api_secret VARCHAR(500),
    webhook_url VARCHAR(500),
    unit_cost DECIMAL(8,4) DEFAULT 0.0000,
    balance DECIMAL(10,2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT FALSE,
    is_tested BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES messaging_providers(id) ON DELETE CASCADE,
    UNIQUE KEY unique_school_provider (school_id, provider_id),
    INDEX idx_school_messaging (school_id, is_active)
);

CREATE TABLE message_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    messaging_config_id INT NOT NULL,
    recipient_type ENUM('student', 'parent', 'teacher', 'employee', 'custom') NOT NULL,
    recipient_id INT,
    recipient_phone VARCHAR(20),
    recipient_email VARCHAR(255),
    message_type ENUM('sms', 'email', 'whatsapp') NOT NULL,
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status ENUM('pending', 'sent', 'failed', 'delivered') DEFAULT 'pending',
    cost DECIMAL(8,4) DEFAULT 0.0000,
    external_id VARCHAR(255),
    error_message TEXT,
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (messaging_config_id) REFERENCES school_messaging_config(id) ON DELETE CASCADE,
    INDEX idx_message_school (school_id, status),
    INDEX idx_message_recipient (recipient_type, recipient_id),
    INDEX idx_message_status (status, sent_at)
);

-- Notifications
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type ENUM('info', 'warning', 'success', 'error') DEFAULT 'info',
    target_type ENUM('all', 'role', 'specific_users', 'class', 'branch') NOT NULL,
    target_value VARCHAR(255), -- role name, user IDs, class ID, branch ID
    is_read BOOLEAN DEFAULT FALSE,
    created_by INT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_notification_school (school_id, target_type),
    INDEX idx_notification_target (target_type, target_value)
);

-- User Notifications (for tracking read status)
CREATE TABLE user_notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    notification_id INT NOT NULL,
    user_id INT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notification_id) REFERENCES notifications(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_notification (notification_id, user_id),
    INDEX idx_user_notifications (user_id, is_read)
);

-- School Billing
CREATE TABLE school_billing (
    id INT PRIMARY KEY AUTO_INCREMENT,
    school_id INT NOT NULL,
    billing_period_start DATE NOT NULL,
    billing_period_end DATE NOT NULL,
    subscription_fee DECIMAL(10,2) NOT NULL,
    messaging_cost DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'paid', 'overdue', 'cancelled') DEFAULT 'pending',
    due_date DATE,
    paid_date DATE,
    payment_method VARCHAR(100),
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    INDEX idx_billing_school (school_id, status),
    INDEX idx_billing_due (due_date, status)
);

-- Insert default messaging providers
INSERT INTO messaging_providers (name, type) VALUES
('Twilio SMS', 'sms'),
('Twilio WhatsApp', 'whatsapp'),
('Hormuud SMS', 'sms'),
('SMTP Email', 'email'),
('WhatsApp Cloud API', 'whatsapp');

-- Insert default superadmin school
INSERT INTO schools (name, subdomain, subscription_plan, subscription_status) VALUES
('SuperAdmin Portal', 'admin', 'enterprise', 'active');

-- Insert main branch for superadmin
INSERT INTO branches (school_id, name, is_main_branch) VALUES
(1, 'Main Office', TRUE);

-- Insert superadmin user
INSERT INTO users (school_id, branch_id, username, email, password_hash, first_name, last_name, role) VALUES
(1, 1, 'superadmin', 'admin@myerpsaas.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Super', 'Admin', 'superadmin');
-- Password: admin123