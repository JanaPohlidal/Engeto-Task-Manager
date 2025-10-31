Task Manager
Python application for task management with MySQL database.

Author: Jana Pohlidalová

## Prerequisites

Docker Desktop (https://www.docker.com/products/docker-desktop)


## Start application
bash
docker-compose run --rm app

An interactive menu will appear. Use Option 5 or press Ctrl+C to exit.
After launch, the application menu will appear. Press Ctrl+C to exit
**Note:** The `--rm` flag automatically removes the app container after exit. Your data remains safe in the MySQL database.


## Testing

### Run All Tests
bash
docker-compose run --rm app pytest tests/ -v


### Run Tests with Coverage Report
bash
docker-compose run --rm app pytest tests/ --cov=src --cov-report=term


### Run Specific Test File
bash
docker-compose run --rm app pytest tests/test_aktualizovat_ukol.py -v

**Note:** MySQL container automatically sets required permissions for test databases via the initialization script `mysql-init/init.sql`. No additional configuration is needed.


## Configuration
Default settings work out of the box. To customize:
bash
cp .env.example .env
nano .env


### Port Configuration
If port 3306 is already in use:
# In .env file:
MYSQL_PORT=3307


## Stopping the Application
bash
docker-compose down
Stop all containers (keeps data)

bash
docker-compose down -v
Stops containers and deletes all data (fresh start). Use -v flag only if you want to completely reset the database!


## Technology Stack
Python 3.13
MySQL 8.0
pytest 8.3.3
Docker & Docker Compose


