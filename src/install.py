import os
import os.path
import stat
import string
import sys 

print 'Installing...\n'
print '--------------------------------\n'

print 'Installing Easy Install\n'
result = os.system('ez_setup.py')
if result != 0:
	print '\nInstall failed!'
	sys.exit(-1)

print 'Installing Scons\n'
result = os.system('ez_setup.py -f http://www.scons.org/ SCons')
if result != 0:
	print '\nInstall failed!'
	sys.exit(-1)

result = os.system('scons')
if result != 0:
	print '\nInstall failed!'
else:
	sys.exit(0)