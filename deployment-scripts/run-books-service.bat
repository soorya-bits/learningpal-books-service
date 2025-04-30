@echo off
setlocal enabledelayedexpansion

:: Configuration
set NETWORK_NAME=librarypal-net
set VOLUME_NAME=librarypal_mysql_data

set DB_CONTAINER=librarypal-db
set DB_IMAGE=mysql:8.0
set DB_PORT=3306
set DB_ROOT_PASSWORD=admin123
set DB_NAME=library

set PMA_CONTAINER=librarypal-db-admin
set PMA_IMAGE=phpmyadmin
set PMA_PORT=8080

set USER_CONTAINER=librarypal-books-service-container
set USER_IMAGE=librarypal-books-service
set USER_PORT=8001

:: MySQL env vars for books-service
set DB_USER=root
set DB_PASSWORD=%DB_ROOT_PASSWORD%
set DB_HOST=%DB_CONTAINER%

echo ➡️  Creating Docker network and volume if not exist...
docker network inspect %NETWORK_NAME% >nul 2>&1 || docker network create %NETWORK_NAME%
docker volume inspect %VOLUME_NAME% >nul 2>&1 || docker volume create %VOLUME_NAME%

:: Start MySQL container
docker ps -q -f name=%DB_CONTAINER% >nul
if not errorlevel 1 (
    echo 🐬 MySQL container "%DB_CONTAINER%" is already running.
) else (
    docker ps -aq -f name=%DB_CONTAINER% >nul
    if not errorlevel 1 (
        echo 🐬 Starting existing MySQL container...
        docker start %DB_CONTAINER%
    ) else (
        echo 🐬 Running new MySQL container...
        docker run -d ^
            --name %DB_CONTAINER% ^
            --network %NETWORK_NAME% ^
            -e MYSQL_ROOT_PASSWORD=%DB_ROOT_PASSWORD% ^
            -e MYSQL_DATABASE=%DB_NAME% ^
            -v %VOLUME_NAME%:/var/lib/mysql ^
            -p %DB_PORT%:3306 ^
            %DB_IMAGE%
    )
)

:: Start phpMyAdmin container
docker ps -q -f name=%PMA_CONTAINER% >nul
if not errorlevel 1 (
    echo 🧰 phpMyAdmin container "%PMA_CONTAINER%" is already running.
) else (
    docker ps -aq -f name=%PMA_CONTAINER% >nul
    if not errorlevel 1 (
        echo 🧰 Starting existing phpMyAdmin container...
        docker start %PMA_CONTAINER%
    ) else (
        echo 🧰 Running new phpMyAdmin container...
        docker run -d ^
            --name %PMA_CONTAINER% ^
            --network %NETWORK_NAME% ^
            -e PMA_HOST=%DB_CONTAINER% ^
            -e PMA_PORT=3306 ^
            -e MYSQL_ROOT_PASSWORD=%DB_ROOT_PASSWORD% ^
            -p %PMA_PORT%:80 ^
            %PMA_IMAGE%
    )
)

:: Restart books-service
echo 🧹 Stopping old books-service container (if any)...
docker rm -f %USER_CONTAINER% >nul 2>&1

echo 🔨 Building books-service image...
docker build -t %USER_IMAGE% .

echo 🚀 Starting books-service container...
docker run -d ^
    --name %USER_CONTAINER% ^
    --network %NETWORK_NAME% ^
    -e DB_USER=%DB_USER% ^
    -e DB_PASSWORD=%DB_PASSWORD% ^
    -e DB_HOST=%DB_HOST% ^
    -e DB_NAME=%DB_NAME% ^
    -p %USER_PORT%:%USER_PORT% ^
    %USER_IMAGE%

echo.
echo ✅ All services are up:
echo - MySQL:         localhost:%DB_PORT%
echo - phpMyAdmin:    http://localhost:%PMA_PORT%
echo - Books Service: http://localhost:%USER_PORT%

endlocal
pause
