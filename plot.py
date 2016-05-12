import os, fcntl, termios, struct, sys

def formString( input ):
	out = ''
	for i in input:
		out += i
	return out

def getTermSize():
	env = os.environ
	def ioctl_GWINSZ(fd):
		try: cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
		except: return
		return cr
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except: pass
	if not cr:
		cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
	return int(cr[1]), int(cr[0])

data, extrema = [], []
dim = 2	
	
for line in sys.stdin:
        split = line.split("\t")
        if len( split ) < dim: continue
        data.append( ( float(split[0]), float(split[1]) ) )

if len(data) is 0: exit()

extrema	= [] 
for i in range( dim ):
	tmp = dict()
	tmp['min'] = data[0][i]
	tmp['max'] = data[0][i]
	extrema.append( tmp )

for pt in data:
        for i in range( dim ):
		if pt[i] < extrema[i]['min']:
			extrema[i]['min'] = pt[i]
		if pt[i] > extrema[i]['max']:
			extrema[i]['max'] = pt[i]

termsize = (getTermSize()[0], getTermSize()[1] - 1)

termstate = []
for y in range( termsize[1] ):
	termstate.append( [' '] * termsize[0] )

###BAD CODE AHEAD

xmin = extrema[0]['min']
xmax = extrema[0]['max']
xscale = abs( (xmax - xmin) / float( termsize[0] ) )

ymin = extrema[1]['min']
ymax = extrema[1]['max']
yscale = abs( (ymax - ymin) / float( termsize[1] ) )

if xmin <= 0 and xmax >= 0:
	xzero = int( round( abs( xmin / xscale ) ) ) 
	if xzero < 0: xzero = 0
	elif xzero > len( termstate[0] ) - 1: xzero = len( termstate[0] ) - 1

	for line in termstate: line[xzero] = '|'

if ymin <= 0 and ymax >= 0:
	yzero = termsize[1] -  int( round( abs( ymin / yscale ) ) ) 
	if yzero < 0: yzero = 0
	elif yzero > len(termstate) - 1: yzero = len(termstate) - 1
	
	termstate[yzero] = [ '-' ] * termsize[0]

if xmin <= 0 and xmax >= 0 and ymin <= 0 and ymax >= 0:
	xzero = int( round( abs( xmin / xscale ) ) ) 
	yzero = termsize[1] - int( round( abs( ymin / yscale ) ) ) 
	termstate[yzero][xzero] = '+'	

for pt in data:
	xcord = int( round( (pt[0] - xmin) / xscale) )
	if xcord < 0: xcord = 0
	elif xcord > len( termstate[0] ) - 1: xcord = len( termstate[0] ) - 1

	ycord = termsize[1] - int( round( (pt[1] - ymin) / yscale) )
	if ycord < 0: ycord = 0
	elif ycord > len( termstate ) - 1: ycord = len( termstate ) - 1

	termstate[ycord][xcord] = 'O'

for line in termstate:
	print formString( line )
