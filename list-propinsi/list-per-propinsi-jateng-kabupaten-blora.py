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

def formatKode(kode):
	different = 5 - len(kode)
	zero = ''
	for i in range(0, different,1):
		zero += '0'
	return zero + kode

def formatKodeTPS(kode):
	different = 3 - len(str(kode))
	zero = ''
	for i in range(0, different,1):
		zero += '0'
	return zero + str(kode)

# set save path. you may change to your own folder. windows version
savePath = "f:/workspace/pilpres2014"
# set save path. you may change to your own folder. mac version
#savePath = "\users\pilpres2014"
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
#propinsi = [{'kode': '1', 'nama': 'ACEH'}, {'kode': '6728', 'nama': 'SUMATERA UTARA'}, {'kode': '12920', 'nama': 'SUMATERA BARAT'},{'kode': '14086', 'nama': 'RIAU'},{'kode': '15885', 'nama': 'JAMBI'},{'kode': '17404', 'nama': 'SUMATERA SELATAN'},{'kode': '20802', 'nama': 'BENGKULU'},{'kode': '22328', 'nama': 'LAMPUNG'},{'kode': '24993', 'nama': 'KEPULAUAN BANGKA BELITUNG'},{'kode': '25405', 'nama': 'KEPULAUAN RIAU'},{'kode': '25823', 'nama': 'DKI JAKARTA'},{'kode': '26141', 'nama': 'JAWA BARAT'},{'kode': '32676', 'nama': 'JAWA TENGAH'},{'kode': '41863', 'nama': 'DAERAH ISTIMEWA YOGYAKARTA'},{'kode': '42385', 'nama': 'JAWA TIMUR'},{'kode': '51578', 'nama': 'BANTEN'},{'kode': '53241', 'nama': 'BALI'},{'kode': '54020', 'nama': 'NUSA TENGGARA BARAT'},{'kode': '55065', 'nama': 'NUSA TENGGARA TIMUR'},{'kode': '58285', 'nama': 'KALIMANTAN BARAT'},{'kode': '60371', 'nama': 'KALIMANTAN TENGAH'},{'kode': '61965', 'nama': 'KALIMANTAN SELATAN'},{'kode': '64111', 'nama': 'KALIMANTAN TIMUR'},{'kode': '65702', 'nama': 'SULAWESI UTARA'},{'kode': '67393', 'nama': 'SULAWESI TENGAH'},{'kode': '69268', 'nama': 'SULAWESI SELATAN'},{'kode': '72551', 'nama': 'SULAWESI TENGGARA'},{'kode': '74716', 'nama': 'GORONTALO'},{'kode': '75425', 'nama': 'SULAWESI BARAT'},{'kode': '76096', 'nama': 'MALUKU'},{'kode': '77085', 'nama': 'MALUKU UTARA'},{'kode': '78203', 'nama': 'PAPUA'},{'kode': '81877', 'nama': 'PAPUA BARAT'}]
propinsi = [{'kode': '32676', 'nama': 'JAWA TENGAH'}]
kabupaten = [{'kode': '37514', 'nama': 'BLORA'}]

# open a log file
# set path for log
logPath = savePath + "/listpropinsi"


# iterate each propinsi
for prop in propinsi:
	logFilename = logPath + "/handy-" + prop['nama'] + "-" + prop['kode'] + "-" + list(kabupaten)[0]['nama'] + ".txt"
	# check for log file
	if not os.path.exists(logPath):
	    os.makedirs(logPath)

	#print "Propinsi : %s" %(prop['nama'])

	# check if file exists
	if not (os.path.exists(logFilename)):
		openLogFile = open(logFilename, 'w')
		openLogFile.write("Generated : "  + time.strftime("%m.%d.%Y %H:%M:%S") + "\n" )
		openLogFile.write("========================================\n")

		openLogFile.write( "Propinsi : %s (%s)\n" %(prop['nama'] , prop['kode']) )
		openLogFile.write( "Format data : Provinsi\tKabupaten/Kota\tKecamatan\tKelurahan\tNomor TPS\tID TPS\tPS-Hatta\tJW-JK\tTidak Sah\tLink4\tLink3\tLink2\tLink1\n\n" )
		listReadLogFile = ''
	else:
		openLogFile = open(logFilename, 'a')
		readLogFile = open(logFilename, 'r')
		listReadLogFile = readLogFile.read()


	# set folder path
	propinsiFolder = savePath + "/" + prop['nama']
	# create a folder if it does not exists
	if not (os.path.exists(propinsiFolder)):
		os.makedirs(propinsiFolder)

	# store ID 
	IDFilename = logPath + "/id-%s.txt" % (prop['kode'])

	# check if file exists
	if not (os.path.exists(IDFilename)):
		openIDFile = open( IDFilename, 'w') # rewrite existing file
		openIDFile.write("%s\n" % (prop['kode']) )
		listReadIDFile = ''
	else:
		openIDFile = open (IDFilename, 'a')
		readIDFile = open (IDFilename,'r')
		listReadIDFile = readIDFile.read()


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

	'''for option in optionTag:
		if(option.string != 'pilih'):
			# store <option> value into dict
			info = {'kode': option.get('value'), 'nama' : option.string }
			#  add dict into list
			kabupaten.append(info)'''

	# add time interval
	time.sleep(random.randint(3,5)) # random sleep time between 8 - 15 second
	# iterate each kabupaten
	for kab in kabupaten:
		#print "%s; %s" %(prop['nama'], kab['nama'])
		if kab['kode'] not in listReadIDFile:
			openIDFile.write("%s\n" % (kab['kode']) )
		
		#openLogFile.write( "%s; %s\n" %(prop['nama'], kab['nama']) )

		# set folder path
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
			#print "%s; %s; %s" %( prop['nama'], kab['nama'], kec['nama'] )
			if kec['kode'] not in listReadIDFile:
				openIDFile.write("%s\n" % (kec['kode']) )

			#openLogFile.write( "%s; %s; %s\n" %( prop['nama'], kab['nama'], kec['nama'] ) )

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

			# iterate each kelurahan
			for kel in kelurahan:
				# check if kelurahan has been downloaded or not in the IDFilename
				#print "%s; %s; %s; %s" %( prop['nama'], kab['nama'], kec['nama'], kel['nama'] )
				#openLogFile.write( "%s; %s; %s; %s" % ( prop['nama'], kab['nama'], kec['nama'], kel['nama'] ) )

				if kel['kode'] not in listReadIDFile:
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
					'''aTag =''
					aTag = htmlFile.find_all('a')
					aList = []
					for a in aTag:
						if(a.get('href').find("javascript:read_jpg") != -1):
							aList.append(a.get('href').strip("javascript:read_jpg('").strip("')"))'''


					noTps = 0
					link1 = ''
					link2 = ''
					link3 = ''
					link4 = ''
					#				12 34567 890 12
					# format scan : 00 32832 006 01.jpg
					for i in range(0,len(tpsKode), 1):
						link1 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=00%s%s01.jpg", "hal.1")' % (formatKode(kel['kode']), formatKodeTPS(i+1))
						link2 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=00%s%s02.jpg", "hal.2")' % (formatKode(kel['kode']), formatKodeTPS(i+1))
						link3 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=00%s%s03.jpg", "hal.3")' % (formatKode(kel['kode']), formatKodeTPS(i+1))
						link4 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=00%s%s04.jpg", "hal.4")' % (formatKode(kel['kode']), formatKodeTPS(i+1))
						#link1 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=%s.jpg", "hal.1")' % (aList[(i * 4) + 0])
						#link2 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=%s.jpg", "hal.2")' % (aList[(i * 4) + 1])
						#link3 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=%s.jpg", "hal.3")' % (aList[(i * 4) + 2])
						#link4 = '=hyperlink("http://scanc1.kpu.go.id/viewp.php?f=%s.jpg", "hal.4")' % (aList[(i * 4) + 3])
						#print "%s\t%s\t%s\t%s\t%d\t%s" %( prop['nama'], kab['nama'], kec['nama'], kel['nama'], i + 1, tpsKode[i] )
						print "%s\t%s\t%s\t%s\t%d\t%s\t0\t0\t0\t%s\t%s\t%s\t%s" %( prop['nama'], kab['nama'], kec['nama'], kel['nama'], i + 1, tpsKode[i], link4, link3, link2, link1 )
						# check whether already written or not
						text = "%s\t%s\t%s\t%s\t%d\t%s\t0\t0\t0\t%s\t%s\t%s\t%s\n" %( prop['nama'], kab['nama'], kec['nama'], kel['nama'], i + 1, tpsKode[i], link4, link3, link2, link1 )
						if text not in listReadLogFile:
							openLogFile.write(text)

					print "----------------------------------------------------------------"
					openIDFile.write("%s\n" % (kel['kode']) )
					time.sleep(random.randint(1,3)) # random sleep time between 1 - 3 second

				else:
					print "%s\t%s\t%s\t%s\t--> DONE" %( prop['nama'], kab['nama'], kec['nama'], kel['nama'])


			# separator between kecamatan
			print "----------------------------------------------------------------"

	# close c instance
	c.close()
	# close openLogFile instance
	openLogFile.close()
