'''
	Author : Tandhy Simanjuntak / July 15th, 2014
	Purpose : To download all c1 form from pilpres2014.kpu.go.id
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

# set save path. 
savePath = "f:/workspace/pilpres2014"
# set this variable to show each form c1 filename after saved into computer
showSavedFilename = True

# variable
propinsi = []
kabupaten = []
kecamatan = []
kelurahan = []

# format file c1: tpsx-tpsKode-[12digit].jpg
# saved under these folder : Propinsi - Kabupaten - Kecamatan - Kelurahan

#
c = pycurl.Curl()
buffer = StringIO()

url = 'http://pilpres2014.kpu.go.id/c1.php'
c.setopt(c.URL,url)
c.setopt(c.WRITEDATA, buffer)
c.perform()

# fetch <option>
htmlFile = BeautifulSoup(buffer.getvalue())
optionTag = htmlFile.find_all('option')
for option in optionTag:
	if(option.string != 'pilih'):
		# store <option> value into dict
		info = {'kode': option.get('value'), 'nama' : option.string }
		#  add dict into list
		propinsi.append(info)

# iterate each propinsi
for prop in propinsi:
	print "Propinsi : %s" %(prop['nama'])
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
	c.setopt(c.WRITEDATA, buffer)
	c.perform()

	# fetch <option>
	htmlFile = BeautifulSoup(buffer.getvalue())
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
		c.setopt(c.WRITEDATA, buffer)
		c.perform()

		# fetch <option>
		htmlFile = BeautifulSoup(buffer.getvalue())
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
			c.setopt(c.WRITEDATA, buffer)
			c.perform()
			
			# fetch <option>
			htmlFile = BeautifulSoup(buffer.getvalue())
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
				print "\t\t\tKelurahan : %s" %(kel['nama'])
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
				c.setopt(c.POSTFIELDS, postfields)
				c.setopt(c.WRITEDATA, buffer)
				c.perform()

				# fetch <td> to get tps code
				htmlFile = BeautifulSoup(buffer.getvalue())
				tdTag = htmlFile.find_all('td')
				tpsKode = []
				for td in tdTag:
					if(td.string != None) and (td.string != 'unduh'):
						if(len(td.string) > 2 ):
							tpsKode.append(td.string)

				# fetch <a> to get link to the image
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
						saveFile = open(filename,'wb')
						# save received data into filename
						c.setopt(c.WRITEDATA, saveFile)
						c.perform()

						if (showSavedFilename):
							print "\t\t\t\t%s -> %s" % (url, filename)
						
						saveFile.close()
						time.sleep(random.randint(3,5)) # random sleep time between 3 - 5 second

				print "\t\t\t\tTotal TPS = %d ; total form C1 = %d\n" % ( len(tpsKode), len(aList))

			# separator between kecamatan
			print "----------------------------------------------------------------"

c.close()
