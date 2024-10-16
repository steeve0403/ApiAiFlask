
# Flask AI API - Documentation

## Description
This API facilitates interaction with one or more AI models through a user interface. The project provides features such as user authentication, 
API key management, and an admin role to control users and logs. This API is designed to be used with a separate project that manages the AI models, 
while this API acts as an intermediary between the user interface and the AI models.

## Features

- **User Management**: Sign up, login, logout, and role-based access control (admin/user).
- **API Keys**: Generation and management of API keys for authenticated users.
- **Authentication**: JSON Web Tokens (JWT) for secure user authentication.
- **Roles**: Admin and user roles, with specific permissions for each.
- **Logging**: Manage and view logs for user actions and API usage.

## Technology Stack

- **Framework**: Flask
- **Database**: Flask-SQLAlchemy (supports MySQL or SQLite by default)
- **Authentication**: Flask-JWT-Extended for JWT token management.
- **Migrations**: Flask-Migrate for database migrations.
- **API Documentation**: ReDoc (OpenAPI specifications)

## Requirements

- **Python 3.8+**
- **MySQL** or **SQLite**
- **pip** for installing Python packages

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/steeve0403/ApiAiFlask.git
   cd ApiAiFlask
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the environment:
   Create a `.env` file in the root directory and set the following environment variables:
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/dbname
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the server:
   ```bash
   flask run
   ```

## Usage

### Authentication
- **Sign up**: `/api/auth/signup` (POST)
- **Login**: `/api/auth/signin` (POST)
- **Logout**: `/api/auth/logout` (POST)

### Users (Admin only)
- **List users**: `/api/admin/users` (GET)
- **Deactivate/Activate user**: `/api/admin/users/<int:user_id>/deactivate` (PUT)

### API Keys
- **Generate API key**: `/api/keys/generate` (POST)
- **List API keys**: `/api/keys/all` (GET)

## API Documentation

Access the interactive API documentation (ReDoc) at:
```
http://localhost:5000/redoc
```
This documentation is automatically generated based on the OpenAPI specifications.

## Testing

To run the unit tests:
```bash
pytest
```

## Deployment

To deploy the application using **Docker**, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t ApiAiFlask.
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 ApiAiFlask
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any feature requests or improvements.

## License

This project is licensed under the MIT License.
