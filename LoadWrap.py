"""
LoadWrap is a madule that provides a convience wrapper object around peter's
Load functions. It is a quick attempt to provide a persistent object that remembers
what data you have loaded incase you want some more like it.
"""

from . import LoadFunction
import numpy


class data(object):

    """The class describes some convience methods to access root data
    with """

    def __init__(
        self, detnum, min_date=0, max_date=numpy.inf, which_dataSet='ba',
            data_location='/data3/cdmsbatsProd/R133/dataReleases/Prodv5-3_June2013/merged'):
        self.min_date = min_date
        self.max_date = max_date
        self.which_dataSet = which_dataSet
        self.data_location = data_location
        self.detnum = detnum
        self.kwargs = {
            'detnum': detnum,
            'min_date': min_date,
            'max_date': max_date,
            'which_dataSet': which_dataSet,
            'data_location': data_location}
        self.loaded_rrqs = []
        self.loaded_rqs = []
        self.loaded_cuts = []

    def rrq(self, rrqs_to_load=[], eventRQ=False):
        self.kwargs['rrqs_to_load'] = rrqs_to_load
        for rrq in rrqs_to_load:
            self.loaded_rrqs.append(rrq)
        self.kwargs['eventRQ'] = eventRQ
        kwargs = self.kwargs
        kwargs['data_location'] = self.data_location + '/all'
        return LoadFunction.LoadRRQ(**kwargs)

    def rq(self, rqs_to_load=[], eventRQ=False):
        self.kwargs['rqs_to_load'] = rqs_to_load
        for rq in rqs_to_load:
            self.loaded_rqs.append(rq)
        self.kwargs['eventRQ'] = eventRQ
        kwargs = self.kwargs
        kwargs['data_location'] = self.data_location + '/all'
        return LoadFunction.LoadRQ(**kwargs)

    def cut(self, cuts_to_load=[]):
        self.kwargs['cuts_to_load'] = cuts_to_load
        for cut in cuts_to_load:
            self.loaded_cuts.append(cut)
        kwargs = self.kwargs
        kwargs['data_location'] = self.data_location + '/cuts'
        return LoadFunction.LoadCut(**kwargs)
