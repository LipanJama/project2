-- Sample Data for SaaS School ERP System

-- Sample Schools
INSERT INTO schools (name, subdomain, logo_url, address, phone, email, subscription_plan, subscription_status, subscription_start_date, subscription_end_date, monthly_fee) VALUES
('Green Valley High School', 'greenvalley', 'https://example.com/logos/greenvalley.png', '123 Education St, City', '+1234567890', 'admin@greenvalley.edu', 'premium', 'active', '2024-01-01', '2024-12-31', 299.99),
('Sunrise Elementary', 'sunrise', 'https://example.com/logos/sunrise.png', '456 Learning Ave, Town', '+1234567891', 'office@sunrise.edu', 'basic', 'active', '2024-01-15', '2024-12-31', 199.99),
('Tech Innovation Academy', 'techinnovation', 'https://example.com/logos/tech.png', '789 Future Blvd, Metro', '+1234567892', 'contact@techinnovation.edu', 'enterprise', 'active', '2024-01-01', '2024-12-31', 499.99);

-- Sample Branches
INSERT INTO branches (school_id, name, address, phone, email, is_main_branch, status) VALUES
-- Green Valley branches
(2, 'Main Campus', '123 Education St, City', '+1234567890', 'main@greenvalley.edu', TRUE, 'active'),
(2, 'North Branch', '124 North Education St, City', '+1234567893', 'north@greenvalley.edu', FALSE, 'active'),
-- Sunrise branches
(3, 'Central Campus', '456 Learning Ave, Town', '+1234567891', 'central@sunrise.edu', TRUE, 'active'),
-- Tech Innovation branches
(4, 'Main Campus', '789 Future Blvd, Metro', '+1234567892', 'main@techinnovation.edu', TRUE, 'active'),
(4, 'Research Wing', '790 Innovation St, Metro', '+1234567894', 'research@techinnovation.edu', FALSE, 'active');

-- Sample Academic Years
INSERT INTO academic_years (school_id, name, start_date, end_date, is_current, status) VALUES
(2, '2023-2024', '2023-09-01', '2024-06-30', FALSE, 'active'),
(2, '2024-2025', '2024-09-01', '2025-06-30', TRUE, 'active'),
(3, '2023-2024', '2023-09-01', '2024-06-30', FALSE, 'active'),
(3, '2024-2025', '2024-09-01', '2025-06-30', TRUE, 'active'),
(4, '2023-2024', '2023-09-01', '2024-06-30', FALSE, 'active'),
(4, '2024-2025', '2024-09-01', '2025-06-30', TRUE, 'active');

-- Sample Users (Admin, Teachers, Parents, Students)
INSERT INTO users (school_id, branch_id, username, email, password_hash, first_name, last_name, phone, role, status) VALUES
-- Green Valley Users
(2, 2, 'gv_admin', 'admin@greenvalley.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'John', 'Smith', '+1234567890', 'admin', 'active'),
(2, 2, 'teacher_mary', 'mary@greenvalley.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Mary', 'Johnson', '+1234567895', 'teacher', 'active'),
(2, 2, 'teacher_david', 'david@greenvalley.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'David', 'Wilson', '+1234567896', 'teacher', 'active'),
(2, 2, 'teacher_sarah', 'sarah@greenvalley.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Sarah', 'Brown', '+1234567897', 'teacher', 'active'),
(2, 2, 'parent_james', 'james.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'James', 'Doe', '+1234567898', 'parent', 'active'),
(2, 2, 'parent_jane', 'jane.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Jane', 'Doe', '+1234567899', 'parent', 'active'),
(2, 2, 'student_alex', 'alex.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Alex', 'Doe', '+1234567900', 'student', 'active'),
(2, 2, 'student_emma', 'emma.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Emma', 'Doe', '+1234567901', 'student', 'active'),
-- Sunrise Users
(3, 4, 'sunrise_admin', 'admin@sunrise.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Lisa', 'Anderson', '+1234567891', 'admin', 'active'),
(3, 4, 'teacher_mike', 'mike@sunrise.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Mike', 'Taylor', '+1234567902', 'teacher', 'active'),
-- Tech Innovation Users
(4, 5, 'tech_admin', 'admin@techinnovation.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Robert', 'Chen', '+1234567892', 'admin', 'active'),
(4, 5, 'teacher_anna', 'anna@techinnovation.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5SvIu', 'Anna', 'Garcia', '+1234567903', 'teacher', 'active');

-- Sample Classes
INSERT INTO classes (school_id, branch_id, name, grade_level, capacity, status) VALUES
-- Green Valley Classes
(2, 2, 'Grade 9', 9, 30, 'active'),
(2, 2, 'Grade 10', 10, 30, 'active'),
(2, 2, 'Grade 11', 11, 25, 'active'),
(2, 2, 'Grade 12', 12, 25, 'active'),
(2, 3, 'Grade 9', 9, 30, 'active'),
(2, 3, 'Grade 10', 10, 30, 'active'),
-- Sunrise Classes
(3, 4, 'Grade 1', 1, 25, 'active'),
(3, 4, 'Grade 2', 2, 25, 'active'),
(3, 4, 'Grade 3', 3, 25, 'active'),
-- Tech Innovation Classes
(4, 5, 'Computer Science 101', 11, 20, 'active'),
(4, 5, 'Advanced Programming', 12, 15, 'active');

-- Sample Sections
INSERT INTO sections (school_id, branch_id, class_id, academic_year_id, section_name, teacher_id, max_students, status) VALUES
-- Green Valley Sections (2024-2025 academic year)
(2, 2, 1, 2, 'A', 3, 30, 'active'),  -- Grade 9-A with Mary Johnson
(2, 2, 1, 2, 'B', 4, 30, 'active'),  -- Grade 9-B with David Wilson
(2, 2, 2, 2, 'A', 5, 30, 'active'),  -- Grade 10-A with Sarah Brown
(2, 2, 3, 2, 'A', 3, 25, 'active'),  -- Grade 11-A with Mary Johnson
(2, 2, 4, 2, 'A', 4, 25, 'active'),  -- Grade 12-A with David Wilson
-- Sunrise Sections
(3, 4, 7, 4, 'A', 10, 25, 'active'), -- Grade 1-A with Mike Taylor
(3, 4, 8, 4, 'A', 10, 25, 'active'), -- Grade 2-A with Mike Taylor
-- Tech Innovation Sections
(4, 5, 10, 6, 'A', 12, 20, 'active'), -- CS 101-A with Anna Garcia
(4, 5, 11, 6, 'A', 12, 15, 'active'); -- Advanced Programming-A with Anna Garcia

-- Sample Subjects
INSERT INTO subjects (school_id, name, code, description, status) VALUES
-- Green Valley Subjects
(2, 'Mathematics', 'MATH', 'Mathematics curriculum', 'active'),
(2, 'English', 'ENG', 'English Language and Literature', 'active'),
(2, 'Physics', 'PHY', 'Physics curriculum', 'active'),
(2, 'Chemistry', 'CHEM', 'Chemistry curriculum', 'active'),
(2, 'Biology', 'BIO', 'Biology curriculum', 'active'),
(2, 'History', 'HIST', 'World and National History', 'active'),
-- Sunrise Subjects
(3, 'Basic Mathematics', 'MATH1', 'Elementary Mathematics', 'active'),
(3, 'Reading', 'READ', 'Reading and Comprehension', 'active'),
(3, 'Science', 'SCI', 'Basic Science', 'active'),
-- Tech Innovation Subjects
(4, 'Computer Programming', 'PROG', 'Programming fundamentals', 'active'),
(4, 'Data Structures', 'DS', 'Data Structures and Algorithms', 'active'),
(4, 'Web Development', 'WEB', 'Web Development Technologies', 'active');

-- Sample Employees
INSERT INTO employees (school_id, branch_id, user_id, employee_id, designation, department, hire_date, salary, salary_type, bank_account, account_type, status) VALUES
-- Green Valley Employees
(2, 2, 2, 'GV001', 'Principal', 'Administration', '2023-01-15', 5000.00, 'monthly', 'ACC001234', 'bank', 'active'),
(2, 2, 3, 'GV002', 'Senior Teacher', 'Science Department', '2023-02-01', 3500.00, 'monthly', 'ACC001235', 'bank', 'active'),
(2, 2, 4, 'GV003', 'Mathematics Teacher', 'Mathematics Department', '2023-02-15', 3200.00, 'monthly', 'ACC001236', 'bank', 'active'),
(2, 2, 5, 'GV004', 'English Teacher', 'Language Department', '2023-03-01', 3200.00, 'monthly', 'ACC001237', 'evc', 'active'),
-- Sunrise Employees
(3, 4, 9, 'SR001', 'Head Teacher', 'Administration', '2023-01-10', 4500.00, 'monthly', 'ACC002001', 'bank', 'active'),
(3, 4, 10, 'SR002', 'Elementary Teacher', 'Primary Education', '2023-01-20', 2800.00, 'monthly', 'ACC002002', 'bank', 'active'),
-- Tech Innovation Employees
(4, 5, 11, 'TI001', 'Director', 'Administration', '2023-01-01', 6000.00, 'monthly', 'ACC003001', 'bank', 'active'),
(4, 5, 12, 'TI002', 'Computer Science Instructor', 'Technology Department', '2023-01-15', 4000.00, 'monthly', 'ACC003002', 'bank', 'active');

-- Sample Students
INSERT INTO students (school_id, branch_id, user_id, student_id, admission_date, date_of_birth, gender, blood_group, address, emergency_contact, status) VALUES
-- Green Valley Students
(2, 2, 7, 'GV2024001', '2024-01-15', '2008-05-15', 'male', 'O+', '123 Student St, City', '+1234567898', 'active'),
(2, 2, 8, 'GV2024002', '2024-01-15', '2008-08-22', 'female', 'A+', '124 Student St, City', '+1234567899', 'active');

-- Sample Parents
INSERT INTO parents (school_id, user_id, relationship, occupation, address) VALUES
(2, 6, 'father', 'Engineer', '123 Student St, City'),
(2, 7, 'mother', 'Teacher', '124 Student St, City');

-- Sample Student-Parent Relationships
INSERT INTO student_parents (school_id, student_id, parent_id, is_primary) VALUES
(2, 1, 1, TRUE),  -- Alex Doe - James Doe (father)
(2, 2, 2, TRUE);  -- Emma Doe - Jane Doe (mother)

-- Sample Student Enrollments
INSERT INTO student_enrollments (school_id, student_id, section_id, academic_year_id, enrollment_date, status) VALUES
(2, 1, 1, 2, '2024-09-01', 'active'),  -- Alex in Grade 9-A
(2, 2, 1, 2, '2024-09-01', 'active');  -- Emma in Grade 9-A

-- Sample Employee Attendance (Last 30 days)
INSERT INTO employee_attendance (school_id, employee_id, date, status, check_in_time, check_out_time, total_hours, overtime_hours) VALUES
-- Green Valley Principal attendance
(2, 1, '2024-01-01', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-02', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-03', 'present', '08:00:00', '17:30:00', 8.50, 0.50),
(2, 1, '2024-01-04', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-05', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-08', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-09', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-10', 'sick_leave', NULL, NULL, 0.00, 0.00),
(2, 1, '2024-01-11', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
(2, 1, '2024-01-12', 'present', '08:00:00', '17:00:00', 8.00, 0.00),
-- Mary Johnson attendance
(2, 2, '2024-01-01', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-02', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-03', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-04', 'late', '09:00:00', '16:30:00', 7.50, 0.00),
(2, 2, '2024-01-05', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-08', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-09', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-10', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-11', 'present', '08:30:00', '16:30:00', 8.00, 0.00),
(2, 2, '2024-01-12', 'present', '08:30:00', '16:30:00', 8.00, 0.00);

-- Sample Student Attendance
INSERT INTO student_attendance (school_id, student_id, section_id, date, status, check_in_time, recorded_by) VALUES
-- Alex Doe attendance
(2, 1, 1, '2024-01-01', 'present', '08:45:00', 3),
(2, 1, 1, '2024-01-02', 'present', '08:45:00', 3),
(2, 1, 1, '2024-01-03', 'present', '08:45:00', 3),
(2, 1, 1, '2024-01-04', 'late', '09:15:00', 3),
(2, 1, 1, '2024-01-05', 'present', '08:45:00', 3),
-- Emma Doe attendance
(2, 2, 1, '2024-01-01', 'present', '08:40:00', 3),
(2, 2, 1, '2024-01-02', 'present', '08:40:00', 3),
(2, 2, 1, '2024-01-03', 'absent', NULL, 3),
(2, 2, 1, '2024-01-04', 'present', '08:40:00', 3),
(2, 2, 1, '2024-01-05', 'present', '08:40:00', 3);

-- Sample Payroll Periods
INSERT INTO payroll_periods (school_id, name, start_date, end_date, status) VALUES
(2, 'January 2024', '2024-01-01', '2024-01-31', 'processed'),
(2, 'February 2024', '2024-02-01', '2024-02-29', 'draft'),
(3, 'January 2024', '2024-01-01', '2024-01-31', 'processed'),
(4, 'January 2024', '2024-01-01', '2024-01-31', 'processed');

-- Sample Employee Deductions
INSERT INTO employee_deductions (school_id, employee_id, name, amount, type, is_recurring, effective_date, status) VALUES
(2, 1, 'PAYE Tax', 15.00, 'percentage', TRUE, '2024-01-01', 'active'),
(2, 1, 'Pension Contribution', 5.00, 'percentage', TRUE, '2024-01-01', 'active'),
(2, 2, 'PAYE Tax', 12.00, 'percentage', TRUE, '2024-01-01', 'active'),
(2, 2, 'Pension Contribution', 5.00, 'percentage', TRUE, '2024-01-01', 'active'),
(2, 3, 'PAYE Tax', 10.00, 'percentage', TRUE, '2024-01-01', 'active'),
(2, 4, 'PAYE Tax', 10.00, 'percentage', TRUE, '2024-01-01', 'active');

-- Sample Employee Bonuses
INSERT INTO employee_bonuses (school_id, employee_id, name, amount, type, award_date, status) VALUES
(2, 1, 'Performance Bonus', 1000.00, 'fixed', '2024-01-15', 'paid'),
(2, 2, 'Teaching Excellence Award', 500.00, 'fixed', '2024-01-20', 'paid'),
(2, 3, 'Perfect Attendance Bonus', 200.00, 'fixed', '2024-01-25', 'pending');

-- Sample Payroll Records
INSERT INTO payroll_records (school_id, payroll_period_id, employee_id, basic_salary, days_worked, total_days, overtime_hours, overtime_rate, gross_salary, deductions, bonuses, paye_tax, net_salary, payment_status) VALUES
-- January 2024 Green Valley payroll
(2, 1, 1, 5000.00, 22, 23, 2.00, 50.00, 5100.00, 1000.00, 1000.00, 750.00, 4350.00, 'paid'),
(2, 1, 2, 3500.00, 23, 23, 0.00, 0.00, 3500.00, 595.00, 500.00, 420.00, 3485.00, 'paid'),
(2, 1, 3, 3200.00, 23, 23, 0.00, 0.00, 3200.00, 320.00, 0.00, 320.00, 2560.00, 'paid'),
(2, 1, 4, 3200.00, 23, 23, 0.00, 0.00, 3200.00, 320.00, 0.00, 320.00, 2560.00, 'paid');

-- Sample Exams
INSERT INTO exams (school_id, branch_id, name, type, description, start_date, end_date, status, created_by) VALUES
(2, 2, 'Mid-term Examination 2024', 'offline', 'First semester mid-term examination', '2024-03-15', '2024-03-22', 'completed', 2),
(2, 2, 'Final Examination 2024', 'offline', 'First semester final examination', '2024-06-10', '2024-06-20', 'draft', 2),
(4, 5, 'Programming Assessment', 'online', 'Online programming skills assessment', '2024-02-01', '2024-02-05', 'completed', 11);

-- Sample School Messaging Configuration
INSERT INTO school_messaging_config (school_id, provider_id, api_key, sender_id, unit_cost, balance, is_active, is_tested) VALUES
(2, 1, 'test_twilio_key_123', 'GreenValley', 0.0500, 1000.00, TRUE, TRUE),
(2, 4, 'smtp_config_456', 'noreply@greenvalley.edu', 0.0100, 5000.00, TRUE, TRUE),
(3, 3, 'hormuud_api_789', 'Sunrise', 0.0300, 500.00, TRUE, TRUE),
(4, 1, 'twilio_tech_abc', 'TechAcademy', 0.0500, 2000.00, TRUE, TRUE);

-- Sample Message Logs
INSERT INTO message_logs (school_id, messaging_config_id, recipient_type, recipient_id, recipient_phone, message_type, subject, message, status, cost, sent_at) VALUES
(2, 1, 'parent', 1, '+1234567898', 'sms', NULL, 'Reminder: Parent-teacher meeting tomorrow at 3 PM', 'delivered', 0.0500, '2024-01-15 10:00:00'),
(2, 2, 'parent', 1, 'james.doe@email.com', 'email', 'School Fee Reminder', 'Dear parent, this is a reminder about the upcoming school fee payment due date.', 'delivered', 0.0100, '2024-01-15 10:05:00'),
(3, 3, 'teacher', 10, '+1234567902', 'sms', NULL, 'Staff meeting scheduled for tomorrow at 9 AM', 'delivered', 0.0300, '2024-01-16 08:00:00');

-- Sample Notifications
INSERT INTO notifications (school_id, title, message, type, target_type, target_value, created_by, expires_at) VALUES
(2, 'Welcome to Green Valley High School', 'Welcome to the new academic year. We wish you success in your studies.', 'info', 'all', NULL, 2, '2024-12-31 23:59:59'),
(2, 'Exam Schedule Released', 'The mid-term examination schedule has been published. Please check your dashboard.', 'warning', 'role', 'student', 2, '2024-03-15 23:59:59'),
(3, 'New Teacher Orientation', 'All new teachers must attend the orientation session on Monday.', 'info', 'role', 'teacher', 9, '2024-02-01 23:59:59'),
(4, 'System Maintenance', 'The system will be under maintenance this weekend. Please save your work.', 'warning', 'all', NULL, 11, '2024-01-20 23:59:59');

-- Sample School Billing
INSERT INTO school_billing (school_id, billing_period_start, billing_period_end, subscription_fee, messaging_cost, total_amount, status, due_date, paid_date, payment_method, transaction_id) VALUES
(2, '2024-01-01', '2024-01-31', 299.99, 15.50, 315.49, 'paid', '2024-02-01', '2024-01-28', 'Credit Card', 'TXN_GV_202401_001'),
(3, '2024-01-01', '2024-01-31', 199.99, 8.20, 208.19, 'paid', '2024-02-01', '2024-01-30', 'Bank Transfer', 'TXN_SR_202401_001'),
(4, '2024-01-01', '2024-01-31', 499.99, 22.50, 522.49, 'paid', '2024-02-01', '2024-01-25', 'Credit Card', 'TXN_TI_202401_001'),
(2, '2024-02-01', '2024-02-29', 299.99, 0.00, 299.99, 'pending', '2024-03-01', NULL, NULL, NULL);