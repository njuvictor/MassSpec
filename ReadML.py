#
#  Read ML file
#
import pymzml

def GetPeakbyMZRange(run, mzrange):
    # input is mzrange (a tuple), the output is the retention time, intensity of the peak
    max_intensity = 0
    for spec in run:
        try:
            mz, intensity = spec.reduce(mzRange = mzrange).highestPeaks(1)[0]
        except:
            continue
        if intensity > max_intensity:
            max_intensity = intensity
            max_mz = mz
            max_time = spec["scan time"]
    print (max_intensity, max_mz, max_time)


if __name__ == "__main__":
    run = pymzml.run.Reader("../E165ug.mzML", MSn_Precision = 250e-6)
#    p = pymzml.plot.Factory()
#    n = 0
#    for spec in run:
#        n = n + 1
#        print n
#        p.newPlot()
#        p.add(spec.peaks, color=(200,00,00), style='circles')
#        p.add(spec.centroidedPeaks, color=(00,00,00), style='sticks')
#        p.add(spec.reprofiledPeaks, color=(00,255,00), style='circles')
#        p.save( filename="output/plotAspect.xhtml")
#        break
    GetPeakbyMZRange(run, (1293.0, 1293.5))
