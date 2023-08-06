=====
Usage
=====

To use FEMAP neutral Parser in a project::

        >>> from femap_neutral_parser import Parser

To instanciate a new parser, just pass a filepath::

        >>> neutral = Parser("fea.NEU")

To have a list of available blocks::

        >>> neutral.available_blocks()
        {'header': 100, 'output_sets': 450, 'output_vectors': 451}

Access available blocs by attribute::
        >>> neutral.output_sets
        {1: {'title': 'Analyse. NASTRAN SPC 1 - TTL - 9g FWD. test',
          'from_prog': 'Unknown',
          'anal_type': 'Static',
          'process_type': None,
          'integer_format': None,
          'value': 0.0,
          'notes': ''},
         2: {'title': 'Analyse. NASTRAN SPC 1 - TTL - 6.9g DOWN. test',
          'from_prog': 'Unknown',
          'anal_type': 'Static',
          'process_type': None,
          'integer_format': None,
          'value': 0.0,
          'notes': ''}}

Vectors for output (block451) are organized as nested dictionnaries ``[<vector title>][<LCID>]``::
        >>> neutral.output_vectors["Total Translation"][2]
        {'vecID': 1,
         'min_val': 0.0,
         'max_val': 0.4330393,
         'abs_max': 0.4330393,
         'component_vec': [10002.0, 10003.0, 10004.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
         'id_min': 1,
         'id_max': 931,
         'calc_warn': True,
         'comp_dir': 1,
         'cent_total': True,
         'record': array([(   1, 0.        ), (   2, 0.        ), (   3, 0.00546075), ...,
                (1363, 0.01782945), (1364, 0.1146496 ), (1365, 0.01633955)],
               dtype=[('nodeID', '<i8'), ('disp', '<f8')])}

To access the ``numpy.ndarray`` wrapping the actual values, just get the ``record`` key::

        >>> arr = neutral.output_vectors["Total Translation"][2]["record"]
        >>> arr
        array([(   1, 0.        ), (   2, 0.        ), (   3, 0.00923191), ...,
               (1363, 0.00986211), (1364, 0.1818963 ), (1365, 0.2173212 )],
              dtype=[('nodeID', '<i8'), ('disp', '<f8')])

which is actually a `structured numpy array <https://numpy.org/doc/stable/user/basics.rec.html>`_. This makes easier some processing or conversion to Pandas DataFrames (if Pandas is available)::

        >>> arr["nodeID"]
        array([   1,    2,    3, ..., 1363, 1364, 1365])
        >>> import pandas as pd
        >>> pd.DataFrame(arr)
              nodeID      disp
        0          1  0.000000
        1          2  0.000000
        2          3  0.009232
        3          4  0.000000
        4          5  0.009233
        ...      ...       ...
        1360    1361  0.225661
        1361    1362  0.014259
        1362    1363  0.009862
        1363    1364  0.181896
        1364    1365  0.217321

        [1365 rows x 2 columns]




