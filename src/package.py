import sys
import datetime
import tarfile
from os.path import basename, isdir
from os import listdir

if __name__=='__main__':
	if len(sys.argv) == 1:
		today = (datetime.date.today()).strftime("%Y_%m_%d")
		tarfilename = "build_" + today + ".tar"
	else:
		tarfilename = sys.argv[1]
	
	tar = tarfile.open("../builds/" + tarfilename, "w")

	tar.add('../src')
	tar.add('../doc')
	tar.add('../test')
	
	tar.close()

