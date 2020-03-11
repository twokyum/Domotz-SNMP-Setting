#!/usr/bin/python
#
# RPICT ATTINY CONFIGURATION UTILITY
# VERSION 1.9.0
# 2017 FEB 27
# LECHACAL.COM

import ConfigParser, sys, struct, serial
import os.path
import optparse


if os.path.exists('/dev/ttyAMA0'):
	serial_port = '/dev/ttyAMA0'
elif os.path.exists('/dev/ttyS0'):
	serial_port = '/dev/ttyS0'
else:
	print 'Could not detect any supported serial port on device'
	sys.exit()


ser = serial.Serial(serial_port, 38400)
ser.flushInput()
ser.flushOutput()

key = 'C-|\x19'# arbitrary identification key / magic key
#key = '\x43\x2D\x7C\x19'
MAX_NODES = 0
MAX_CHANNELS = 0

def extr_float(lL, idx):
	out = ""
	for i in range(4):
		out += lL[idx+i]
	return out

def extr_byte(lL, idx):
	out = lL[idx]+'\x00'+ '\x00'+'\x00'
	return out

def extr_int(lL, idx):
	out = lL[idx]+ lL[idx+1]+ '\x00'+'\x00'
	return out

def wait_and_read(options):
# Function waiting to receive the id key
# Once id key detected the structure is read (stored in L[4])
# Then the length is known and full config is stored in L
# We then print the configuration in human readable format
	global MAX_NODES
	global MAX_CHANNELS
	fileoutname = "/tmp/rpict.conf"
	f = open(fileoutname,'w')
	f.write("[main]\n")
	
	L = ["","","",""]
	read_length = 5
	while len(L)<read_length:
		r = ser.read(1)
                #if options.debug: print "%d/%d" % (len(L),read_length)
		if "".join(L[:4])==key:
			L.append(r)
			if len(L)==5:
				if options.debug: print "\n# Received magic key ok."
				if L[4]=='\xa0':
					read_length = 21
				elif L[4]=='\xa1':
					read_length = 49
				elif L[4]=='\xa2':
					read_length = 52
                                elif L[4]=='\xb0':
					N_SENSORS = 8
					MAX_NODES = 25 # for 0xB0 only
					MAX_CHANNELS = 64 # for 0xB0 only
                                        read_length = 47+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xb1':
					N_MAX_BOARD = 5
					N_SENSORS = 8
					MAX_NODES = 25 # for 0xB1 only
					MAX_CHANNELS = 64 # for 0xB1 only
                                        read_length = 47+128+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xb2':
					N_MAX_BOARD = 5
					N_SENSORS = 8
					MAX_NODES = 28 # for 0xB2 only
					MAX_CHANNELS = 64 # for 0xB2 only
                                        read_length = 47+128+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xb3':
					N_MAX_BOARD = 5
					N_SENSORS = 8
					MAX_NODES = 28 # for 0xB2 only
					MAX_CHANNELS = 64 # for 0xB2 only
                                        read_length = 48+128+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xb4':
					N_MAX_BOARD = 5
					N_SENSORS = 8
					MAX_NODES = 28 # for 0xB2 only
					MAX_CHANNELS = 64 # for 0xB2 only
                                        read_length = 51+128+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xc0':
					N_MAX_BOARD = 2
					N_SENSORS = 8
					MAX_NODES = 16 # 
					MAX_CHANNELS = 64 # 
                                        read_length = 79+4*MAX_NODES+2*MAX_CHANNELS
                                elif L[4]=='\xc1':
					N_MAX_BOARD = 2
					N_SENSORS = 8
					MAX_NODES = 16 # 
					MAX_CHANNELS = 64 # 
                                        read_length = 80+4*MAX_NODES+2*MAX_CHANNELS
				else:
					print "Unknown structure 0x%02x" % ord(L[4])
					sys.exit()
		else:
			if options.debug: print ".",
			L.append(r)
			L.pop(0)
	print "# "	
	print "# Configuration in memory:"
	print "# "	
	print "# Structure: 0x%02x" % ord(L[4])
	idx = 5
	format_ = struct.unpack('I', extr_byte(L, idx))
	idx += 1
	print "# Format: %d" % format_
	f.write("format = %d\n" % format_)
	nodeid = struct.unpack('I', extr_byte(L, idx))
	idx += 1
	print "# NodeId: %d" % nodeid
	f.write("nodeid = %d\n" % nodeid)
	polling = struct.unpack('I', extr_int(L, idx))
	idx += 2
	print "# Polling: %d" % polling[0]
	f.write("polling = %d\n" % polling[0])

        if L[4]=='\xa0': # RPICT3T1 RPICT3V1 RPICT4T4
		ical = struct.unpack('f', extr_float(L, idx))
		idx += 4
		print "# ICAL: %f" % ical
		f.write("ical = %f\n" % ical)
                vcal = struct.unpack('f', extr_float(L, idx))
		idx += 4
		print "# VCAL: %f" % vcal
                f.write("vcal = %f\n" % vcal)
                vest = struct.unpack('f', extr_float(L, idx))
		idx += 4
                print "# VEST: %f" % vest
                f.write("vest = %f\n" % vest)
	elif L[4]=='\xa1':
                print "# KCAL: ",
                f.write("kcal =")
		nkcalread = 8
		for u in range(nkcalread):
                        sup = struct.unpack('f', extr_float(L, idx))[0],
                        f.write(" %s" % sup)
                        print " %s" % sup,
                        idx += 4
		f.write("\n")
		print
                phasecal = struct.unpack('f', extr_float(L, idx))
		idx += 4
		print "# PHASECAL: %f" % phasecal
                f.write("phasecal = %f\n" % phasecal)
                vest = struct.unpack('f', extr_float(L, idx))
		idx += 4
                print "# VEST: %f" % vest
                f.write("vest = %f\n" % vest)
	elif L[4]=='\xa2':
                print "# KCAL: ",
                f.write("kcal =")
		nkcalread = 8
		for u in range(nkcalread):
                        sup = struct.unpack('f', extr_float(L, idx))[0],
                        f.write(" %s" % sup)
                        print " %s" % sup,
                        idx += 4
		f.write("\n")
		print

		phasecal = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# PHASECAL: %d" % phasecal
                f.write("phasecal = %d\n" % phasecal)
                
                vest = struct.unpack('f', extr_float(L, idx))
		idx += 4
                print "# VEST: %f" % vest
                f.write("vest = %f\n" % vest)

		xpFREQ = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# xpFREQ: %d" % xpFREQ
                f.write("xpFREQ = %d\n" % xpFREQ)

		Ncycle = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Ncycle: %d" % Ncycle
                f.write("Ncycle = %d\n" % Ncycle)
		
                debug = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# debug: %d" % debug
                f.write("debug = %d\n" % debug)
        
        elif L[4] in ['\xb0','\xb1','\xb2','\xb3','\xc0','\xc1']: # RPICT7V1 & RPICT4V3 version 2 + RPICT8
                print "# KCAL: ",
                f.write("kcal =")
		if L[4]=='\xb0': nkcalread = N_SENSORS
		elif L[4] in ['\xb1','\xb2','\xb3','\xc0','\xc1']: nkcalread = N_SENSORS * N_MAX_BOARD 
		for u in range(nkcalread):
                	sup = struct.unpack('f', extr_float(L, idx))[0],
			f.write(" %s" % sup)
			print " %s" % sup,
			idx += 4
		f.write("\n")
		print

		if L[4] in ['\xb3','\xc1']:
			PHASECAL = struct.unpack('I', extr_byte(L, idx))
			idx += 1
			print "# PHASECAL: %d" % PHASECAL
                	f.write("phasecal = %d\n" % PHASECAL)

		vest = struct.unpack('f', extr_float(L,idx))
		idx += 4
		print "# VEST: %f" % vest
                f.write("vest = %f\n" % vest)

		Nnode = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Nnode: %d" % Nnode
                f.write("Nnode = %d\n" % Nnode)

		Nchan = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Nchan: %d" % Nchan
                f.write("Nchan = %d\n" % Nchan)

                f.write("HWSCT =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")

                f.write("HWMCPSCT =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			
			idx += 1
		f.write("\n")
                
		f.write("HWVOL =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("HWMCPVOL =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("CHTYPE =")
		for u in range(MAX_CHANNELS):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("CHID =")
		for u in range(MAX_CHANNELS):
                	sup =  struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		print "# Complete configuration in %s" % fileoutname
        elif L[4]=='\xb4': # RPICT7V1 & RPICT4V3 version 2 + RPICT8
                print "# KCAL: ",
                f.write("kcal =")
		nkcalread = N_SENSORS * N_MAX_BOARD 
		for u in range(nkcalread):
                	sup = struct.unpack('f', extr_float(L, idx))[0],
			f.write(" %s" % sup)
			print " %s" % sup,
			idx += 4
		f.write("\n")
		print

		PHASECAL = struct.unpack('b', L[idx])#extr_byte(L, idx))
		idx += 1
		print "# PHASECAL: %d" % PHASECAL
                f.write("phasecal = %d\n" % PHASECAL)

		vest = struct.unpack('f', extr_float(L,idx))
		idx += 4
		print "# VEST: %f" % vest
                f.write("vest = %f\n" % vest)

		xpFREQ = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# xpFREQ: %d" % xpFREQ
                f.write("xpFREQ = %d\n" % xpFREQ)
		
		Ncycle = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Ncycle: %d" % Ncycle
                f.write("Ncycle = %d\n" % Ncycle)
                
                Nnode = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Nnode: %d" % Nnode
                f.write("Nnode = %d\n" % Nnode)

		Nchan = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# Nchan: %d" % Nchan
                f.write("Nchan = %d\n" % Nchan)

                f.write("HWSCT =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")

                f.write("HWMCPSCT =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			
			idx += 1
		f.write("\n")
                
		f.write("HWVOL =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("HWMCPVOL =")
		for u in range(MAX_NODES):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("CHTYPE =")
		for u in range(MAX_CHANNELS):
                	sup = struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")
		
		f.write("CHID =")
		for u in range(MAX_CHANNELS):
                	sup =  struct.unpack('I', extr_byte(L, idx))[0]
			f.write(" %s" % sup)
			idx += 1
		f.write("\n")

                debug = struct.unpack('I', extr_byte(L, idx))
		idx += 1
		print "# debug: %d" % debug
                f.write("debug = %d\n" % debug)

		print "# Complete configuration in %s" % fileoutname
        print "# "

	f.close()

	return L

def config_serialise(config, structure):

	tts = key
	tts += structure
	tts += chr(int(config.get('main', 'format')))
	tts += struct.pack('B', int(config.get('main', 'nodeid')))#nodeid
	tts += struct.pack('H', int(config.get('main', 'polling')))#polling
	if structure=='\xa0':
		tts += struct.pack('f', float(config.get('main', 'ical')))#ical
		tts += struct.pack('f', float(config.get('main', 'vcal')))#vcal
		tts += struct.pack('f', float(config.get('main', 'vest')))#vest
	elif structure=='\xa1':
		kcal = config.get('main', 'kcal').split()
		for k in  kcal:
			tts += struct.pack('f', float(k))
		tts += struct.pack('f', float(config.get('main', 'phasecal')))#phasecal
		tts += struct.pack('f', float(config.get('main', 'vest')))#vest
	elif structure=='\xa2':
		kcal = config.get('main', 'kcal').split()
		for k in  kcal:
			tts += struct.pack('f', float(k))
		tts += struct.pack('B', int(config.get('main', 'phasecal')))#phasecal
		tts += struct.pack('f', float(config.get('main', 'vest')))#vest
		tts += struct.pack('B', int(config.get('main', 'xpFREQ')))# xpFREQ
		tts += struct.pack('B', int(config.get('main', 'Ncycle')))# Ncycle
		tts += struct.pack('B', int(config.get('main', 'debug')))# debug
	elif structure in ['\xb0','\xb1','\xb2','\xb3','\xc0','\xc1']:
		kcal = config.get('main', 'kcal').split()
		for k in  kcal:
			tts += struct.pack('f', float(k))
		if structure in ['\xb3','\xc1']: tts += struct.pack('c', chr(int(config.get('main', 'phasecal'))))#phasecal
		tts += struct.pack('f', float(config.get('main', 'vest')))#vest
		tts += struct.pack('c', chr(int(config.get('main', 'Nnode'))))#Nnode
		tts += struct.pack('c', chr(int(config.get('main', 'Nchan'))))#Nchan
		
		hwsct = config.get('main', 'HWSCT').split()
		if len(hwsct) != MAX_NODES: 
			print "config error HWSCT"
			print "Expected length %d got %d" % (MAX_NODES,len(hwsct))
			sys.exit()
		for k in  hwsct:
			tts += struct.pack('c', chr(int((k))))

		hwmcpsct = config.get('main', 'HWMCPSCT').split()
		if len(hwmcpsct) != MAX_NODES: 
			print "config error HWMCPSCT"
			print "Expected length %d got %d" % (MAX_NODES,len(hwmcpsct))
			sys.exit()
		for k in  hwmcpsct:
			tts += struct.pack('c', chr(int((k))))
		
		hwvol = config.get('main', 'HWVOL').split()
		if len(hwvol) != MAX_NODES: 
			print "config error HWVOL"
			print "Expected length %d got %d" % (MAX_NODES,len(hwvol))
			sys.exit()
		for k in  hwvol:
			tts += struct.pack('c', chr(int((k))))
		
		hwmcpvol = config.get('main', 'HWMCPVOL').split()
		if len(hwmcpvol) != MAX_NODES: 
			print "config error HWMCPVOL"
			print "Expected length %d got %d" % (MAX_NODES,len(hwmcpvol))
			sys.exit()
		for k in  hwmcpvol:
			tts += struct.pack('c', chr(int((k))))
		
		chtype = config.get('main', 'CHTYPE').split()
		if len(chtype) != MAX_CHANNELS: 
			print "config error CHTYPE"
			print "Expected length %d got %d" % (MAX_CHANNELS,len(chtype))
			sys.exit()
		for k in  chtype:
			tts += struct.pack('c', chr(int((k))))
		
		chid = config.get('main', 'CHID').split()
		if len(chid) != MAX_CHANNELS: 
			print "config error CHID" 
			print "Expected length %d got %d" % (MAX_CHANNELS,len(chid))
			sys.exit()
		for k in  chid:
			tts += struct.pack('c', chr(int((k))))
	elif structure == '\xb4':
		kcal = config.get('main', 'kcal').split()
		for k in  kcal:
			tts += struct.pack('f', float(k))
		tts += struct.pack('b', int(config.get('main', 'phasecal')))#phasecal
		tts += struct.pack('f', float(config.get('main', 'vest')))#vest
		tts += struct.pack('B', int(config.get('main', 'xpFREQ')))#phasecal
		tts += struct.pack('B', int(config.get('main', 'Ncycle')))#phasecal
		tts += struct.pack('B', int(config.get('main', 'Nnode')))#Nnode
		tts += struct.pack('B', int(config.get('main', 'Nchan')))#Nchan
		
		hwsct = config.get('main', 'HWSCT').split()
		if len(hwsct) != MAX_NODES: 
			print "config error HWSCT"
			print "Expected length %d got %d" % (MAX_NODES,len(hwsct))
			sys.exit()
		for k in  hwsct:
			tts += struct.pack('B', int((k)))

		hwmcpsct = config.get('main', 'HWMCPSCT').split()
		if len(hwmcpsct) != MAX_NODES: 
			print "config error HWMCPSCT"
			print "Expected length %d got %d" % (MAX_NODES,len(hwmcpsct))
			sys.exit()
		for k in  hwmcpsct:
			tts += struct.pack('B', int((k)))
		
		hwvol = config.get('main', 'HWVOL').split()
		if len(hwvol) != MAX_NODES: 
			print "config error HWVOL"
			print "Expected length %d got %d" % (MAX_NODES,len(hwvol))
			sys.exit()
		for k in  hwvol:
			tts += struct.pack('B', int((k)))
		
		hwmcpvol = config.get('main', 'HWMCPVOL').split()
		if len(hwmcpvol) != MAX_NODES: 
			print "config error HWMCPVOL"
			print "Expected length %d got %d" % (MAX_NODES,len(hwmcpvol))
			sys.exit()
		for k in  hwmcpvol:
			tts += struct.pack('B', int((k)))
		
		chtype = config.get('main', 'CHTYPE').split()
		if len(chtype) != MAX_CHANNELS: 
			print "config error CHTYPE"
			print "Expected length %d got %d" % (MAX_CHANNELS,len(chtype))
			sys.exit()
		for k in  chtype:
			tts += struct.pack('B', int((k)))
		
		chid = config.get('main', 'CHID').split()
		if len(chid) != MAX_CHANNELS: 
			print "config error CHID" 
			print "Expected length %d got %d" % (MAX_CHANNELS,len(chid))
			sys.exit()
		for k in  chid:
			tts += struct.pack('B', int((k)))
		tts += struct.pack('B', int(config.get('main', 'debug')))#booleans
	else:
		print "Unknown structure 0x%02x" % ord(L[4])
		sys.exit()
	return tts



if __name__ == "__main__":
# If just reading then the config is displayed
# If writing then the config file is sent over serial
	# Some option parsing first
	config = ConfigParser.ConfigParser()

	parser = optparse.OptionParser(usage="%prog [-w] filename [--version]", version="%prog 1.9.0")
	parser.add_option('-w', '--write',
				dest='filename',
				default="",
			)
        parser.add_option('-d', '--debug',
                                dest='debug',
                                default=False,
                                action='store_true',
                        )

	options, remainder = parser.parse_args()



	write_config = False
	if os.path.isfile(options.filename):
		config.read(options.filename)
		write_config = True
	else:
		if options.filename != "":
			print "Can not read file %s" % options.filename
			sys.exit()
		
	print "# RPICT Configuration Utility"
	if write_config:
		print "# Configuration will be overwritten (Ctrl C to cancel)"
	else:
		print "# Read only"
	print "# Now reset RPICT hardware"
	L = wait_and_read(options)


	if write_config:
		print "# Writing configuration with file %s" % options.filename
		tts = config_serialise(config, L[4])
		
		ser.write(tts)
	
		wait_and_read(options)

	if options.debug:
		while True:
			try:
				print ser.readline(),
				#tobe tested:
				#print ser.read(),
			except KeyboardInterrupt:
      				ser.close()
				break
