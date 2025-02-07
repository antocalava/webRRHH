@echo off
setlocal

for /f "tokens=*" %%i in ('docker ps -q --filter "publish=8000"') do (
    set CONTAINER_ID=%%i
)
if defined CONTAINER_ID (
    docker stop %CONTAINER_ID%
    docker rm %CONTAINER_ID%
)

cd backend
docker build -t sebn_es_suite_backend .
cd ..
docker run -d -p 8000:8000 --name sebn_es_suite_backend_container sebn_es_suite_backend
pause
