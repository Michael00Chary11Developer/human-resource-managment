# Human Resource Management System

A comprehensive Django REST API for managing human resources, including personnel, recruitment, salary, and resource allocation.

## Features

- **Personnel Management**: Complete employee information management
- **Recruitment Process**: Track recruitment workflows and interviews
- **Salary Management**: Calculate and manage employee salaries
- **Resource Allocation**: Track company resources assigned to employees
- **REST API**: Full RESTful API with JWT authentication
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Technology Stack

- **Backend**: Django 5.1.1, Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL 15
- **Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **Containerization**: Docker & Docker Compose
- **Code Quality**: Pre-commit hooks (Black, isort, flake8, autoflake)

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd human-resource-managment
   ```

2. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

3. **Using Docker (Recommended)**
   ```bash
   docker-compose up --build
   ```

4. **Manual Installation**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

### API Endpoints

- **API Documentation**: http://localhost:8000/api/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **API Base**: http://localhost:8000/

#### Main Endpoints:
- `/personnel/` - Personnel management
- `/recruitment/` - Recruitment process
- `/salary/` - Salary management
- `/resources/` - Resource allocation

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=human_resource_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## API Usage

### Authentication

1. **Get JWT Token**:
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Use Token in Requests**:
   ```bash
   curl -H "Authorization: Bearer your_token_here" \
     http://localhost:8000/personnel/manage/
   ```

### Example API Calls

**Get all personnel**:
```bash
GET /personnel/manage/
```

**Create new personnel**:
```bash
POST /personnel/manage/
Content-Type: application/json

{
  "firstname": "John",
  "lastname": "Doe",
  "marital_status": "single",
  "have_child": false,
  "religion": "Islam",
  "phone_number": "+1234567890",
  "birth_date": "1990-01-01",
  "degree": "Bachelor",
  "field_of_study": "Computer Science",
  "career_records": "5 years experience",
  "position": "Developer",
  "level_for_position": "Senior",
  "date_of_employment": "2020-01-01"
}
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Quality

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency.

**Setup pre-commit:**
```bash
# Install pre-commit
pip install pre-commit

# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

**Pre-commit hooks include:**
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **autoflake**: Remove unused imports
- **trailing-whitespace**: Remove trailing whitespace
- **end-of-file-fixer**: Ensure files end with newline
- **check-added-large-files**: Prevent large files from being committed
- **gitlint**: Commit message linting

**Manual code formatting:**
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Remove unused imports
autoflake --remove-all-unused-imports --in-place -r .

# Run flake8 linting
flake8 .
```

## Security Features

- JWT Authentication
- Environment-based configuration
- Input validation and sanitization
- SQL injection protection
- XSS protection headers
- CSRF protection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Install pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```
4. Make your changes
5. Ensure all pre-commit hooks pass:
   ```bash
   pre-commit run --all-files
   ```
6. Add tests for new functionality
7. Submit a pull request

**Note**: All commits must pass pre-commit hooks before being accepted.

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact the development team.
