# `pgb_utils`: Tools for interacting with Pitt-Google Broker

See [tutorials/PGB_Tutorial.ipynb](tutorials/PGB_Tutorial.ipynb) for an intro on accessing our data, both directly using Google Cloud's SDK and with the aid of `pgb_utils`.

Table of Contents
- [`pgb_utils` Python package](#pgb_utils-python-package)
- [Data overview](#data-overview)

## `pgb_utils` Python package

`pgb_utils` is a collection of helper functions to facilitate interaction with Pitt-Google Broker data. The tutorial will demonstrate its use. The package is essentially a set of:

1. Convience wrappers for the [Google Cloud Python SDK](https://cloud.google.com/python/docs/reference)
2. Helper functions for ZTF data decoding and plotting, provided by ZTF (see [Filtering_alerts.ipynb](https://github.com/ZwickyTransientFacility/ztf-avro-alert/blob/master/notebooks/Filtering_alerts.ipynb))
3. Helper functions for running [Apache Beam](https://beam.apache.org/) pipelines

You are encouraged to look at and alter the source code to learn how to use the underlying methods yourself.

Modules and their functionality include:

- `pgb_utils.beam`
    - helper functions for running Apache Beam data pipelines

- `pgb_utils.bigquery`
    - view dataset, table, and schema information
    - query: lightcurves
    - query: cone search
    - cast query results to a `pandas.DataFrame` or `json` formatted string.

- `pgb_utils.figures`
    - plot lightcurves
    - plot cutouts

- `pgb_utils.utils`
    - general utilities such as data type casting


## Data overview

All Pitt-Google Broker data is public and hosted by [Google Cloud](https://cloud.google.com/). In order to make API calls you will need to create a Cloud project that is associated with your Google account.
The Setup section of the tutorial will walk you through this.
Our ZTF data begins ~November 2020.

- Databases
    - [BigQuery](https://cloud.google.com/bigquery)
    - query for:
        - alerts (except cutouts)
        - object histories
        - cone searches

- File storage
    - [Cloud Storage](https://cloud.google.com/storage)
    - download the complete, original alert packets in Avro format, including cutouts (science, template, difference)

- Message streams
    - [Pub/Sub](https://cloud.google.com/pubsub/docs/overview) messaging service
    - streams include:
        - ZTF stream: complete
        - ZTF stream: filtered for purity
        - ZTF stream: filtered for likely extragalactic transients
        - ZTF stream + Salt2 fits (for likely extragalactic transients)


All data and resources can be accessed via Google's [Cloud SDK](https://cloud.google.com/sdk) by way of the command-line, Python, and many other languages.
In addition, we are developing the `pgb_utils` Python package (see below) which provides convience functions for common tasks such as querying the database for lightcurves or cone searches, decoding, plotting, and processing the data.
The tutorial demonstrates access via the command-line (Cloud SDK) and Python (Cloud SDK, `pgb_utils`).
