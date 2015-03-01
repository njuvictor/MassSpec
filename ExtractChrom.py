

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
    ExtractTest()
