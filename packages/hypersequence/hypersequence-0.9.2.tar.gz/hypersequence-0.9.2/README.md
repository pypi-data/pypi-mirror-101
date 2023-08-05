HyperSequence
============
HyperSequence is a data format and library for super-fast training of large machine learning datasets. HyperSequence aims to be much faster than conventional data pipelining solutions, especially with larger records.

Features:
 * Simple API to write datasets
 * Supports multiple inputs and outputs per training record
 * Functions for rebatching, randomization and splitting
 * tensorflow.keras integration


Usage
-----
### Building a dataset
To write create a `HyperSequenceWriter` and call `.append(inputs=..., outputs=...)` for every row you wish to add to the dataset.

```python
import hypersequence as hs
import numpy as np

test_file = "/data/myset.hsq"
batch_size = 16
no_of_recs = 10000

with hs.HyperSequenceWriter(test_file, batch_size) as hsw:
    for i in range(no_of_recs):
        inp = np.random.random((10, 10))
        out = np.random.random((2, 10, 2))
        hsw.append(inputs=inp, outputs=out)
```
Note that `HyperSequenceWriter` has a native batch-size granularity. It will be optimized for this batch-size. Though it is possible to deviate from this batch-size, this comes at a (often small) performance penalty. Moreover, batch-sizes are constrained to either a divider or multiple of the native batch-size.

### Training the dataset using tensorflow.keras
Training with HyperSequence is also straight-forward. Create a `HyperSequenceFile` and use `KerasSequence` wrapper class to feed it to the Fit function.

```python
import hypersequence as hs
import numpy as np
import tensorflow.keras as tfk

test_file = "/data/myset.hsq"

with hs.HyperSequenceFile(test_file) as hsq:
    (inp_dtype,), (out_dtype,) = hsq.dtypes()

    model = tfk.models.Sequential(
        [
            tfk.layers.InputLayer(input_shape=inp_dtype.shape),
            tfk.layers.Flatten(),
            tfk.layers.Dense(np.prod(out_dtype.shape), activation='relu'),
            tfk.layers.Reshape(out_dtype.shape)
        ]
    )
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(
        hs.KerasSequence(hsq, shuffle_on_epoch=True),
        epochs=16,
        batch_size=hsq.batch_size()
    )
```
Note the `shuffle_on_epoch` can be used to randomize the order of the dataset before each epoch.

### Multi-Input/Multi-Output
HyperSequence supports multi-input/output for more complex training datasets.

```python
import hypersequence as hs
import numpy as np

test_file = "/data/myset.hsq"
batch_size = 16
no_of_recs = 10000

with hs.HyperSequenceWriter(test_file, batch_size) as hsw:
    for i in range(no_of_recs):
        inp1 = np.random.random((10, 10))
        inp2 = np.random.random(100)
        inp3 = np.random.random((3, 3, 3))
        out1 = np.random.random((2, 10, 2))
        out2 = np.random.random((100))
        hsw.append(inputs=(inp1, inp2, inp3), outputs=(out1, out2))
```

### Splitting the dataset into training and validation
Using `HyperSequence.split()` you can split the dataset into multiple sub-sets. 

Here is the same example as above, but with splitting.

```python
import hypersequence as hs
import numpy as np
import tensorflow.keras as tfk

test_file = "/data/myset.hsq"

with hs.HyperSequenceFile(test_file) as hsq:
    train, validation = hsq.split(0.8)

    (inp_dtype,), (out_dtype,) = hsq.dtypes()

    model = tfk.models.Sequential(
        [
            tfk.layers.InputLayer(input_shape=inp_dtype.shape),
            tfk.layers.Flatten(),
            tfk.layers.Dense(np.prod(out_dtype.shape), activation='relu'),
            tfk.layers.Reshape(out_dtype.shape)
        ]
    )
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(
        hs.KerasSequence(train, shuffle_on_epoch=True),
        epochs=16,
        batch_size=train.batch_size(),
        validation_data=hs.KerasSequence(validation)
    )
```

### Changing the batch-size

```python
import hypersequence as hs
import tensorflow.keras as tfk

test_file = "/data/myset.hsq"

with hs.HyperSequenceFile(test_file) as hsq:
    # Rebatch from 16 records to 64 records.
    hsq64 = hs.rebatch(hsq, 64)
    # Split for training and validation
    train, validation = hsq64.split(0.8)

    # create model as before....

    # Train!
    model.fit(
        hs.KerasSequence(train, shuffle_on_epoch=True),
        epochs=16,
        batch_size=hsq64.batch_size(),
        validation_data=hs.KerasSequence(validation)
    )
```
