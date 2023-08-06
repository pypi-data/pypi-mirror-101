@ECHO OFF

REM TODO: CREATE %userprofile%\.awsee if not exits
REM TODO: CREATE %userprofile%\.awsee\tmp if not exits
if not exist %userprofile%\.awsee\tmp md %userprofile%\.awsee\tmp
DEL %userprofile%\.awsee\tmp\awseeos_*  >nul 2>&1

set external=0
for %%x in (%*) do (
   IF "%%~x"=="-nt" (
      set external=1
   )
   IF "%%~x"=="--new-terminal" (
      set external=1
   )
)

set myrnd=%random%
set mypid=pid_%myrnd%_pid
set FILE_NAME=%userprofile%/.awsee/tmp/awseeos_%myrnd%.txt

awseepy "%mypid%" %* > %FILE_NAME%

IF %external%==0 (
   for /f "tokens=* delims= " %%a in (%FILE_NAME%) do (
      %%a
   )
)
