@echo off
REM Script facilitador para abrir a Interface Gráfica (GUI) da Calculadora

set PYTHON_EXE=C:\Users\tulul\AppData\Local\Programs\Python\Python312\pythonw.exe

if exist "%PYTHON_EXE%" (
    start "" "%PYTHON_EXE%" main.py --gui
) else (
    set PYTHON_EXE_FALLBACK=C:\Users\tulul\AppData\Local\Programs\Python\Python312\python.exe
    if exist "%PYTHON_EXE_FALLBACK%" (
        start "" "%PYTHON_EXE_FALLBACK%" main.py --gui
    ) else (
        python main.py --gui
    )
)
