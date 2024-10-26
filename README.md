# Loan Application API

This is a FastAPI application that allows users to apply for loans and enables admins to manage these applications. The application features user registration, login, loan application submission, and admin capabilities for approving/rejecting applications.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Using Docker](#using-docker)
- [API Endpoints](#api-endpoints)
- [Role-Based Access Control](#role-based-access-control)
- [Running Tests](#running-tests)
- [Using Docker](#using-docker)
- [Testing in local(without docker)](#testing-in-local)

## Features

- User registration and login with JWT authentication.
- Users can submit loan applications and view their statuses.
- Admins can approve or reject loan applications and view all applications.
- Pagination for loan application lists.
- API rate limiting to prevent abuse.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pytest for testing

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd loan_application_api



## API Endpoints
1. **User Registration:**
POST /register - Register a new user.

2. **User Login:**
POST /login - Login to get a JWT token.

3. **Submit Loan Application:**
POST /apply - Submit a loan application (user role).

4. **View Loan Application Status:**
GET /status/{application_id} - View the status of a specific loan application (user role).

5. **Admin Approve/Reject Loan Application:**
POST /admin/application/{application_id}/approve - Approve a loan application.
POST /admin/application/{application_id}/reject - Reject a loan application.

6. **View All Loan Applications:**
GET /admin/applications - View all loan applications (admin role).


## role-based-access-control

**User Role:**
Users can register and log in.
Users can submit loan applications and view the status of their own applications.

**Admin Role:**
Admins can log in and view all loan applications.
Admins can approve or reject loan applications.

## running-tests
use the below command to run
pytest


## using docker
To run the application using Docker, follow these steps:

**Build the Docker Image: In the project root directory, run:**

docker build -t loan_application_api .

**Run the Docker Container: Start the container with:**

docker run -d -p 8000:8000 --name loan_application_api loan_application_api

Access the Application: Open your web browser and navigate to http://localhost:8000/docs to access the API documentation.

**Stop and Remove the Container: To stop the container, run:**

docker stop loan_application_api

**To remove the container, run:**

docker rm loan_application_api


## testing-in-local

1. Create a PostgreSQL Database: Ensure that PostgreSQL is installed and running. Create a database named loandb:

psql -U postgres -c "CREATE DATABASE loan_app;"

2. Install Dependencies: If you are not using Docker, install the required dependencies:
pip install -r requirements.txt

4. Set Up the below URL.
SQLALCHEMY_DATABASE_URL=postgresql://<username>:<password>@localhost:5432/loandb