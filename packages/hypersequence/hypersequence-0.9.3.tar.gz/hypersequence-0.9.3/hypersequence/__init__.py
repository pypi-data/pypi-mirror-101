import pathlib as pl
import numpy as np
import json
import os
import mmap
import platform
import typing

try:
    from tensorflow.keras import utils as ku
    _HAS_TF_KERAS = True
except ImportError:
    _HAS_TF_KERAS = False
    pass

__version__ = "0.9.3"

_MAX_META_SIZE = 1024
_META_SIGNATURE = "@@FSEQ@@"

_PLATFORM = platform.system()

def _share_array(array, *shares):
    """
    Split an array into shares.

    :param array:       The array of elements to divide into shares
    :param shares:      The shares [0..1), by proportion.
    :return:            Return len(shares)+1 arrays of which the number of items is proportional to shares.
    """
    if np.sum(np.round(np.array(shares) * len(array))) >= len(array):
        raise ValueError("Sum of rounded shares equals or exceeds array capacity")

    split_set = []
    orig_size = len(array)
    for s in shares:
        selection = np.zeros(len(array), dtype=bool)
        items = int(np.round(orig_size * s))
        if items < 1:
            raise ValueError("Can't split dataset as specified, one subset will not have any items")
        selection[np.round(np.linspace(0, len(array) - 1, items)).astype(int)] = True
        split_set.append(array[selection])
        array = array[~selection]

    if len(array) == 0:
        raise ValueError("Can't split dataset as specified, one subset will not have any items")

    split_set.append(array)

    return split_set


class HyperSequenceWriter:
    """
        HyperSequenceWriter is a class for building sequences for NN training.
    """

    def __init__(self, output_file: str or pl.Path, batch_size: int = 16):
        """
        Create a new FastSequenceWriter for writing HyperSequence format files.

        A HyperSequence has a native batch size, which is used as the granularity with which the data is written and
        read. Input data will be batched to given batch size, and remaining data will be discarded, e.g. given a batch
        size of 100, writing 250 input and output sets will cause the last 50 sets of be discarded. However, performance
        wise a small batch size will come with a performance penalty.

        When using a HyperSequence file is it possible to overwrite the batch size, but within limits, and this also
        incurs a performance penalty.

        :param output_file:     Output file to write to, should have ".hsq" extension.
        :param batch_size:      Native batch size, must be >= 1
        """
        self._output_file = pl.Path(output_file)
        self._batch_size = batch_size
        self._fp = None
        self._dtype = None
        self._stacks = None
        self._batch_count = 0
        self._closed = False
        self._in_dtypes = None
        self._records = 0
        self._no_inputs = None
        self._no_outpus = None

    def _write_meta_file(self):
        meta_data = {
            "version": __version__,
            "records": self._records,
            "batch_size": self._batch_size,
            "no_inputs": self._no_inputs,
            "no_outputs": self._no_outputs,
            "dtype": self._dtype.descr
        }
        self._fp.write(_META_SIGNATURE.encode("ascii"))
        self._fp.write(json.dumps(meta_data).encode("ascii"))

    def close(self):
        if self._closed or self._fp is None:
            return

        self._closed = True

        self._write_meta_file()

        self._fp.close()
        self._fp = None

    def _init_dtype(self, inputs, outputs):
        self._in_dtypes = [arr.dtype for arr in inputs + outputs]
        self._no_inputs = len(inputs)
        self._no_outputs = len(outputs)

        input_struct = [(f"i{i}", inp.dtype, (self._batch_size, ) + inp.shape, )
                        for i, inp in enumerate(inputs)]
        output_struct = [(f"o{i}", out.dtype, (self._batch_size, ) + out.shape)
                         for i, out in enumerate(outputs)]

        self._dtype = np.dtype(input_struct + output_struct)
        self._stacks = [[] for _ in range(len(inputs) + len(outputs))]

    def _flush(self):
        record = np.array(tuple(np.stack(stack) for stack in self._stacks), dtype=self._dtype)

        if self._fp is None:
            self._fp = open(self._output_file, "wb")
        record.tofile(self._fp)
        self._records += 1

        for stack in self._stacks:
            stack.clear()

    def append(self,
               inputs: typing.Tuple[np.ndarray] or np.ndarray,
               outputs: typing.Tuple[np.ndarray] or np.ndarray):
        """
        Append training data to the HyperSequence file.

        :param inputs:      single ndarray or Tuple or ndarray input data.
        :param outputs:     single ndarray or Tuple or ndarray output data.
        """

        if self._closed:
            raise IOError("File already closed")

        if not isinstance(inputs, tuple):
            inputs = (inputs, )
        if not isinstance(outputs, tuple):
            outputs = (outputs, )

        if self._dtype is None:
            self._init_dtype(inputs, outputs)

        for exp_dt, arr, stack in zip(self._in_dtypes, inputs + outputs, self._stacks):
            if arr.dtype != exp_dt:
                raise ValueError(f"Expected array of type {exp_dt} but was {arr.dtype}")
            stack.append(arr)

        if self._batch_count == self._batch_size - 1:
            self._flush()
            self._batch_count = 0
        else:
            self._batch_count += 1

    def __enter__(self):
        return self

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()


class HyperSequence:
    """
        HyperSequence super-class
    """

    def shuffle(self):
        """
        Shuffle the underlying indices
        :return:
        """
        raise RuntimeError(f"Class {self.__class__} does not support shuffle")

    def split(self, *shares):
        """
        Split data into two or more subsets.
        Provide N floating points (N >= 1), of which the sum is < 1. Will return N+1 items.

        Each floating value is the share of the dataset for that set.

        For example, split 80 train, 20 test:
            train, test = hsq.split(0.8)

        For example, split 70 train, 20 test, 10 verify:
            train, test, verify = hsq.split(0.7, 0.2)
        :param args:
        :return:
        """

        indices = np.arange(0, len(self), dtype=int)
        sub_sets = _share_array(indices, *shares)

        return tuple(HyperSequenceView(self, sub_set) for sub_set in sub_sets)

    def dtypes(self):
        """
        Get the data-types returned by this sequence
        :return: input, output tuples containing dtypes
        """
        raise NotImplementedError("dtypes")

    def no_inputs(self):
        raise NotImplementedError("no_inputs")

    def no_outputs(self):
        raise NotImplementedError("no_outputs")

    def batch_size(self):
        raise NotImplementedError("batch_size")

    def __len__(self):
        raise NotImplementedError("__len__")

    def _get(self, index: int):
        raise NotImplementedError("_get")

    def __getitem__(self, item):
        raw = self._get(item)
        no_in = self.no_inputs()
        no_out = self.no_outputs()
        return tuple(raw[0:no_in]) if no_in != 1 else raw[0],\
               tuple(raw[no_out:]) if no_out != 1 else raw[no_in]

class HyperSequenceChild(HyperSequence):

    def __init__(self, parent : HyperSequence):
        super(HyperSequenceChild, self).__init__()
        self._fs = parent

    def shuffle(self):
        self._fs.shuffle()

    def no_inputs(self):
        return self._fs.no_inputs()

    def no_outputs(self):
        return self._fs.no_outputs()

    def batch_size(self):
        return self._fs.batch_size()

    def dtypes(self):
        return self._fs.dtypes()

    def __len__(self):
        return self._fs.__len__()

    def _get(self, index: int):
        return self._fs._get(index)


class HyperSequenceFile(HyperSequence):
    """
        HyperSequenceFile maps the HyperSequence file to memory.

        Note: Arrays returned use a memory mapped file in the background. The numpy arrays are only valid for as long
        as the file is open. To use the data from this sequence after the file is closed you must make a copy!
    """

    def __init__(self, hyper_seq_file: pl.Path or str):
        """
        :param hyper_seq_file:
        :param batch_size:
        """

        self._input_file = hyper_seq_file
        self._fp = open(self._input_file, "rb")
        self._load_meta()
        # internally we use mmap!
        mmap_kwargs = {}

        if _PLATFORM == "Linux":
            mmap_kwargs["prot"] = mmap.PROT_READ
        elif _PLATFORM == "Windows":
            mmap_kwargs["access"] = mmap.ACCESS_READ

        self._mmap = mmap.mmap(self._fp.fileno(), self._records * self._dtype.itemsize,
                               offset=0, **mmap_kwargs)

    def _load_meta(self):
        # Meta-data is located at the end of the file. To be sure we'll read the last _MAX_META_SIZE bytes
        # from the end of the file and search for _META_SIGNATURE. The JSON encoded meta-data should be
        # trailing this marker.
        self._fp.seek(0, os.SEEK_END)
        file_size=self._fp.tell()
        load_offset=file_size-_MAX_META_SIZE
        if load_offset < 0:
            load_offset = 0

        self._fp.seek(load_offset)
        meta_block = self._fp.read(_MAX_META_SIZE).decode("latin_1")

        p = meta_block.rfind(_META_SIGNATURE)
        if p == -1:
            raise RuntimeError("Failed to find meta-data")
        json_data = meta_block[p+len(_META_SIGNATURE):]
        meta_data = json.loads(json_data)

        self._records = meta_data["records"]
        self._batch_size = meta_data["batch_size"]
        self._no_inputs = meta_data["no_inputs"]
        self._no_outputs = meta_data["no_outputs"]
        self._dtype = np.dtype([tuple(named) for named in meta_data["dtype"]])
        self._in_dtypes = None
        self._out_dtypes = None

        unpacked = [np.dtype((self._dtype[name].base, self._dtype[name].shape[1:])) for name in self._dtype.names]
        self._in_dtypes = tuple(unpacked[0:self._no_inputs])
        self._out_dtypes = tuple(unpacked[self._no_inputs:])

    def dtypes(self):
        return self._in_dtypes, self._out_dtypes

    def no_inputs(self):
        return self._no_inputs

    def no_outputs(self):
        return self._no_outputs

    def batch_size(self):
        return self._batch_size

    def __len__(self):
        return self._records

    def _get(self, index: int):
        if index < 0 or index >= self._records:
            raise IndexError(f"Out of bounds: {index}")
        return np.frombuffer(self._mmap, self._dtype, count=1, offset=index * self._dtype.itemsize)[0].item()

    def close(self):
        """
        Close the file. After this access to the data provided by this array is no longer valid, and the application
        may crash if you try to do so.
        """
        if self._fp is None:
            return
        self._mmap.close()
        self._fp.close()
        self._fp = None

    def __enter__(self):
        return self

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()


class _HyperSequenceSupBatch(HyperSequenceChild):

    def __init__(self, hyperseq: HyperSequence, new_batch_size: int):
        if new_batch_size % hyperseq.batch_size() != 0:
            raise ValueError("new_batch_size must be multiple of original batch size")

        super(_HyperSequenceSupBatch, self).__init__(hyperseq)
        self._batch_size = new_batch_size
        self._factor = new_batch_size // self._fs.batch_size()
        self._len = len(self._fs) // self._factor
        self._depth = self._fs.no_inputs() + self._fs.no_outputs()

    def batch_size(self):
        return self._batch_size

    def __len__(self):
        return self._len

    def _get(self, index: int):
        offset = index * self._factor
        stacks = [[] for _ in range(self._depth)]

        for pos in range(self._factor):
            for s, d in zip(stacks, self._fs._get(offset+pos)):
                s.append(d)

        stacks = [np.concatenate(s) for s in stacks]

        return stacks


class _HyperSequenceSubBatch(HyperSequenceChild):

    def __init__(self, hyperseq: HyperSequence, new_batch_size: int):
        if hyperseq.batch_size() % new_batch_size != 0:
            raise ValueError("new_batch_size must be divisor of original batch size")

        super(_HyperSequenceSubBatch, self).__init__(hyperseq)
        self._batch_size = new_batch_size
        self._factor = self._fs.batch_size() // new_batch_size
        self._len = len(self._fs) * self._factor
        self._depth = self._fs.no_inputs() + self._fs.no_outputs()

    def batch_size(self):
        return self._batch_size

    def __len__(self):
        return self._len

    def _get(self, index: int):
        par_index = index // self._factor
        off = (index % self._factor) * self._batch_size

        raw = self._fs._get(par_index)
        return [a[off:off+self._batch_size] for a in raw]


def rebatch(hyperseq: HyperSequence, new_batch_size: int):
    if new_batch_size > hyperseq.batch_size():
        return _HyperSequenceSupBatch(hyperseq, new_batch_size)
    elif new_batch_size < hyperseq.batch_size():
        return _HyperSequenceSubBatch(hyperseq, new_batch_size)
    else:
        return hyperseq


class HyperSequenceView(HyperSequenceChild):
    """
    A view on HyperSequenceFile with different indices
    """

    def __init__(self, hyperseq: HyperSequence, indices: np.ndarray or None=None):
        super(HyperSequenceView, self).__init__(hyperseq)
        if indices is None:
            self._indices = np.arange(0, len(self._fs), dtype=int)
        else:
            self._indices = indices

    def shuffle(self):
        """
        Shuffle the elements in the set
        """
        np.random.shuffle(self._indices)

    def __len__(self):
        return len(self._indices)

    def _get(self, index: int):
        return self._fs._get(self._indices[index])


if _HAS_TF_KERAS:
    class KerasSequence(ku.Sequence):

        def __init__(self, hyperseq: HyperSequenceFile or HyperSequenceView, shuffle_on_epoch: bool = False):
            super(KerasSequence, self).__init__()

            # shuffle is only possible on a view
            if shuffle_on_epoch and isinstance(hyperseq, HyperSequenceFile):
                hyperseq = HyperSequenceView(hyperseq)

            self._hyperseq = hyperseq
            self._shuffle_on_epoch = shuffle_on_epoch
            if self._shuffle_on_epoch:
                self._hyperseq.shuffle()

        def __len__(self):
            return len(self._hyperseq)

        def __getitem__(self, index: int):
            return self._hyperseq[index]

        def on_epoch_end(self):
            if self._shuffle_on_epoch:
                self._hyperseq.shuffle()

else:
    class KerasSequence(ku.Sequence):

        def __init__(self, hyperseq: HyperSequenceFile or HyperSequenceView, shuffle_on_epoch: bool = False):
            raise RuntimeError("Please install tensorflow >= 2.0 first")
