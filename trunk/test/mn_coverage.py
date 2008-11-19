import os, sys

if __name__ == '__main__':
	os.system('coverage.py -e')
	os.system('coverage.py -x mn_unittest.py')
	os.system('coverage.py -r -m mynotepad.py')