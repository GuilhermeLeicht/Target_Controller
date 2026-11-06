@echo off
setlocal
cd /d "%~dp0"
if not exist "icone.ico" (
  echo ERRO: Coloque seu icone na pasta deste projeto, com o nome icone.ico
  pause
  exit /b 1
)
py -m pip install --upgrade flask pyinstaller
if errorlevel 1 goto :erro
py -m PyInstaller --noconfirm --clean --onedir --noconsole --name "Target Controller" --icon "icone.ico" --add-data "static;static" app.py
if errorlevel 1 goto :erro
if not exist "dist\Target Controller\config.json" (
  echo { } > "dist\Target Controller\config.json"
)
echo.
echo COMPILACAO CONCLUIDA!
echo Executavel: dist\Target Controller\Target Controller.exe
echo Copie a pasta inteira para outro computador.
pause
exit /b 0
:erro
echo.
echo Ocorreu um erro. Confira as mensagens acima.
pause
exit /b 1
