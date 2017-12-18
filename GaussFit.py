from math import ceil, sqrt, log, floor, fabs
from numpy import histogram, linspace, arange
from scipy.stats import norm, chisquare, skew
import matplotlib.text as text
from matplotlib.pyplot import hist, plot, legend, suptitle, show, close, figure, savefig, xticks
from matplotlib.mlab import normpdf
from sys import stdout
from os import system
from traceback import print_exc

def gauss_fit(data, **kwargs):
	'''
	Makes a Gauss fit for the input data parameter and a histogram based on the number of bins that are 
	located in 'kwargs'. It saves 2 graphs that both include a normal distribution curve, histogram 
	and data. One of them contains the p-value of the Chi squares test, the other contains: 
	number of bins, size of bins, mean and standard deviation for the gauss distribution and 
	Chi squares test results, including: Chi square, p-value and degrees of freedom.
	'''
	# For every bin size located in kwargs:
	for title, bins in kwargs.items():
		n = len(data)

		# Calculates the edges of the bins, centers of the bins and their sizes:
		unused_hist, bin_edges = histogram(data, bins=bins, normed=True)
		bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
		bin_size = bin_edges[1]-bin_edges[0]

		# Fits the data into normal distribution and makes a plot:
		mean, stdev = norm.fit(data)
		x = linspace(min(data), max(data), n/2)
		gauss = normpdf(x, mean, stdev)
		
		# Calculates the Chi square test results:
		hist_chi = histogram(data, bins=bins)
		x_chi = bin_centres
		gauss_chi = normpdf(x_chi, mean, stdev)
		chi_square = chisquare(hist_chi[0], gauss_chi * n) #chisquare(expected_result, result_from_gauss)

		print "Processing %s" %(title)

		# Plots and saves the first figure that includes the p-value:
		figure_pvalue = figure(1)
		xticks(range(int(floor(min(data))), int(ceil(max(data))), 1))
		plot(x, gauss, 'r')
		suptitle(str(title))
		hist(data, bins=bins, normed=True, color='y', alpha=0.75)
		pvalue_text = "p-value= " + str(chi_square[1])
		figure_pvalue.text(0.15, 0.86, pvalue_text, ha='left', va='top', size='smaller')
		savefig("graph_pvalue_%s%s" %(str(title),".png"))

		# Plots and saves the second figure that includes rest of the data:
		figure_output = figure(2)
		xticks(range(int(floor(min(data))), int(ceil(max(data))), 1))
		plot(x, gauss, 'r')
		suptitle(str(title))
		hist(data, bins=bins, normed=True, color='y', alpha=0.75)
		output_text = "Bins (number, size): "+str(bins)+", "+str(bin_size)+"\nMean: "+str(mean)+ \
			"\nStandard deviation: "+str(stdev)+"\nChi square test (Chi square, p-value, DOF): \n" \
			+str(chi_square[0])+", "+str(chi_square[1])+", "+str(len(data)-1)
		figure_output.text(0.15, 0.86, output_text, ha='left', va='top', size=8, linespacing=1.5)
		savefig("graph_output_%s%s" %(str(title),".png"))
		
		close('all')
		#return bin_size, mean, stdev, chi_square

def import_data():
	'''
	Imports data from the file 'data.txt' and returns that data as a list of numbers.
	NOTE: data in 'data.txt' must be separated by blank spaces or located on new lines. 
	'''
	try:
		dataset = open("data.txt","r")
		rawdata = dataset.read().strip().split()
		dataset.close()
	except: 
		print "ERROR: Opening 'data.txt' failed! Check if the file exists or if it's named properly.\n"
		print_exc(file=stdout)

	data=[]
	try:
		for e in rawdata:
			data.append(float(e))
		return data
	except:
		print "ERROR: Value %d in 'data.txt' is not a valid number!\n" %(rawdata.index(e)+1)
		print_exc(file=stdout)


data = import_data()
n = len(data)

# A dictionary that includes calculations for the various suggested number of bins
bin_dict = {
	"bin_sqrt" : int(ceil(sqrt(n))),    # Square-root choice
	"bin_sturges" : int(ceil(log(n,2)+1)),    # Sturges' formula
	"bin_rice_rule" : int(ceil(2*n**(1.0/3))),    # Rice Rule
	"bin_doane" : int(1 + log(n,2) + log(1+((fabs(skew(data)))/sqrt((6*(n-2))/((n+1.)*(n+3)))),2))
	# Doane's formula
}

try:
	print "Starting Gauss fit . . ."
	gauss_fit(data, **bin_dict)
	print "Finished!"
	#print "Bins (number, size): ", bins,",",bin_size, "\nMean: ", mean, "\nStandard deviation: ", stdev,\
	#"\nChi square test (Chi square, p-value, DOF): \n\t", chi_square[0],",",chi_square[1],",",len(data)-1

except: 
	print "ERROR: There was an error preforming the Gauss distribution!\n"
	print_exc(file=stdout)
	
system('pause')