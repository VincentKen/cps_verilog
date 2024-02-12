@echo OFF
set EDAUTILS_ROOT=%CD%
set EDAUTILS_LICENSE_FILE=%EDAUTILS_ROOT%\edautils.lic
set PATH=%EDAUTILS_ROOT%\bin;%PATH%
set CLASSPATH=%EDAUTILS_ROOT%\lib\testbenchgenerators.jar 
::set MAXMEM=2048
::set JAVA_FLAGS= -ms5m -Xmx%MAXMEM%m 


cmd.exe
