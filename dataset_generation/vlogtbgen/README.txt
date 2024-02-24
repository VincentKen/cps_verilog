 

**************************************************************************
*                                                                        *
*                   Verilog Testbench Generator                          *
*                 Copyright (C) 2012-2015, edautils.com                  *
*                                                                        *
**************************************************************************

Welcome to the free Verilog Testbench Generator utility!  This utility
is meant for those verilog users who wants to analyze, elaborate and
simulate their verilog top module. This testbench generator has been
implemented in Java and this utility has been packaged as a JAR file.
Goto installation area and source/run the setup_env file to setup
the environment for this tool.

    Alternatively for Unix
    setenv EDAUTILS_ROOT /usr/user1/DesignPlayer-linux.x86/01MAY2014 ( this installation directory )
    set path = ( $EDAUTILS_ROOT/bin $path ) 

    And for Windows 

    set EDAUTILS_ROOT=D:\tmp\DesignPlayer-win32.x86_64\01MAY2014 ( this installation directory )
    set PATH="%path%;%EDAUTILS_ROOT%\bin"

You need to execute this utility as -

    gentbvlog -in simple_and.v -top simple_and -out edautils_tech_tb.v [+incdir+dir1+dir2] -clk "clk1@8{in1:in2}" -clk clk2 -rst rst1 -rst "rst2{1@5:0@50:1@150}"  

				OR

    java com.eu.miscedautils.gentbvlog.GenTBVlog -in simple_and.v -top simple_and -out edautils_tech_tb.v [+incdir+dir1+dir2] -clk "clk1@8{in1:in2}" -clk clk2 -rst rst1 -rst "rst2{1@5:0@50:1@150}" 

In the above example 'clk1' is one of the clock with period interval 8 time
unit. The 'rst2' is the reset which will get value '1' at 5, then '0' after 50
and then '1' again after 150 time unit.

Examples
========
    Have a look onto the examples directory to get a better understanding
of this tool. 

License Setting
===============
    Set the EDAUTILS_LICENSE_KEY environment variable before running the tool.
    You may refer the page www.computerhope.com/issues/ch000549.htm to know howto set
    environment variables in Windows.

FEEDBACK
========
Send feedback to help@edautils.com

 
