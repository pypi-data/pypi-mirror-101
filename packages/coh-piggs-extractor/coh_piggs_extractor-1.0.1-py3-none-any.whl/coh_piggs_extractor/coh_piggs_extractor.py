'''
Inspiration for this parser has been taken from https://github.com/ovekaaven/cohtools/blob/master/readpigg.py and
reuses sections of code this therefore continues the original copyright from that source

Copyright (c) 2016 Ove Kåven (https://github.com/ovekaaven)
Copyright (c) 2021 CoderSparks (https://github.com/codersparks)
'''

import datetime
import logging
import os
import os.path
import struct
import zlib

_logger = logging.getLogger(__name__)


def is_match(name, args):
    if len(args) == 0:
        return True
    # FIXME: handle wildcards?
    return name in args


class DirEntry(object):
    def __init__(self, dirent):
        self.name = None
        self.slot = None
        self.strnum = dirent[1]
        self.fsize = dirent[2]
        self.tstamp = datetime.datetime.fromtimestamp(dirent[3])
        self.offset = dirent[4]
        self.slotnum = dirent[6]
        self.md5 = dirent[7]
        self.csize = dirent[8]


class PiggFile(object):
    """
    The piggFile object processes the specified file into the relevant details, using the supplied strategy for further
    processing the extracted files
    """

    def __init__(self, fname, strategy):
        """
        Constructor
        :param fname: filename/path of piggs file to process
        :param strategy: The implementation of PiggFileEntryProcessingStrategy to use to process the entries of the file
        """
        self.strategy = strategy
        self.fname = fname
        self.files = []
        self.strings = []
        self.slots = []

        self.f = open(fname, "rb")

        hdr = self.read_struct("<LHHHHL", 16)
        if hdr[0] != 0x123:
            _logger.error("Not a PIGG file!")
            return
        ents = hdr[5]

        # read directory entries
        for n in range(0, ents):
            ent = self.read_struct("<LLLLLLL16sL", 48)
            self.files.append(DirEntry(ent))

        # read string table
        strhdr = self.read_struct("<LLL", 12)
        if strhdr[0] != 0x6789:
            _logger.info("Invalid string table!")
            return

        pos = self.f.tell()

        for n in range(0, strhdr[1]):
            s = self.read_string()
            self.strings.append(s)

        # read slot table
        pos += strhdr[2]
        self.f.seek(pos)
        slothdr = self.read_struct("<LLL", 12)
        if slothdr[0] != 0x9abc:
            _logger.info("Invalid slot table!")
            return
        for n in range(0, slothdr[1]):
            s = self.read_vardata()
            ds = self.decompress_slot(s)
            self.slots.append(s)

        # fixup file list
        for ent in self.files:
            if ent.strnum < len(self.strings):
                ent.name = self.strings[ent.strnum]
            if ent.slotnum < len(self.slots):
                ent.slot = self.slots[ent.slotnum]

    def extract_files(self, out_dir="out"):
        for ent in self.files:
            name = ent.name

            _logger.debug("Extracting %s..." % name)
            self.f.seek(ent.offset)
            if ent.csize == 0:
                data = self.f.read(ent.fsize)
            else:
                cdata = self.f.read(ent.csize)
                data = zlib.decompress(cdata)

            self.strategy.process_pigg_file_entry(ent, data)




    def decompress_slot(self, data):
        fsize = struct.unpack("<L", data[:4])[0]
        if fsize == len(data):
            return data[4:]
        (fsize, csize) = struct.unpack("<LL", data[:8])
        if fsize + 4 != len(data):
            _logger.info("Slot size mismatch:", fsize, csize, len(data))
        if csize == 0:
            return data[8:]
        else:
            return zlib.decompress(data[8:])

    def read_struct(self, format, size):
        if size is None:
            size = struct.calcsize(format)
        data = self.f.read(size)
        return struct.unpack(format, data)

    def read_vardata(self):
        slen = self.read_struct("<L", 4)[0]
        data = self.f.read(slen)
        return data

    def read_string(self):
        # strip final null byte
        return self.read_vardata()[:-1]


class PiggFileEntryProcessingStrategy(object):
    """
    A simple no-op strategy that others can extend from
    """

    def process_pigg_file_entry(self, meta, data):
        pass

class SimpleFileOutputEntryProcessingStrategy(PiggFileEntryProcessingStrategy):
    """
    This simple strategy outputs each of the files (maintaining internal directory structure) to the folder passed at
    construction
    """

    def __init__(self, out_dir):
        """
        Constructor
        :param out_dir: The directory to output the files to
        """
        self.out_dir = out_dir

    def process_pigg_file_entry(self, meta, data):
        output_file = os.path.join(self.out_dir, meta.name.decode('utf-8'))

        output_folder = os.path.dirname(output_file)

        if not os.path.exists(output_folder):
            os.makedirs(os.path.dirname(output_file))

        with open(output_file, "wb") as df:
            df.write(data)