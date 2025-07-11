# SaaS School ERP System

A comprehensive multi-tenant School ERP (Enterprise Resource Planning) system built with FastAPI backend and React.js frontend. This system supports multiple schools as tenants with subdomain-based access and role-based permissions.

## 🚀 Features

### 🏫 Multi-Tenant Architecture
- **Subdomain-based tenancy**: Each school gets its own subdomain (e.g., `greenhigh.myerpsaas.com`)
- **Isolated data**: Complete data isolation between schools
- **Scalable**: Supports unlimited schools on a single instance
- **Custom branding**: Each school can have its own logo and branding

### 👥 Role-Based Access Control
- **SuperAdmin**: System-wide management, school creation, subscription management
- **Admin**: School-level administration, user management, reports
- **Teacher**: Class management, attendance, grading, student records
- **Parent**: View children's information, attendance, grades, communication
- **Student**: View personal information, attendance, grades, assignments

### 📚 Core Modules

#### 🏢 School Management
- Multi-branch support per school
- School profile and settings management
- Subscription plan management (Basic, Premium, Enterprise)
- Billing and payment tracking

#### 👤 User Management
- Multi-role user system
- Profile management with avatar support
- Authentication with JWT tokens
- Password reset functionality

#### 🎓 Academic Management
- **Classes & Sections**: Grade-wise class organization with sections
- **Academic Years**: Year-wise academic session management
- **Subjects**: Subject management and teacher assignment
- **Student Enrollment**: Section-wise student enrollment per academic year

#### 👨‍🎓 Student Management
- Complete student profiles with medical information
- Parent-child relationship mapping
- Student ID generation and management
- Academic records and transcript generation

#### 👨‍🏫 Employee Management
- Employee profiles and designation management
- Department-wise organization
- Salary structure and payment details
- Multiple account types (Bank, EVC, Cash)

#### 📊 Attendance System
- **Student Attendance**: Daily attendance tracking with status (Present, Absent, Late, Excused)
- **Employee Attendance**: Staff attendance with overtime tracking
- **Bulk Operations**: Mass attendance marking
- **Reports**: Attendance reports and statistics

#### 💰 Payroll Management
- **Automated Calculations**: Attendance-based salary calculation
- **Deductions**: PAYE tax, pension, custom deductions
- **Bonuses**: Performance bonuses, allowances
- **Payment Tracking**: Payment status and history
- **Reports**: Payroll reports and payslips

#### 📝 Examination System
- **Online & Offline Exams**: Support for both examination modes
- **Subject-wise Exams**: Class and subject-specific examinations
- **Result Management**: Grade calculation and result processing
- **Report Cards**: Automated report card generation

#### 📱 Messaging System
- **Multi-Provider Support**: 
  - SMS: Twilio, Hormuud (Somalia)
  - Email: SMTP, SendGrid
  - WhatsApp: WhatsApp Business API
- **Cost Tracking**: Per-message cost calculation and balance management
- **Message Templates**: Pre-defined message templates
- **Bulk Messaging**: Send messages to groups (class, parents, staff)
- **Message History**: Complete message logs and delivery status

#### 🔔 Notification System
- **In-App Notifications**: Real-time notifications
- **Role-based Targeting**: Send notifications to specific roles
- **Read Status Tracking**: Track notification read status
- **Expiration Support**: Auto-expiring notifications

#### 💳 Billing & Subscription
- **Monthly/Yearly Billing**: Flexible billing cycles
- **Usage-based Pricing**: Messaging cost calculation
- **Payment Tracking**: Payment history and status
- **Subscription Management**: Plan upgrades and downgrades

### 📈 Dashboard & Reports
- **Role-specific Dashboards**: Customized views for each role
- **Real-time Statistics**: Live data updates
- **Charts & Graphs**: Visual data representation
- **Export Options**: PDF and Excel exports
- **Custom Reports**: Configurable report generation

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Primary database
- **Redis**: Caching and session management
- **Celery**: Background task processing
- **JWT**: Authentication and authorization
- **Pydantic**: Data validation and serialization

### Frontend (Coming Soon)
- **React.js**: Modern JavaScript library for UI
- **Tailwind CSS**: Utility-first CSS framework
- **Redux Toolkit**: State management
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Nginx**: Reverse proxy and load balancer
- **GitHub Actions**: CI/CD pipeline
- **AWS/DigitalOcean**: Cloud deployment

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- MySQL 8.0+
- Redis 7+

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/your-username/school-erp-saas.git
cd school-erp-saas
```

2. **Environment Configuration**
```bash
# Backend environment
cp backend/.env.example backend/.env
# Edit backend/.env with your configurations
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- API Documentation: http://localhost:8000/api/v1/docs
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000 (when implemented)
- MySQL: localhost:3306
- Redis: localhost:6379

### Manual Setup

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Database setup**
```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE school_erp_saas;"
mysql -u root -p school_erp_saas < database_schema.sql
mysql -u root -p school_erp_saas < sample_data.sql
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env file with your database and other configurations
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔐 Default Login Credentials

### SuperAdmin Portal (admin.myerpsaas.com)
- **Email**: admin@myerpsaas.com
- **Password**: admin123
- **Role**: SuperAdmin

### Sample School (greenvalley.myerpsaas.com)
- **Admin Email**: admin@greenvalley.edu
- **Password**: admin123
- **Role**: Admin

### Test Users
- **Teacher**: mary@greenvalley.edu / admin123
- **Parent**: james.doe@email.com / admin123
- **Student**: alex.doe@email.com / admin123

## 📖 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Multi-tenant login
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

#### Dashboard
- `GET /api/v1/dashboard/stats` - Role-based dashboard statistics
- `GET /api/v1/dashboard/attendance-summary` - Today's attendance summary

#### Schools (SuperAdmin only)
- `GET /api/v1/schools` - List all schools
- `POST /api/v1/schools` - Create new school
- `PUT /api/v1/schools/{id}` - Update school
- `DELETE /api/v1/schools/{id}` - Delete school

## 🗄️ Database Schema

The system uses a comprehensive database schema with 25+ tables:

### Core Tables
- `schools` - Tenant information
- `branches` - School branches
- `users` - Multi-role user accounts
- `students` - Student profiles
- `employees` - Staff information
- `parents` - Parent information

### Academic Tables
- `academic_years` - Academic sessions
- `classes` - Grade levels
- `sections` - Class sections
- `subjects` - Subject management
- `student_enrollments` - Student-section mapping

### Operational Tables
- `student_attendance` - Student attendance records
- `employee_attendance` - Staff attendance records
- `payroll_periods` - Payroll cycles
- `payroll_records` - Salary calculations
- `exams` - Examination management
- `student_exam_results` - Exam results

### Communication Tables
- `messaging_providers` - SMS/Email providers
- `school_messaging_config` - Tenant messaging settings
- `message_logs` - Message history
- `notifications` - In-app notifications

## 🔧 Configuration

### Environment Variables

Key environment variables for configuration:

```env
# Database
DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/school_erp_saas

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Multi-tenant
MAIN_DOMAIN=myerpsaas.com
DEFAULT_SUBDOMAIN=admin

# Messaging
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
SENDGRID_API_KEY=your-sendgrid-key

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
```bash
# Set production environment variables
export ENVIRONMENT=production
export DATABASE_URL=your-production-db-url
export JWT_SECRET_KEY=your-production-secret
```

2. **Docker Production Build**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Database Migration**
```bash
# Run database migrations
docker exec -it school-erp-backend alembic upgrade head
```

### Scaling Considerations

- **Database**: Use managed MySQL service (AWS RDS, Google Cloud SQL)
- **Redis**: Use managed Redis service (AWS ElastiCache, Redis Cloud)
- **File Storage**: Use object storage (AWS S3, Google Cloud Storage)
- **Load Balancing**: Use nginx or AWS ALB for load balancing
- **Monitoring**: Implement logging and monitoring (ELK stack, Prometheus)

## 📊 Features Roadmap

### Phase 1 (Current)
- ✅ Multi-tenant architecture
- ✅ Role-based authentication
- ✅ Basic CRUD operations
- ✅ Dashboard with statistics
- ✅ Database schema and models

### Phase 2 (In Progress)
- 🔄 Complete API endpoints
- 🔄 React.js frontend
- 🔄 Messaging system integration
- 🔄 Payroll calculations
- 🔄 Report generation

### Phase 3 (Planned)
- 📅 Mobile app (React Native)
- 📅 Advanced reporting
- 📅 AI-powered insights
- 📅 Integration APIs
- 📅 Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- 📧 Email: support@myerpsaas.com
- 📖 Documentation: [Wiki](https://github.com/your-username/school-erp-saas/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/school-erp-saas/issues)

## 🏆 Acknowledgments

- FastAPI team for the amazing framework
- SQLAlchemy for the powerful ORM
- Tailwind CSS for the beautiful styling
- All contributors and supporters

---

**Made with ❤️ for educational institutions worldwide**