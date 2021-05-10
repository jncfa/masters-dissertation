
import csv, math
from matplotlib import pyplot

# replace name with file to plot

threadNumHeader = "Num Threads"
primeCountHeader = "Prime Count"
totalTimeHeader = "Total time"

dataByThreads_udoo = {}
with open('sysbench-cpu-udooboltv3.csv', newline='') as csvfile:
    csvReader = csv.DictReader(csvfile)
    for row in csvReader:
        threadCount = float(row[threadNumHeader])
        if dataByThreads_udoo.get(threadCount, None) is None:
            dataByThreads_udoo[threadCount] = ([], [])
        # assumes the data is ordered, otherwise we need to sort beforehand
        dataByThreads_udoo[threadCount][0].append(float(row[primeCountHeader]))
        dataByThreads_udoo[threadCount][1].append(float(row[totalTimeHeader]))

dataByThreads_raspi = {}
with open('sysbench-cpu-raspi4b.csv', newline='') as csvfile:
    csvReader = csv.DictReader(csvfile)
    for row in csvReader:
        threadCount = float(row[threadNumHeader])
        if dataByThreads_raspi.get(threadCount, None) is None:
            dataByThreads_raspi[threadCount] = ([], [])
        # assumes the data is ordered, otherwise we need to sort beforehand
        dataByThreads_raspi[threadCount][0].append(float(row[primeCountHeader]))
        dataByThreads_raspi[threadCount][1].append(float(row[totalTimeHeader]))
        
pyplot.figure()
plot_idx = 1
# prime count is the same for udoo and raspi
for threadCount in dataByThreads_udoo:
    pyplot.subplot(math.ceil(math.sqrt(len(dataByThreads_udoo.keys()))), math.floor(math.sqrt(len(dataByThreads_udoo.keys()))), plot_idx)
    plot_idx += 1
    pyplot.grid()
    pyplot.title("Using {:d} thread{}".format(int(threadCount), '' if threadCount == 1 else 's'))
    pyplot.plot(dataByThreads_raspi[threadCount][0], dataByThreads_raspi[threadCount][1], 'ro--', label='Raspberry Pi 4B')
    pyplot.plot(dataByThreads_udoo[threadCount][0], dataByThreads_udoo[threadCount][1],'go--', label='Udoo Bolt v3')
    pyplot.xlabel('Number of primes calculated')
    pyplot.ylabel('Run time ($s$)')
    pyplot.legend()

pyplot.show()

#plt.figure()
#plt.subplot(211)
#plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

#plt.subplot(212)
#plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
#plt.show()