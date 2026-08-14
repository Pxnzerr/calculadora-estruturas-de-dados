@echo off
REM Script facilitador para execução da Calculadora no Windows

set PYTHON_EXE=C:\Users\tulul\AppData\Local\Programs\Python\Python312\python.exe

if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" main.py %*
) else (
    python main.py %*
)
