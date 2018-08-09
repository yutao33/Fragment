@echo off
set NUM=100
echo %NUM%
FOR /L %%a IN (1,1,%NUM%) DO (
	echo %%a
	start /b DictClient 127.0.0.1 4500 "crucial" > %%a.txt
	rem DictClient 127.0.0.1 4500 "crucial" > %%a.txt
)

set COUNT=0

:ec
tasklist |find "DictClient" /i > nul
if "%errorlevel%"=="1" goto str
ping -n 2 127.0.0.1 > nul
echo wait
set /a COUNT=%COUNT%+1
goto ec
:str

FOR /L %%a IN (1,1,%NUM%) DO (
	echo %%a
	@echo on
	type %%a.txt
	del %%a.txt
	@echo off
)

echo time=%COUNT%s



rem start /b DictClient 127.0.0.1 4500 "crucial"