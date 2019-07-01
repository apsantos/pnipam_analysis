#!/usr/bin/env python
"""Rg_histogram

 generate histogram of values of Rg or anything
 							                                    
 -Andrew P. Santos					                            
 
"""
import sys, argparse
import numpy as np

class Histogram(object):
    """Callable Strain Rate Second Invariant 

        Finds the arrest time
    """
    def __init__(self):
        self.arresttime = []

    def addParser(self, parser):
        """
        Get relevant values from an argparse parser
        """
        if (parser.parse_args().start_line != None):
            self.start_line = parser.parse_args().start_line
        else:
            print 'assuming startline is 1'
            self.start_line = 1

        if parser.parse_args().filename:
            self.ifilename = parser.parse_args().filename

        if parser.parse_args().outfilename:
            self.ofilename = parser.parse_args().outfilename

        self.v_conversion = parser.parse_args().v_conversion
        if parser.parse_args().v_collumn >= 0:
            self.ic_v = parser.parse_args().v_collumn
        else:
            print 'you cant have a negative collumn number silly'
            return -1
        
        self.v_name = parser.parse_args().v_name

        if parser.parse_args().v_min:
            self.v_min = parser.parse_args().v_min
            self.guess_vmin = False
        else:
            self.guess_vmin = True

        if parser.parse_args().v_max:
            self.v_max = parser.parse_args().v_max
            self.guess_vmax = False
        else:
            self.guess_vmax = True

        self.nbins = parser.parse_args().nbins

    def read(self, filelist=None):
        self.values = []
        self.readValueFile( self.ifilename )

    def readValueFile(self, filename=None):
        """
        Read the Rg or whatever
        """
        if filename == None:
            filename = self.filenames[0]

        try:
            ifile = open(filename, 'r')
        except IOError:
            raise IOError('cannot find: %s. Either put the file in the working directory or fix the input file.' % filename)

        i_line = 0
        for line in ifile:
            i_line += 1
            if (i_line < self.start_line):
                continue

            data = line.strip().split()

            self.values.append( float( data[self.ic_v] ) )

    def generate(self, value_list=None):
        if self.guess_vmin:
            self.v_min = min(self.values)
        if self.guess_vmax:
            self.v_max = max(self.values)

        vrange=[self.v_min, self.v_max]
        self.frequency = np.histogram(self.values, bins=self.nbins, range=vrange, density=True)

    def write(self, filename=None):
        """
        Write the histogram
        """
        if filename == None:
            filename = self.ofilename

        ofile = open(filename, 'w')

        ofile.write('# %s frequency\n' % self.v_name )
        for i in range(self.nbins):
            ofile.write("%10.8f %10.8f\n" % ( self.frequency[1][i], self.frequency[0][i] ) )

        ofile.close()

def main(argv=None):
    # Parse in command-line arguments, and create the user help instructions
    parser = argparse.ArgumentParser(description='Fit a density profile and extract valuble information')
    parser.add_argument('-f', "--filename", type=str, 
                   help='file with density data.')
    parser.add_argument("-o", "--outfilename", type=str, default='histogram.txt',
                   help='output file name, assumed to be histogram.txt')
    parser.add_argument('-l', "--start_line", type=int,
                   help='Set the starting line number.')
    parser.add_argument("--v_collumn", type=int, default=0,
                   help='Collumn with the value')
    parser.add_argument("--v_conversion", type=float, default=1.0,
                   help='convert the values by this conversion')
    parser.add_argument("--v_name", type=str, default='property',
                   help='value name')
    parser.add_argument("--v_min", type=float, 
                   help='minimum  value')
    parser.add_argument("--v_max", type=float, 
                   help='maximum  value')
    parser.add_argument("--nbins", type=int, default=10,
                   help='number of histogram bins')

    histo = Histogram()

    # Tell the class everything specified in files and command line
    err = histo.addParser(parser)

    if err != None:
        print 'error parsing info'
        return

    # read in data 
    histo.read()

    # generate histogram based on read values
    histo.generate()

    # write histog
    histo.write()

if __name__ == '__main__':
    sys.exit(main())

# "The greatest happiness is to know the source of unhappiness." -Fyodor Dostoevsky
