::##############################################################################
::
::    This program is distributed in the hope that it will be useful,
::    but WITHOUT ANY WARRANTY; without even the implied warranty of
::    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
::
::    Contact help@edautils.com you need more informattion/support
::##############################################################################


@echo off
IF "%EDAUTILS_ROOT%" == "" GOTO NOPATH

:YESPATH

set JAVA=java
set MAIN=com.eu.miscedautils.gentbvlog.GenTBVlog
%JAVA% %JAVA_FLAGS% %MAIN% %* 

GOTO END

:NOPATH
        @echo 'Environment variable EDAUTILS_ROOT is not set. Set it to the installation directory.'
        @echo 'Example: set EDAUTILS_ROOT=F:\edautils_toos\installdir'
        @echo 'Example: set PATH=%EDAUTILS_ROOT%\bin;%PATH%'
GOTO END

:END


