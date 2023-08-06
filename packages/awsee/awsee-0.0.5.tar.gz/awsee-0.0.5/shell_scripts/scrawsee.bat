@ECHO OFF
for /F "tokens=1,30* delims=" %%i in ('awseepy') do (
    echo %%i
    echo."UALTER;OK"
    REM ECHO %%i | findstr /C:"AWS_">nul && (
    REM     echo %%i
    REM     SET "%%i"
    REM )
)
