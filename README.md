loan_app/
│
├── app/
│   ├── api/
│   │   ├── auth.py               # Handles user registration, login
│   │   ├── loans.py              # Loan submission and status APIs
│   │   ├── admin.py              # Admin endpoints for loan approval/rejection
│   │
│   ├── core/
│   │   ├── config.py             # Configuration settings (database, JWT, etc.)
│   │   ├── security.py           # JWT token creation and verification
│   │
│   ├── models/
│   │   ├── user.py               # User model for SQLAlchemy
│   │   ├── loan.py               # Loan Application model for SQLAlchemy
│   │
│   ├── database/
│   │   ├── db.py                 # Database connection and session management
│   │
│   ├── tests/
│   │   ├── test_auth.py          # Unit tests for registration, login
│   │   ├── test_loans.py         # Unit tests for loan application and status
│   │   ├── test_admin.py         # Unit tests for admin actions
│   │
│   └── main.py                   # Main FastAPI application entry point
│
├── docker-compose.yml             # Docker setup for PostgreSQL and FastAPI
├── Dockerfile                     # Dockerfile for FastAPI service
├── requirements.txt               # Python dependencies
└── README.md                      # Instructions for running the project
