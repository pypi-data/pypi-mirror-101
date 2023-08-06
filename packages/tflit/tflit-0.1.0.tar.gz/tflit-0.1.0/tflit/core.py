import numpy as np
import tflite_runtime.interpreter as tflite
from . import util


class Model:
    '''Tflite Model, providing a similar interface to Keras.
    
    Example:
    >>> model = tflit.Model('path/to/model.tflite', batch_size=32, num_threads=3)
    >>> model.summary()
    >>> model.predict(X)  # if multiple inputs, X is a list, otherwise, just the array.
    '''
    input_details = ()
    output_details = ()
    multi_input = multi_output = True
    _input_idxs = ()
    _output_idxs = ()
    def __init__(self, model_path, inputs=None, outputs=None, batch_size=None, model_content=None, num_threads=None, **kw):
        self.model_path = model_path
        self.interpreter = tflite.Interpreter(model_path, num_threads=num_threads, **kw)
        self._given_input_idxs = inputs
        self._given_output_idxs = outputs
        self.reallocate()

        # update batch if provided
        if batch_size:
            self.set_batch_size(batch_size)

    def __repr__(self):
        return '{}( {!r}, in={} out={} )'.format(
            self.__class__.__name__, self.model_path,
            self.input_shape, self.output_shape)

    def reallocate(self):
        '''Will reallocate tensors and refresh tensor details.'''
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # convert user inputted indexes to the actual tensor indexes
        self._input_idxs, self.multi_input = util.get_auto_index(
            self._given_input_idxs, self.input_details)
        self._output_idxs, self.multi_output = util.get_auto_index(
            self._given_output_idxs, self.output_details)

    def set_batch_size(self, batch_size):
        '''Change the batch size of the model.'''
        # set batch for inputs
        for d in self.input_details:
            self.interpreter.resize_tensor_input(
                d['index'], [batch_size] + list(d['shape'][1:]))
    
        # set batch for outputs
        for d in self.output_details:
            self.interpreter.resize_tensor_input(
                d['index'], [batch_size] + list(d['shape'][1:]))
    
        # apply changes
        self.reallocate()
        assert self.batch_size == batch_size, 'batch size expected to be {}, but was {}.'.format(batch_size, self.batch_size)

    def reset(self):
        '''Reset all interpreter variables.'''
        self.interpreter.reset_all_variables()


    def __getitem__(self, key):
        '''Returns a numpy view pointing to the tensor buffer.'''
        return self.interpreter.tensor(key)()

    def get(self, index):
        '''Get a copy of the tensor buffer'''
        return self.interpreter.get_tensor(key)

    ##############
    # Model
    ##############

    def __call__(self, X, *a, **kw):
        '''Call predict on data. Alias for model.predict(...).'''
        return self.predict(X, *a, **kw)

    def predict_batch(self, X, multi_input=None, multi_output=None, add_batch=False):
        '''Predict a single batch.'''
        # set inputs
        X = self._check_inputs(X, multi_input)
        for i, idx in self._input_idxs:
            x = np.asarray(X[i], dtype=self.dtype)
            self.interpreter.set_tensor(idx, x[None] if add_batch else x)

        # compute outputs
        self.interpreter.invoke()

        # get outputs
        return self._check_outputs([
            self.interpreter.get_tensor(idx)
            for i, idx in self._output_idxs], multi_output)

    def predict(self, X, multi_input=None, multi_output=None):
        '''Predict data.'''
        return self._check_outputs([
            np.concatenate(x) for x in zip(*self.predict_each_batch(
                X, multi_input=multi_input, multi_output=True))
        ], multi=multi_output)

    def as_batches(self, X, multi_input=None, multi_output=None):
        '''Yield X in batches.'''
        X = self._check_inputs(X, multi_input)
        batch_size = self.batch_size

        # check that there's only one batch size
        batch_sizes = [len(x) for x in X]
        if len(set(batch_sizes)) != 1:
            raise ValueError(
                'Expected a single batch size. Got {}.'.format(batch_sizes))

        for i in range(0, len(X[0]), batch_size):
            xi = [x[i:i + batch_size] for x in X]
            yield xi if multi_output or len(xi) != 1 else xi[0]

    def predict_each_batch(self, X, multi_input=None, multi_output=None):
        '''Predict and yield each batch.'''
        # NOTE: multi=True so we don't squeeze
        for x in self.as_batches(X, multi_input=multi_input, multi_output=True):
            yield self.predict_batch(x, True, multi_output)


    def _check_inputs(self, X, multi=None):
        # coerce inputs to be a list
        multi = self.multi_input if multi is None else multi
        return X if multi else [X]

    def _check_outputs(self, Y, multi=None):
        # return either a single array or list of arrays depending on
        # single/multi output
        multi = self.multi_output if multi is None else multi
        return Y if multi else Y[0] if len(Y) else None

    ##############
    # Info
    ##############

    # names

    @property
    def input_names(self):
        return [d['name'] for d in self.input_details]

    @property
    def output_names(self):
        return [d['name'] for d in self.output_details]

    # dtypes

    @property
    def input_dtypes(self):
        return [d['dtype'].__name__ for d in self.input_details]

    @property
    def output_dtypes(self):
        return [d['dtype'].__name__ for d in self.output_details]

    @property
    def dtype(self):
        dtypes = set(self.input_dtypes + self.output_dtypes)
        return next(iter(dtypes), None)

    # shapes

    @property
    def input_shapes(self):
        return [tuple(d['shape']) for d in self.input_details]

    @property
    def output_shapes(self):
        return [tuple(d['shape']) for d in self.output_details]

    # shape

    @property
    def input_shape(self):
        shape = self.input_shapes
        return shape[0] if len(shape) == 1 else shape

    @property
    def output_shape(self):
        shape = self.output_shapes
        return shape[0] if len(shape) == 1 else shape

    @property
    def batch_size(self):
        shapes = self.input_shapes
        return shapes[0][0] if shapes else None

    # print

    def summary(self):
        print(util.add_border('\n'.join([
            str(self),
            '', '-- Input details --',
            util.format_details(self.input_details),
            '', '-- Output details --',
            util.format_details(self.output_details),
        ]), ch='.'))
