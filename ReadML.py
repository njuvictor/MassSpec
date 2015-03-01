#
#  Read ML file
#
import pymzml
import Tkinter, tkFileDialog

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
    max_intensity = 0
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


def MassToCharge(mass):
    if mass>4000:
        mz16= (mass- 3*1.007)/3
        mz18 = ((mass+2)-3*1.007)/3
    elif mass>2000:
        mz16=(mass - 2*1.007)/2
        mz18 = ((mass+2)-2*1.007)/2
    else:
        mz16= mass -1.007
        mz18=  mass+2-*1.007
    return mz16, mz18

def GetRT(mass):
    rt = 0.0078 * mass + 9.3348
    rt1 = rt - 4
    rt2 = rt + 4
    return rt1, rt2

def main():
    inputmass = 43
    mz16, mz18 = MassToCharge(inputmass)
    r_time    = GetRT(inputmass)
    GetPeakbyMZRange(inputfile, (mz16 - 0.2, mz16 + 0.2), (r_time - 10, r_time + 10))

def Test():
    filename = "E165ug.mzML"
    run = pymzml.run.Reader(filename)
    print run[1701].extremeValues('i')
    print run[1700].extremeValues('i')
    print run[1702].extremeValues('i')
    print run[1702].peaks

def examples(inputfile):
    # first example
    #run = pymzml.run.Reader("E165ug.mzML", noiseThreshold = 100, MSn_Precision = 250e-6)
    #GetPeakbyMZRange("E165ug.mzML", (818.2, 818.7), (19.82, 20.34))
    #GetPeakbyMZRange("E165ug.mzML", (819.2, 819.7), (19.82, 20.34))
    GetPeakbyMZRange(inputfile, (818.2, 818.7), (15, 41))
    GetPeakbyMZRange(inputfile, (819.2, 819.7), (15, 41))
    GetPeakbyMZRange(inputfile, (1255.4, 1255.9), (15, 41))
    GetPeakbyMZRange(inputfile, (1256.1, 1256.6), (15, 41))
    GetPeakbyMZRange(inputfile, (1365, 1365.2), (15, 41))
    GetPeakbyMZRange(inputfile, (1365.6, 1365.8), (15, 41))
    #print Test()

if __name__ == "__main__":
    root = Tkinter.Tk()
    root.withdraw()
    inputfile = tkFileDialog.askopenfilename()
    examples(inputfile)
