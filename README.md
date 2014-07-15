pilpres2014
===========

python based code to download C1 form to support transparancy of Indonesia President election.

How to use :<br>
1. Determine your Operating System, either Windows, Mac OS X or Linux/*nix.<br>
2. Download python 2.7.x for your OS, not 3.x !<br>
<a href="https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi">Python for windows</a><br>
<a href="https://www.python.org/download/releases/2.7.8/">Python for Mac OS X</a><br>
<a href="https://www.python.org/download/releases/2.7.8/">Python for Linux/*nix</a><br>
3. Setup environment for Python : <a href="http://docs.python-guide.org/en/latest/starting/install/win/">instruction</a> or here are the summaries for windows OS :<br>
	a. Install the downloaded installer by double click the installer file. The file should look like this : python-2.7.8.msi.<br>
	b. follow on-screen instruction, use the default configuration.<br>
	c. open your command prompt by : hit [window button]+R at the same time. A RUN dialog box will appears, type 'cmd' and hit ENTER.<br>
	d. command prompt dialog box will appears.<br>
	e. type the following : [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")<br>
	f. type 'python' and hit ENTER. if you see the following output that mean you have successfully install python. Yeaayy! Now you can go to step h.<br>
	Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32<br>
	Type "help", "copyright", "credits" or "license" for more information.<br>
	>>><br>
	<br>
	If you do not see that message, do not be scare, we could use another way to run the script.<br>
	g. if you do not see that message, make sure that you have to go to python directory in order to run PYTHON. here's how to do it: in command prompt, type 'cd c:\python27\'. if you prompt look like : "c:\Python27>", then you are on the right track, otherwise, make sure python27 is the same directory which you entered in the installation proccess.<br>
	h. download these files and save it to your python directory : <br>
		1. <a href="https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py">ez_setup.py</a><br>
		2. <a href="https://raw.github.com/pypa/pip/master/contrib/get-pip.py">get-pip.py</a><br>

		run these file in your current directory or "c:\Python27\" :
		1. type 'python ez_setup.py' and hit ENTER
		2. type 'python get-pip.py' and hit ENTER

		once done, you may continue to the next step.
	i. Create virtual environment for python. here is how to do it:
		in command prompt, at python27 directory, type 'pip install virtualenv'.
	j. once virtual environment has been isntalled, enter the virtual env by 
		type 'cd c:\Python27\venv\scripts' and hit ENTER
		type 'activate' and hit ENTER
		if you see this output, you are in the right track:
		(venv) c:\Python27\venv\Scripts>

	k. install supporting tools to run pilpres2014 code. In '(venv) c:\Python27\venv\Scripts>' :
		type 'easy_install pycurl'
		type 'easy_install beautifulsoup4'
		if these file installed, then you are ready to go.

	l. download pilpres2014 file : <a href="https://github.com/tandhy/pilpres2014/blob/master/download-per-propinsi.py">download-per-propinsi.py </a>and <a href="https://github.com/tandhy/pilpres2014/blob/master/download-semua-c1.py">download-semua-c1.py</a> by Right click and choose 'Save Link as...'. Save them to 'c:\python27\venv'

	m. before start to download, please modify the save path inside each file. In the file, I save it to drive F: under pilpres2014 folder : f:/pilpres2014, therefore I need to create a new folder, I named it 'pilpres2014' in drive F:. You may change the drive letter and the folder name.
	So, open the file, either download-semua-c1.py or download-per-propinsi.py. Right click on the file, choose "open with...", select or find notepad. Once the file opened, find 'savePath', it sits after 'import xxx' line.
	eg. if you want to save it to z:\pemilu2014, create the folder and modify savePath to 'z:/pemilu2014'. So it will looks like this: savePath = "z:/pemilu2014"

	m. if you want to download all C1 file, in '(venv) c:\Python27\venv\Scripts>', type 'python download-per-propinsi.py' and hit ENTER.
	it will create propinsi folder, kabupaten folder, kecamatan folder and kelurahan folder under the savePath folder.
	the scanned c1 will be formatted into : tpsNo-tpsID-imageID.jpg.

	The same way works if you want to download by propinsi. But you need to modify another line. 



