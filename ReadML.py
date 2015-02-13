#
#  Read ML file
#
import pymzml

def GetNPeakbyMZRange(run, mzrange, n):
    # input is mzrange (a tuple), the output is the retention time, intensity of the peak
    max_intensity = 0
    n = 0
    for spec in run:
        n += 1
        try:
            mz, intensity = spec.reduce(mzRange = mzrange).highestPeaks(1)[0]
            print spec.reduce(mzRange = mzrange).highestPeaks(1)
            break
        except:
            continue
        if intensity > max_intensity:
            max_intensity = intensity
            max_mz = mz
            max_time = spec["scan time"]
    print n
    print (max_intensity, max_mz, max_time)


def PlotRange(run):
    p = pymzml.plot.Factory()
    n = 0
    for spec in run:
        n = n + 1
        print n
        p.newPlot()
        p.add(spec.peaks, color=(200,00,00), style='circles')
        p.add(spec.centroidedPeaks, color=(00,00,00), style='sticks')
        p.add(spec.reprofiledPeaks, color=(00,255,00), style='circles')
        p.save( filename="output/plotAspect.xhtml")
        break

class SpecBasic:
    def __init__(self, rt, index):
        self._rt = rt
        self._idx = index

    @property
    def rtime(self, rtime):
        self_rt = rtime

    @property
    def index(self, index):
        self._idx = index

    def __str__(self):
        return "retention time: %s, index: %s" %(self._rt, self._idx)

def SpecDict(dict):
    def __init__(self):
        pass
    def __getattr__(self, time):
        for self[int(time)]

    def __setattr__(self, time, specbasic):
        if not isinstance(specbasic, SpecBasic):
            raise Exception("SpectDict only accept SpecBasic")
        try:
            self[int(time)].append(specbasic)
        except:
            self[int(time)] = [specbasic]

def setup(filename):
    # set up basic data structure
    run = pymzml.run.Reader(filename)
    speclist = []
    for spectrum in run:
        if spectrum['ms level'] == 1:
            speclist.append(SpecBasic(spectrum['scan time'], spectrum['id']))
    return speclist

def ExtractIonChromWithTime(run, time):


def ExtractIonChrom(run):
    timeDependentIntensities = []
    #MASS_2_FOLLOW = 1402
    MASS_2_FOLLOW = 1403
    print "mass 2 follow:", MASS_2_FOLLOW
    for spectrum in run:
        print spectrum['id']
    #for spectrum in run:
    #    if spectrum['ms level'] == 1:
    #        matchList = spectrum.hasPeak(MASS_2_FOLLOW)
    #        if matchList != []:
    #            print "matched"
    #            for mz,I in matchList:
    #                if I > 100:
    #                    timeDependentIntensities.append( [ spectrum['scan time'], I , mz ])
    for rt, i, mz in timeDependentIntensities:
        print('{0:5.3f} {1:13.4f}       {2:10}'.format( rt, i, mz ))


def examples():
    pass
    # first example
    #run = pymzml.run.Reader("../E165ug.mzML", MSn_Precision = 250e-6)
    #GetPeakbyMZRange(run, (1293.0, 1293.5))
    # second example
    #run = pymzml.run.Reader("../4tRNA1_102009.mzML", MSn_Precision = 250e-6)
    #GetPeakbyMZRange(run, (1402.0, 1402.5))
    #run = pymzml.run.Reader("./4tRNA1_102009.mzML", MSn_Precision = 250e-6)
    #GetNPeakbyMZRange(run, (1403.0, 1403.3))
    #ExtractIonChrom(run)

if __name__ == "__main__":
    setup("./4tRNA1_102009.mzML")
