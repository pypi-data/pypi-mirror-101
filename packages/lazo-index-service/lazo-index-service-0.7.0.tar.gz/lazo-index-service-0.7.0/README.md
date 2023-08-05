# Lazo Index Service Client

Client library for indexing and querying the [Lazo Index Service](https://gitlab.com/ViDA-NYU/auctus/lazo-index-service).

## How to install?

    $ pip install lazo-index-service

## How to run?

First, instantiate the client:

```python
import lazo_index_service

lazo_client = lazo_index_service.LazoIndexClient(host=SERVER_HOST, port=SERVER_PORT)
```

where `SERVER_HOST` and `SERVER_PORT` are the hostname and the port where the Lazo index server is running, respectively.

To index a set of values:

```python
(n_permutations, hash_values, cardinality) = lazo_client.index_data(
    VALUES,
    DATASET_NAME,
    COLUMN_NAME
)
```

where `VALUES` is the list of string values, and `DATASET_NAME` and `COLUMN_NAME` are the names of the dataset/column from where the values come from. The tuple `(n_permutations, hash_values, cardinality)` represents the corresponding Lazo sketch.

If server and client are co-located, you can send the path to the dataset `csv` file instead, which should be significantly more efficient:

```python
lazo_sketches = lazo_client.index_data_path(
    DATA_PATH,
    DATASET_NAME,
    COLUMN_NAME_LIST
)
```

where `DATA_PATH` is the path to the dataset `csv` file, `DATASET_NAME` is the name of the dataset, and `COLUMN_NAME_LIST` is a list of column names. The return, `lazo_sketches`, is a list of `(n_permutations, hash_values, cardinality)` tuples, where each tuple corresponds to a dataset column.

To simply compute and retrieve the Lazo sketches, without adding them to the index, `get_lazo_sketch_from_data` or `get_lazo_sketch_from_data_path` can be used:

```python
(n_permutations, hash_values, cardinality) = lazo_client.get_lazo_sketch_from_data(
    VALUES,
    DATASET_NAME,
    COLUMN_NAME
)

lazo_sketches = lazo_client.get_lazo_sketch_from_data_path(
    DATA_PATH,
    DATASET_NAME,
    COLUMN_NAME_LIST
)
```

To query the index:

```python
query_results = lazo_client.query_data(
    QUERY_VALUES
)
```

where `QUERY_VALUES` is the list of values to be used for the query.

If server and client are co-located, and the values to be used for the query come from a dataset, you can send the path to its corresponding `csv` file instead:

```python
query_results_list = lazo_client.query_data_path(
    DATA_PATH,
    DATASET_NAME,
    COLUMN_NAME_LIST
)
```

It is also possible to delete sketches from the index:

```python
ack = lazo_client.remove_sketches(
    DATASET_NAME,
    COLUMN_NAME_LIST
)
```

where `ack` returns `True` if the requested columns are successfully deleted from the index.
