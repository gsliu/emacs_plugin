# 
# Test of the 'file' command
# $Id: file.cmd.in,v 1.1 2007/02/13 11:42:54 rockyb Exp $
#
set trace-commands on
cd .
file hanoi.py
info line
where 2
step 1+1
where 2
quit
