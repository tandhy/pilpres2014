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

# set Prov code and name to download specific C1 form.
Prov = {'kode':'26141', 'nama':'Jawa Barat'} # Propinsi Jawa Barat
Kab = {'kode':'28573', 'nama':'Ciamis'} # Kabupaten Ciamis

# variable
kecamatan = []
kelurahan = []

# format file c1: tpsKode-[12digit].jpg
# tapi simpan di folder dan sub folder : Propinsi - Kabupaten - Kecamatan - Kelurahan

c = pycurl.Curl()
buffer = StringIO()

print "Propinsi : %s" % (Prov['nama'])
# create folder for propinsi
PropinsiFolder = savePath + "/" + Prov['nama']
if not (os.path.exists(PropinsiFolder)):
	os.makedirs(PropinsiFolder)

print "\tKabupaten : %s" % (Kab['nama'])
# create folder for kabupaten
kabupatenFolder = PropinsiFolder + "/" + Kab['nama']
if not (os.path.exists(kabupatenFolder)):
	os.makedirs(kabupatenFolder)

# url path for downloading all province
#url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=0&parent=26141'
# get kecamatan kode
url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % ( Prov['kode'], Kab['kode'] )
post_data = {'wilayah_id': Kab['kode']}
postfields = urlencode(post_data)
c.setopt(c.URL,url)
c.setopt(c.POSTFIELDS, postfields)
c.setopt(c.WRITEDATA, buffer)
c.perform()

# buat tree, dan ambil nilai <option>
htmlFile = BeautifulSoup(buffer.getvalue())
optionTag = htmlFile.find_all('option')
for option in optionTag:
	if(option.string != 'pilih'):
		#print "kode : %s = %s" %(option.get('value') , option.string )
		info = {'kode': option.get('value'), 'nama' : option.string }
		kecamatan.append(info)


# add time interval
time.sleep(random.randint(8,15)) # random sleep time between 8 - 15 second

# get kelurahan/desa kode per kecamatan
for kec in kecamatan:
	print "\t\tKecamatan : %s" %(kec['nama'])

	c = pycurl.Curl()
	buffer = StringIO()
	#url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=28573&parent=28574'
	url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % (Kab['kode'], kec['kode'])
	post_data = {'wilayah_id': kec['kode']}
	postfields = urlencode(post_data)
	c.setopt(c.URL,url)
	c.setopt(c.POSTFIELDS, postfields)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	# buat tree, dan ambil nilai <option>
	htmlFile = BeautifulSoup(buffer.getvalue())
	optionTag = htmlFile.find_all('option')
	for option in optionTag:
		if(option.string != 'pilih'):
			info = {'kode': option.get('value'), 'nama' : option.string }
			kelurahan.append(info)

	time.sleep(random.randint(8,15)) # random sleep time between 8 - 15 second

	# get tps from each kelurahan
	for kel in kelurahan:
		print "\t\t\tKelurahan : %s" %(kel['nama'])
		# create folder for kecamatan
		kecamatanFolder = kabupatenFolder + "/" + kec['nama']
		if not (os.path.exists(kecamatanFolder)):
			os.makedirs(kecamatanFolder)

		
		c = pycurl.Curl()
		buffer = StringIO()
		url = 'http://pilpres2014.kpu.go.id/c1.php?cmd=select&grandparent=%s&parent=%s' % (kec['kode'], kel['kode'])
		post_data = {'wilayah_id': kel['kode']}
		postfields = urlencode(post_data)
		c.setopt(c.URL,url)
		c.setopt(c.POSTFIELDS, postfields)
		c.setopt(c.WRITEDATA, buffer)
		c.perform()

		# buat tree, dan ambil nilai <td> untuk tps
		htmlFile = BeautifulSoup(buffer.getvalue())
		tdTag = htmlFile.find_all('td')
		tpsKode = []
		for td in tdTag:
			if(td.string != None) and (td.string != 'unduh'):
				if(len(td.string) > 2 ):
					tpsKode.append(td.string)

		aTag = htmlFile.find_all('a')
		aList = []
		for a in aTag:
			if(a.get('href').find("javascript:read_jpg") != -1):
				aList.append(a.get('href').strip("javascript:read_jpg('").strip("')"))


		noTps = 0
		for i in range(0,len(aList), 1):
			# download image menggunakan curl dan save dengan format tpsKode-[12digit].jpg
			# buat folder dan sub folder apabila diperlukan

			# create folder for kelurahan
			kelurahanFolder = kecamatanFolder + "/" + kel['nama']
			if not (os.path.exists(kelurahanFolder)):
				os.makedirs(kelurahanFolder)

			filename = kelurahanFolder + "/" + 'tps%s-%s-%s.jpg' % (int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i])
			# do not download existing filename
			if not (os.path.exists(filename)):
				c = pycurl.Curl()
				buffer = StringIO()
				url = 'http://scanc1.kpu.go.id/viewp.php?f=%s.jpg' % (aList[i])
				c.setopt(c.URL, url)
				saveFile = open(filename,'wb')
				c.setopt(c.WRITEDATA, saveFile)
				c.perform()

				print "\t\t\t\t%s -> tps%s-%s-%s.jpg" % (url, int( aList[i][8:10] ) , tpsKode[ int( aList[i][8:10] ) - 1 ], aList[i])
				saveFile.close()
				time.sleep(random.randint(3,10)) # random sleep time between 8 - 15 second

		print "\t\t\t\tTotal TPS = %d ; total form C1 = %d\n" % ( len(tpsKode), len(aList))

	print "------------------------------------------------------------------------------"

c.close()
