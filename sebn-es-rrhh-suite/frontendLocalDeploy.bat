@echo off
setlocal

for /f "tokens=*" %%i in ('docker ps -q --filter "publish=8864"') do (
    set CONTAINER_ID=%%i
)
if defined CONTAINER_ID (
    docker stop %CONTAINER_ID%
    docker rm %CONTAINER_ID%
)
cd frontend
docker build -t sebn_es_suite_frontend .
cd ..
docker run -d -p 8864:8864 --name sebn_es_suite_frontend_container sebn_es_suite_frontend
pause