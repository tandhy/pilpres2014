'''
	Author : Tandhy Simanjuntak / July 15th, 2014
	Purpose : To download all c1 form per province from pilpres2014.kpu.go.id
'''
# cURL operation
import pycurl
# handle buffer
from StringIO import StringIO
# encode given variable
from urllib import urlencode
# prettify output
import pprint
# handle directory operation
import os


# use beautifulSoup to read html
from bs4 import BeautifulSoup
# generate time and date and sleep interval
import time
# add random function to generate sleep interbal
import random

# set save path. you may change to your own folder.
savePath = "f:/temp/pilpres2014"
# set this variable to show each form c1 filename after saved into computer
showSavedFilename = True



# variable
prop = []
kabupaten = []
kecamatan = []
kelurahan = []

# format file c1: tpsx-tpsKode-[12digit].jpg
# saved under these folder : Propinsi - Kabupaten - Kecamatan - Kelurahan


# remove hashtag to enable propinsi download.
# For example, if you want to download propinsi Bali, remove '#' from prop = {'kode': '53241', 'nama': 'BALI'}
#prop = {'kode': '1', 'nama': 'ACEH'}
#prop = {'kode': '6728', 'nama': 'SUMATERA UTARA'}
#prop = {'kode': '12920', 'nama': 'SUMATERA BARAT'}
#prop = {'kode': '14086', 'nama': 'RIAU'}
#prop = {'kode': '15885', 'nama': 'JAMBI'}
#prop = {'kode': '17404', 'nama': 'SUMATERA SELATAN'}
#prop = {'kode': '20802', 'nama': 'BENGKULU'}
#prop = {'kode': '22328', 'nama': 'LAMPUNG'}
#prop = {'kode': '24993', 'nama': 'KEPULAUAN BANGKA BELITUNG'}
#prop = {'kode': '25405', 'nama': 'KEPULAUAN RIAU'}
#prop = {'kode': '25823', 'nama': 'DKI JAKARTA'}
#prop = {'kode': '26141', 'nama': 'JAWA BARAT'}
#prop = {'kode': '32676', 'nama': 'JAWA TENGAH'}
#prop = {'kode': '41863', 'nama': 'DAERAH ISTIMEWA YOGYAKARTA'}
#prop = {'kode': '42385', 'nama': 'JAWA TIMUR'}
#prop = {'kode': '51578', 'nama': 'BANTEN'}
#prop = {'kode': '53241', 'nama': 'BALI'}
#prop = {'kode': '54020', 'nama': 'NUSA TENGGARA BARAT'}
#prop = {'kode': '55065', 'nama': 'NUSA TENGGARA TIMUR'}
#prop = {'kode': '58285', 'nama': 'KALIMANTAN BARAT'}
prop = {'kode': '60371', 'nama': 'KALIMANTAN TENGAH'}
#prop = {'kode': '61965', 'nama': 'KALIMANTAN SELATAN'}
#prop = {'kode': '64111', 'nama': 'KALIMANTAN TIMUR'}
#prop = {'kode': '65702', 'nama': 'SULAWESI UTARA'}
#prop = {'kode': '67393', 'nama': 'SULAWESI TENGAH'}
#prop = {'kode': '69268', 'nama': 'SULAWESI SELATAN'}
#prop = {'kode': '72551', 'nama': 'SULAWESI TENGGARA'}
#prop = {'kode': '74716', 'nama': 'GORONTALO'}
#prop = {'kode': '75425', 'nama': 'SULAWESI BARAT'}
#prop = {'kode': '76096', 'nama': 'MALUKU'}
#prop = {'kode': '77085', 'nama': 'MALUKU UTARA'}
#prop = {'kode': '78203', 'nama': 'PAPUA'}
#prop = {'kode': '81877', 'nama': 'PAPUA BARAT'}

# open a log file
# set path for log
logPath = savePath + "/log"
logFilename = logPath + "/" + prop['nama'] + "-" + prop['kode'] + "-" + time.strftime("%Y%m%d-%H%M%S") + ".txt"
# check for log file
if not os.path.exists(logPath):
    os.makedirs(logPath)

openLogFile = open(logFilename, 'w')
openLogFile.write("Generated : "  + time.strftime("%m.%d.%Y %H:%M:%S") + "\n" )
openLogFile.write("========================================\n")

# store ID 
IDFilename = savePath + "/id-%s.txt" % (prop['kode'])

# check if file exists
if not (os.path.exists(IDFilename)):
	openIDFile = open( IDFilename, 'w') # rewrite existing file
	openIDFile.write("%s\n" % (prop['kode']) )
	listReadIDFile = ''
else:
	openIDFile = open (IDFilename, 'a')
	readIDFile = open (IDFilename,'r')
	listReadIDFile = readIDFile.read()




# iterate each propinsi
if (len(prop) == 0):
	print "You have to choose which propinsi you want to download"
else:
	print "Propinsi : %s" %(prop['nama'])

	openLogFile.write( "Propinsi : %s (%s)\n" %(prop['nama'] , prop['kode']) )
	if prop['kode'] not in listReadIDFile:
		openIDFile.write("%s\n" % (prop['kode']) )

	# set folder path
	propinsiFolder = savePath + "/" + prop['nama']
	# create a folder if it does not exists
	if not (os.path.exists(propinsiFolder)):
		os.makedirs(propinsiFolder)


	c = pycurl.Curl()
	buffer = StringIO()
	url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=0&parent=%s' % ( prop['kode'] )
	post_data = {'wilayah_id': prop['kode']}
	postfields = urlencode(post_data)
	c.setopt(c.URL,url)
	c.setopt(c.POSTFIELDS, postfields)
	c.setopt(c.CONNECTTIMEOUT,999)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()

	# fetch <option>
	htmlFile = BeautifulSoup(buffer.getvalue())
	optionTag = ''
	optionTag = htmlFile.find_all('option')
	kabupaten = []
	for option in optionTag:
		if(option.string != 'pilih'):
			# store <option> value into dict
			info = {'kode': option.get('value'), 'nama' : option.string }
			#  add dict into list
			kabupaten.append(info)

	# add time interval
	time.sleep(random.randint(3,5)) # random sleep time between 8 - 15 second
	# iterate each kabupaten
	for kab in kabupaten:
		print "\tKabupaten : %s" %(kab['nama'])
		
		openLogFile.write( "\tKabupaten : %s (%s)\n" %(kab['nama'] , kab['kode']) )
		if kab['kode'] not in listReadIDFile:
			openIDFile.write("%s\n" % (kab['kode']) )

		# set folder path
		kabupatenFolder = propinsiFolder + "/" + kab['nama']
		# create a folder if it does not exists
		if not (os.path.exists(kabupatenFolder)):
			os.makedirs(kabupatenFolder)

		c = pycurl.Curl()
		buffer = StringIO()
		url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % ( prop['kode'] , kab['kode'])
		post_data = {'wilayah_id': kab['kode']}
		postfields = urlencode(post_data)
		c.setopt(c.URL,url)
		c.setopt(c.POSTFIELDS, postfields)
		c.setopt(c.CONNECTTIMEOUT,999)
		c.setopt(c.WRITEDATA, buffer)
		c.perform()

		# fetch <option>
		htmlFile = BeautifulSoup(buffer.getvalue())
		optionTag = ''
		optionTag = htmlFile.find_all('option')
		kecamatan = []
		for option in optionTag:
			if(option.string != 'pilih'):
				# store <option> value into dict
				info = {'kode': option.get('value'), 'nama' : option.string }
				#  add dict into list
				kecamatan.append(info)

		# iterate each kecamatan
		for kec in kecamatan:
			print "\t\tKecamatan : %s" %(kec['nama'])

			openLogFile.write( "\t\tKecamatan : %s (%s)\n" %(kec['nama'], kec['kode']) )
			if kec['kode'] not in listReadIDFile:
				openIDFile.write("%s\n" % (kec['kode']) )

			# set folder path
			kecamatanFolder = kabupatenFolder + "/" + kec['nama']
			# create a folder if it does not exists
			if not (os.path.exists(kecamatanFolder)):
				os.makedirs(kecamatanFolder)

			c = pycurl.Curl()
			buffer = StringIO()
			url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % (kab['kode'], kec['kode'])
			post_data = {'wilayah_id': kec['kode']}
			postfields = urlencode(post_data)
			c.setopt(c.URL,url)
			c.setopt(c.POSTFIELDS, postfields)
			c.setopt(c.CONNECTTIMEOUT,999)
			c.setopt(c.WRITEDATA, buffer)
			c.perform()
			
			# fetch <option>
			htmlFile = BeautifulSoup(buffer.getvalue())
			optionTag = ''
			optionTag = htmlFile.find_all('option')
			kelurahan = []
			for option in optionTag:
				if(option.string != 'pilih'):
					# store <option> value into dict
					info = {'kode': option.get('value'), 'nama' : option.string }
					#  add dict into list
					kelurahan.append(info)

			time.sleep(random.randint(3,5)) # random sleep time between 3 - 5 second

			# iterate each kelurahan
			for kel in kelurahan:
				# check if kelurahan has been downloaded or not in the IDFilename
				if kel['kode'] not in listReadIDFile:
					print "\t\t\tKelurahan : %s" %(kel['nama'])

					openLogFile.write( "\t\t\tKelurahan : %s (%s)\n" %(kel['nama'], kel['kode']) )

					# set folder path
					kelurahanFolder = kecamatanFolder + "/" + kel['nama']
					# create a folder if it does not exists
					if not (os.path.exists(kelurahanFolder)):
						os.makedirs(kelurahanFolder)

					
					c = pycurl.Curl()
					buffer = StringIO()
					url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % (kec['kode'], kel['kode'])
					post_data = {'wilayah_id': kel['kode']}
					postfields = urlencode(post_data)
					c.setopt(c.URL,url)
					c.setopt(c.CONNECTTIMEOUT,999)
					c.setopt(c.POSTFIELDS, postfields)
					c.setopt(c.WRITEDATA, buffer)
					c.perform()

					# fetch <td> to get tps code
					htmlFile = BeautifulSoup(buffer.getvalue())
					tdTag = ''
					tdTag = htmlFile.find_all('td')
					tpsKode = []
					for td in tdTag:
						if(td.string != None) and (td.string != 'unduh'):
							if(len(td.string) > 2 ):
								tpsKode.append(td.string)

					# fetch <a> to get link to the image
					aTag =''
					aTag = htmlFile.find_all('a')
					aList = []
					for a in aTag:
						if(a.get('href').find("javascript:read_jpg") != -1):
							aList.append(a.get('href').strip("javascript:read_jpg('").strip("')"))


					noTps = 0
					for i in range(0,len(aList), 1):
						# file format : tpsx-tpsKode-[12digit].jpg -> tps1-xxxxxx-xxxxxxxxxxxx.jpg

						filename = kelurahanFolder + "/" + 'tps%s-%s-%s.jpg' % (int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i])
						# do not download existing filename
						if not (os.path.exists(filename)):
							c = pycurl.Curl()
							buffer = StringIO()
							url = 'http://scanc1.kpu.go.id/viewp.php?f=%s.jpg' % (aList[i])
							c.setopt(c.URL, url)
							c.setopt(c.CONNECTTIMEOUT,999)
							saveFile = open(filename,'wb')
							# save received data into filename
							c.setopt(c.WRITEDATA, saveFile)
							c.perform()

							if (showSavedFilename):
								print "\t\t\t\t%s -> tps%s-%s-%s.jpg" % (url, int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i] )

							openLogFile.write( "\t\t\t\t%s -> tps%s-%s-%s.jpg\n" % (url, int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i]) )
							
							saveFile.close()
							time.sleep(random.randint(3,5)) # random sleep time between 3 - 5 second
						else:
							# file has been downloaded
							print "\t\t\t\tDone -> tps%s-%s-%s.jpg" % ( int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i] )
							openLogFile.write( "\t\t\t\tDone -> tps%s-%s-%s.jpg\n" % ( int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i] ) )

					print "\t\t\t\tTotal TPS = %d ; total form C1 = %d\n" % ( len(tpsKode), len(aList))
					openLogFile.write( "\t\t\t\tTotal TPS = %d ; total form C1 = %d\n" % ( len(tpsKode), len(aList)) )
					if(len(aList) != 0):
						openIDFile.write("%s\n" % (kel['kode']) )

				else:
					print "\t\t\tKelurahan : %s --> done" %(kel['nama'])
					openLogFile.write( "\t\t\tKelurahan : %s --> done\n" %(kel['nama']) )

			# separator between kecamatan
			print "----------------------------------------------------------------"
			openLogFile.write( "------------------------------------------------------------------------------\n" )

	# close c instance
	c.close()
	# close openLogFile instance
	openLogFile.close()
