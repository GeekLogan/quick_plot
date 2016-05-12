import os, fcntl, termios, struct, sys

dim = 2

def formString( input ):
	out = ''
	for i in input: out += i
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
	if not cr: cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
	return int(cr[1]), int(cr[0]) - 1

def readin():
	out = []
	for line in sys.stdin:
			split = line.split("\t")
			if len( split ) is not dim: continue
			out.append( ( float(split[0]), float(split[1]) ) )
	return out
	
def getextrema( data ):
	out = []
	for i in range( dim ):
		tmp = dict()
		tmp['min'] = data[0][i]
		tmp['max'] = data[0][i]
		out.append( tmp )
	return out

def addaxis( termstate, extrema, termsize ):
	xscale = abs( (extrema[0]['max'] - extrema[0]['min']) / float( termsize[0] ) )
	yscale = abs( (extrema[1]['max'] - extrema[1]['min']) / float( termsize[1] ) )

	if extrema[0]['min'] <= 0 and xmax >= 0:
		xzero = int( round( abs( extrema[0]['min'] / xscale ) ) ) 
		if xzero < 0: xzero = 0
		elif xzero > len( termstate[0] ) - 1: xzero = len( termstate[0] ) - 1
		for line in termstate: line[xzero] = '|'

	if extrema[1]['min'] <= 0 and extrema[1]['max'] >= 0:
		yzero = termsize[1] -  int( round( abs( extrema[1]['min'] / yscale ) ) ) 
		if yzero < 0: yzero = 0
		elif yzero > len(termstate) - 1: yzero = len(termstate) - 1
		termstate[yzero] = [ '-' ] * termsize[0]

	if extrema[0]['min'] <= 0 and extrema[0]['max'] >= 0:
		if extrema[1]['min'] <= 0 and extrema[1]['max'] >= 0:
			xzero = int( round( abs( extrema[0]['min'] / xscale ) ) ) 
			yzero = termsize[1] - int( round( abs( extrema[1]['min'] / yscale ) ) ) 
			termstate[yzero][xzero] = '+'

def plotdata( termstate, data, extrema, termsize ):
	xscale = abs( (extrema[0]['max'] - extrema[0]['min']) / float( termsize[0] ) )
	yscale = abs( (extrema[1]['max'] - extrema[1]['min']) / float( termsize[1] ) )

	for pt in data:
		xcord = int( round( (pt[0] - extrema[0]['min']) / xscale) )
		if xcord < 0: xcord = 0
		elif xcord > len( termstate[0] ) - 1: xcord = len( termstate[0] ) - 1

		ycord = termsize[1] - int( round( (pt[1] - extrema[1]['min']) / yscale) )
		if ycord < 0: ycord = 0
		elif ycord > len( termstate ) - 1: ycord = len( termstate ) - 1

		termstate[ycord][xcord] = 'O'
		
def framebuffer( termsize ):
	out = []
	for y in range( termsize[1] ): out.append( [' '] * termsize[0] )
	return out

def draw( termstate ):
	for line in termstate:
		print formString( line )

def main():
	extrema = []
	
	data = readin()
	if not data: exit()
	
	extrema	= getextrema( data )

	for pt in data:
			for i in range( dim ):
				if pt[i] < extrema[i]['min']: extrema[i]['min'] = pt[i]
				if pt[i] > extrema[i]['max']: extrema[i]['max'] = pt[i]

	termsize = getTermSize()

	termstate = framebuffer( termsize )

	addaxis( termstate, extrema, termsize )
	plotdata( termstate, data, extrema, termsize ) 

	draw( termstate )

if __name__ == "__main__":
    main()
