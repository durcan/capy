"""
This module handles conversion of ROOT's TFile and
contained TTrees into HDF5 format with PyTables
"""
import os
import sys
import warnings

from rootpy.io import root_open, TemporaryFile
from rootpy import log; log = log[__name__]
from rootpy.extern.progressbar import ProgressBar, Bar, ETA, Percentage

from root_numpy import tree2rec, RootNumpyUnconvertibleWarning

import pandas as pd


def _drop_object_col(rec, warn=True):
    # ignore columns of type `object` since PyTables does not support these
    if rec.dtype.hasobject:
        names = []
        fields = rec.dtype.fields
        for name in rec.dtype.names:
            if fields[name][0].kind != 'O':
                names.append(name)
            elif warn:
                log.warning(
                    "ignoring unsupported object branch '{0}'".format(name))
        return rec[names]
    return rec

def check_tty(stream):
    if not hasattr(stream, 'fileno'):
        return False
    try:
        fileno = stream.fileno()
        return os.isatty(fileno)
    except (OSError, IOError):
        return False

def convert(rfile, hfile, rpath='', entries=-1, userfunc=None, selection=None, indexes=False):

    isatty = check_tty(sys.stdout)
    if isatty:
        widgets = [Percentage(), ' ', Bar(), ' ', ETA()]

    own_h5file = False
    if isinstance(hfile, basestring):
        hfile = pd.HDFStore(hfile)
        own_h5file = True
    own_rootfile = False
    if isinstance(rfile, basestring):
        rfile = root_open(rfile)
        own_rootfile = True
    for dirpath, dirnames, treenames in rfile.walk(
            rpath, class_pattern='TTree'):

        # skip root
        if not dirpath and not treenames:
            continue

        # skip directories w/o trees or subdirs
        if not dirnames and not treenames:
            continue

        where_group = '/' + os.path.dirname(dirpath)
        current_dir = os.path.basename(dirpath)

        #if not current_dir:
            #group = hfile.root
        #else:
            #group = hfile.createGroup(where_group, current_dir, "")

        ntrees = len(treenames)
        log.info(
            "Will convert {0:d} tree{1} in this directory".format(
                ntrees, 's' if ntrees != 1 else ''))
        for treename in treenames:

            input_tree = rfile.Get(os.path.join(dirpath, treename))
            path_to_tree = os.path.join(dirpath, treename)

            if userfunc is not None:
                tmp_file = TemporaryFile()
                # call user-defined function on tree and get output trees
                log.info("Calling user function on tree '{0}'".format(
                    input_tree.GetName()))
                trees = userfunc(input_tree)

                if not isinstance(trees, list):
                    trees = [trees]

            else:
                trees = [input_tree]
                tmp_file = None

            for tree in trees:

                log.info("Converting tree '{0}' with {1:d} entries ...".format(
                    tree.GetName(),
                    tree.GetEntries()))

                #if tree.GetName() in group:
                    #log.warning(
                        #"skipping tree '{0}' that already exists "
                        #"in the output file".format(tree.GetName()))
                    #continue

                total_entries = tree.GetEntries()
                pbar = None
                if isatty and total_entries > 0:
                    pbar = ProgressBar(widgets=widgets, maxval=total_entries)

                if entries <= 0:
                    # read the entire tree
                    if pbar is not None:
                        pbar.start()
                    recarray = tree2rec(tree, selection=selection)
                    recarray = pd.DataFrame(_drop_object_col(recarray))
                    hfile.append(path_to_tree, recarray, data_columns = indexes)
                    #table = hfile.createTable(
                        #group, tree.GetName(),
                        #recarray, tree.GetTitle())
                    ## flush data in the table
                    #table.flush()
                    ## flush all pending data
                    #hfile.flush()
                else:
                    # read the tree in chunks
                    offset = 0
                    while offset < total_entries or offset == 0:
                        if offset > 0:
                            with warnings.catch_warnings():
                                warnings.simplefilter(
                                    "ignore",
                                    RootNumpyUnconvertibleWarning)
                                recarray = tree2rec(
                                    tree,
                                    entries=entries,
                                    offset=offset,
                                    selection=selection)
                            recarray = pd.DataFrame(_drop_object_col(recarray, warn=False))
                            #table.append(recarray)
                            hfile.append(path_to_tree,recarray, data_columns = indexes)
                        else:
                            recarray = tree2rec(
                                tree,
                                entries=entries,
                                offset=offset,
                                selection=selection)
                            recarray = pd.DataFrame(_drop_object_col(recarray))
                            if pbar is not None:
                                # start after any output from root_numpy
                                pbar.start()
                            #table = hfile.createTable(
                                #group, tree.GetName(),
                                #recarray, tree.GetTitle())
                            hfile.append(path_to_tree,recarray, data_columns = indexes)
                        offset += entries
                        if offset <= total_entries and pbar is not None:
                            pbar.update(offset)
                        ## flush data in the table
                        #table.flush()
                        ## flush all pending data
                        #hfile.flush()

                if pbar is not None:
                    pbar.finish()

            input_tree.Delete()

            if userfunc is not None:
                for tree in trees:
                    tree.Delete()
                tmp_file.Close()

    if own_h5file:
        hfile.close()
    if own_rootfile:
        rfile.Close()
