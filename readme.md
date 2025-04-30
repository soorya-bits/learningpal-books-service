# Book Service

This application is a microservice designed to handle book-related operations such as book creation, retrieval, and updates. It is built to be lightweight, scalable, and easy to integrate with other services.

## Key Features
- Book creation, retrieval, and management
- RESTful API endpoints for seamless integration
- Lightweight and containerized for efficient deployment
- Supports running with or without Docker

## Prerequisites
- Docker installed on your system (if running with Docker)
- Basic knowledge of Docker commands (if applicable)

## Running the Application in Docker

### Steps for Windows and Mac:

1. Clone the repository:
  ```bash
  git clone https://github.com/soorya-bits/learningpal-books-service.git
  cd learningpal-books-service
  ```

2. Run the appropriate script based on your operating system:
   - **For Windows**: Run the `run-book-service.bat` script:
   ```cmd
   ./deployment-script/run-book-service.bat
   ```
   - **For macOS**: Run the `run-book-service.sh` script:
   ```bash
   ./deployment-script/run-book-service.sh
   ```

3. Access the application:
  Open your browser and navigate to `http://localhost:8001/docs`.

## Notes
- Ensure Docker Desktop is running on your system.