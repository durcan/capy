# The follwoing file will do in python something similar what is done in
# matllab + CAP. The basic idea is that you can load .root trees using
# the functionality provided by the very nice root_numpy package.
#
# Written by Peter Redl. For comments please Email me at: redl@stanford.edu
# Version 0.0     06/09/2013
#
# This is written with numpy version 1.7 in mind... if you have an oder
# numpy version I guarantee nothing, as a matter of fact I guarantee nothing
# regardless of your numpy version, use at your own risk :)! Have fun...


import numpy
from glob import *
#from scipy import *
from root_numpy import *
import numpy.lib.recfunctions as rfn
import sys


def LoadRRQ(detnum, min_date=0, max_date=numpy.inf, which_dataSet='ba',
            data_location='/galbadata/R133/dataReleases/Prodv5-3/merged/all',
            rrqs_to_load=[], eventRQ=False):

    if not ((which_dataSet is 'ba') or (which_dataSet is 'cf') or
            (which_dataSet is 'bg_permitted')):
        print 'You have selected a dataset to load that I do not recognize'
        print 'Please select eighter "ba", "cf" or "bg_permitted"... exiting now'
        sys.exit()

    if (detnum < 1100) or (detnum > 1115):
        print 'You have selected a detector number that is outside of the range'
        print 'Now exiting. Select a detector number that is between 1101-1115'
        # break
        sys.exit()

    if (min_date == 0) or (max_date == numpy.inf):
        print 'You have elected to load all of the ', which_dataSet, ' data'
    else:
        if (min_date > 10000) or (max_date > 10000):
            print 'you selected a data that is larger than the allowed date range'
            print 'please select a date in the format Year Month as a solid string'
            print 'so February 2013 would be 1302'
            sys.exit()
        print 'Minimum load day is: ', min_date, ' Maximum load day is: ', max_date
        min_date = numpy.int(min_date)
        max_date = numpy.int(max_date)

    detnum = numpy.int(detnum - 1100)
    print "Loading RRQ's: ", rrqs_to_load
    # Deciding what data To load....
    LoadingData = data_location + '/' + which_dataSet
    AllFiles = glob(LoadingData + '/*calib_Prodv5-3_01*.root')
    DataRelease = 53
    if len(AllFiles) == 0:
        AllFiles = glob(LoadingData + '/*calib_Prodv5-2_01*.root')
        DataRelease = 52
    AllFiles.sort()
    PassingFilesToLoad = []
    for line in AllFiles:
        #FileDate = numpy.int(line.split("_")[-2].split("a")[0])
        if DataRelease == 53:
            FileDate = numpy.int(line.split("_")[-2][0:-1])
        if DataRelease == 52:
            FileDate = numpy.int(line.split("_")[-2][0:-2])  # - 1000000
        print FileDate, line
        FileDate = FileDate - 10000
        if (FileDate >= min_date) and (FileDate <= max_date):
            PassingFilesToLoad = numpy.append(PassingFilesToLoad, line)
            # print FileDate, line
    # print 'These are the files we are loading for RRQs: \n',
    # PassingFilesToLoad

    # Done deciding what data to load...
    #PassingFilesToLoad = numpy.sort(PassingFilesToLoad)
    # now loading the data....
    #RRQ = root2array(PassingFilesToLoad, 'rrqDir/calibzip1', rrqs_to_load)
    # now loading the data....
    if eventRQ == False:
        if len(rrqs_to_load) > 0:
            RRQ = root2array(
                PassingFilesToLoad,
                'rrqDir/calibzip%0.1d' %
                detnum,
                rrqs_to_load)
        else:
            RRQ = root2array(
                PassingFilesToLoad,
                'rrqDir/calibzip%0.1d' %
                detnum)
        return RRQ
    if eventRQ:
        if len(rrqs_to_load) > 0:
            RRQ = root2array(
                PassingFilesToLoad,
                'rrqDir/calibevent',
                rrqs_to_load)
        else:
            RRQ = root2array(PassingFilesToLoad, 'rrqDir/calibevent')
        return RRQ


def LoadRQ(detnum, min_date=0, max_date=numpy.inf, which_dataSet='ba',
           data_location='/galbadata/R133/dataReleases/Prodv5-3/merged/all',
           rqs_to_load=[], eventRQ=False):

    if not ((which_dataSet is 'ba') or (which_dataSet is 'cf') or
            (which_dataSet is 'bg_permitted')):
        print 'You have selected a dataset to load that I do not recognize'
        print 'Please select eighter "ba", "cf" or "bg_permitted"... exiting now'
        sys.exit()

    if (detnum < 1100) or (detnum > 1115):
        print 'You have selected a detector number that is outside of the range'
        print 'Now exiting. Select a detector number that is between 1101-1115'
        # break
        sys.exit()

    if (min_date == 0) or (max_date == numpy.inf):
        print 'You have elected to load all of the ', which_dataSet, ' data'
    else:
        if (min_date > 10000) or (max_date > 10000):
            print 'you selected a data that is larger than the allowed date range'
            print 'please select a date in the format Year Month as a solid string'
            print 'so February 2013 would be 1302'
            sys.exit()
        print 'Minimum load day is: ', min_date, ' Maximum load day is: ', max_date
        min_date = numpy.int(min_date)
        max_date = numpy.int(max_date)

    detnum = numpy.int(detnum - 1100)
    print "Loading RQ's: ", rqs_to_load
    # Deciding what data To load....
    LoadingData = data_location + '/' + which_dataSet

    AllFiles = glob(LoadingData + '/*merge_Prodv5-3_01*.root')
    DataRelease = 53
    if len(AllFiles) == 0:
        AllFiles = glob(LoadingData + '/*merge_Prodv5-2_01*.root')
        DataRelease = 52

    PassingFilesToLoad = []
    AllFiles.sort()
    for line in AllFiles:
        #FileDate = numpy.int(line.split("_")[-2].split("a")[0])
        FileDate = numpy.int(line.split("_")[-2][0:-1])
        if DataRelease == 52:
            FileDate = numpy.int(line.split("_")[-2][0:-2])
        # print FileDate
        FileDate = FileDate - 10000
        if (FileDate >= min_date) and (FileDate <= max_date):
            PassingFilesToLoad = numpy.append(PassingFilesToLoad, line)

    # print 'These are the files we are loading for RQs: \n', PassingFilesToLoad
    # print rqs_to_load
    # Done deciding what data to load...

    # now loading the data....
    if eventRQ == False:
        if len(rqs_to_load) > 0:
            RQ = root2array(
                PassingFilesToLoad,
                'rqDir/zip%0.1d' %
                detnum,
                rqs_to_load)
        else:
            RQ = root2array(PassingFilesToLoad, 'rqDir/zip%0.1d' % detnum)
        return RQ
    if eventRQ:
        if len(rqs_to_load) > 0:
            RQ = root2array(PassingFilesToLoad, 'rqDir/eventTree', rqs_to_load)
        else:
            RQ = root2array(PassingFilesToLoad, 'rqDir/eventTree')
        return RQ


def LoadCut(detnum, min_date=0, max_date=numpy.inf, which_dataSet='ba',
            data_location='/galbadata/R133/dataReleases/Prodv5-3/merged/cuts/',
            cuts_to_load=[]):

    if not ((which_dataSet is 'ba') or (which_dataSet is 'cf') or
            (which_dataSet is 'bg_permitted')):
        print 'You have selected a dataset to load that I do not recognize'
        print 'Please select eighter "ba", "cf" or "bg_permitted"... exiting now'
        sys.exit()

    if (detnum < 1100) or (detnum > 1115):
        print 'You have selected a detector number that is outside of the range'
        print 'Now exiting. Select a detector number that is between 1101-1115'
        # break
        sys.exit()

    if (min_date == 0) or (max_date == numpy.inf):
        print 'You have elected to load all of the ', which_dataSet, ' data'
    else:
        if (min_date > 10000) or (max_date > 10000):
            print 'you selected a data that is larger than the allowed date range'
            print 'please select a date in the format Year Month as a solid string'
            print 'so February 2013 would be 1302'
            sys.exit()
        print 'Minimum load day is: ', min_date, ' Maximum load day is: ', max_date
        min_date = numpy.int(min_date)
        max_date = numpy.int(max_date)

    detnum = numpy.int(detnum - 1100)

    # Deciding what data To load....
    LoadingData = data_location + '/' + which_dataSet
    # print LoadingData
    # sys.exit()
    #cuts = numpy.zeros(len(cuts_to_load))
    print LoadingData
    # exit()
    cuts = []
    PassingFilesToLoad = []
    # print LoadingData
    for i in cuts_to_load:
        print "Loading Cut ", i
        AllFiles = []
        AllFiles = sorted(
            glob(LoadingData + '/' + i + '/*v53_01*.root'))
        # print LoadingData + '/current/' + i + '*.root'
        # print AllFiles
        # sys.exit()
        for line in AllFiles:
            FileDate = numpy.int(line.split("_")[-2][0:-1])
            # print FileDate
            FileDate = numpy.int(FileDate - 10000)
            # print FileDate

            if (FileDate >= min_date) and (FileDate <= max_date):

                PassingFilesToLoad = numpy.append(PassingFilesToLoad, line)
                print FileDate, line
        # print PassingFilesToLoad
        if len(cuts_to_load) > 1:
            try:
                cuts = rfn.merge_arrays(
                    [cuts,
                    root2array(PassingFilesToLoad,
                                'cutDir/cutzip%0.1d' % detnum,
                                [i])],
                    flatten=True,
                    usemask=False)
            except:
                cuts = rfn.merge_arrays(
                    [cuts,
                    root2array(PassingFilesToLoad,
                                'cutDir/cutevent',
                                [i])],
                    flatten=True,
                    usemask=False)

        else:
            print i, detnum
            try:
                cuts = root2array(
                    PassingFilesToLoad, 'cutDir/cutzip%0.1d' %
                    detnum, [i])
            except:
                cuts = root2array(
                    PassingFilesToLoad, 'cutDir/cutevent',
                    [i])


        #cuts = root2array(PassingFilesToLoad, 'cutDir/cutzip%0.1d'%detnum)
        #cuts = numpy.append(cuts, root2array(PassingFilesToLoad, 'cutDir/cutzip%0.1d'%detnum))
        PassingFilesToLoad = []

    if len(AllFiles) == -11111111:
        for i in cuts_to_load:
            AllFiles = glob(LoadingData + '/' + i + '/*.root')

            for line in AllFiles:
                FileDate = numpy.int(line.split("_")[-2][0:-2])
                print FileDate
                FileDate = FileDate - 10000
                if (FileDate >= min_date) and (FileDate <= max_date):
                    PassingFilesToLoad = numpy.append(PassingFilesToLoad, line)
            cuts = numpy.append_fields(
                cuts,
                i,
                root2array(
                    numpy.sort(
                        PassingFilesToLoad),
                    'cutDir/cutzip%0.1d' %
                    detnum))
            PassingFilesToLoad = []

    PassingFilesToLoad = []

    # now loading the data....
    return cuts
