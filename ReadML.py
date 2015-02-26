#
#  Read ML file
#
import pymzml

def HighestPeaks(peaklist):
    max_item= (0,0)
    for eachitem in peaklist:
        if eachitem[1] > max_item[1]:
            max_item = eachitem
    return max_item

IGNORE_LIST = []
def GetPeakbyMZRange(filename, mzrange, rtrange):
    # input is mzrange (a tuple), the output is the retention time, intensity of the peak

    # for m mz values
    #max_int_dict = dict()
    #for eachmz in mzrange_list:
    #    max_int_dict[eachmz] = {"max_int": 0}
    run = pymzml.run.Reader(filename, noiseThreshold = 100)
    for spec in run:
        try:
            rt_time = spec["scan time"]
            if rt_time < rtrange[0]:
                continue
            elif rt_time > rtrange[1]:
                print rt_time, spec["id"]
                break
        except:
            continue
        try:
            mz, intensity = HighestPeaks(spec.reduce(mzRange = mzrange).peaks)
        except:
            continue
        if intensity > max_intensity:
            max_intensity = intensity
            max_mz = mz
            max_time = spec["scan time"]
            max_id   = spec["id"]
    print (max_intensity, max_mz, max_time, max_id)


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
        # here the program assume the retention time is a float number
        self._rt = float(rt)
        self._idx = index

    @property
    def rtime(self):
        return self._rt

    @property
    def index(self, index):
        self._idx = index

    def __str__(self):
        return "retention time: %s, index: %s" %(self._rt, self._idx)

class SpecDict(dict):
    def __init__(self):
        self._dict = dict()

    def __getitem__(self, time):
        if float(time).is_integer():
            return self._dict[int(time)]
        else:
            matchlist = []
            dec_len = len(str(time).split(".")[-1])
            for specbasic in self._dict[int(time)]:
                if (specbasic.rtime - time) * 10 ** dec_len // 1 == 0:
                    matchlist.append(specbasic)
            return matchlist


    def __setitem__(self, time, specbasic):
        if not isinstance(specbasic, SpecBasic):
            raise Exception("SpectDict only accept SpecBasic")
        try:
            self._dict[int(time)].append(specbasic)
        except:
            self._dict[int(time)] = [specbasic]

    def __str__(self):
        return "number of spec: %s" % (len(self._dict.keys()))

class ExtractSpec:
    def __init__(self, filename):
        self.run, self.specdict = self.setup(filename)
        print self.specdict

    def setup(self, filename):
        # set up basic data structure
        run = pymzml.run.Reader(filename)
        specdict = SpecDict()
        for spectrum in run:
            if spectrum['ms level'] == 1:
                #print max(spectrum.i), min(spectrum.i)
                specbasic = SpecBasic(spectrum['scan time'], spectrum['id'])
                specdict[spectrum['scan time']] = specbasic
        return run, specdict

    def extractWithTime(self, time):
        return self.specdict[time]



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

def Test():
    filename = "E165ug.mzML"
    run = pymzml.run.Reader(filename)
    print run[1701].extremeValues('i')
    print run[1700].extremeValues('i')
    print run[1702].extremeValues('i')
    print run[1702].peaks



def examples():
    # first example
    #run = pymzml.run.Reader("E165ug.mzML", noiseThreshold = 100, MSn_Precision = 250e-6)
    #GetPeakbyMZRange("E165ug.mzML", (818.2, 818.7), (19.82, 20.34))
    #GetPeakbyMZRange("E165ug.mzML", (819.2, 819.7), (19.82, 20.34))
    GetPeakbyMZRange("E165ug.mzML", (818.2, 818.7), (15, 41))
    GetPeakbyMZRange("E165ug.mzML", (819.2, 819.7), (15, 41))
    GetPeakbyMZRange("E165ug.mzML", (1255.4, 1255.9), (15, 41))
    GetPeakbyMZRange("E165ug.mzML", (1256.1, 1256.6), (15, 41))
    #print Test()
    #ExtractIonChrom(run)

def ExtractTest():
    exspec = ExtractSpec("./4tRNA1_102009.mzML")
    # extract spectrums for specific time
    specs  = exspec.extractWithTime(1)
    print "for time 1"
    for spec in specs:
        print spec
    specs  = exspec.extractWithTime(1.1)
    print "for time 1.1"
    for spec in specs:
        print spec

if __name__ == "__main__":
    examples()
