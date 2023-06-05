import subprocess
cmd = ['"C:/Program Files/7-Zip/7z.exe"', 'a', '"D:/R.SAWB/.nc/File.zip"', '"D:/R.SAWB/.nc/cru_ts4.03.1901.2018.pre.dat.nc"', '-v97m']
sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=False)
#sp = subprocess.call(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
#result = subprocess.run(cmd, capture_output=True, text=True)
