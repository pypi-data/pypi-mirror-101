Fiddler Client
=============

Python client for interacting with Fiddler. Provides a user-friendly interface to our REST API and enables event
publishing for use with our monitoring features.

Requirements
------------
Requires Python >= Python-3.6.3.

Installation
------------

    $ pip3 install fiddler-client

API Example Usage
-------------
Documentation for the API can be found [here](https://docs.fiddler.ai/api-reference/python-package/). For examples of interacting with our APIs, please check out our [Quick Start Guide](https://docs.fiddler.ai/quick-start/) as well as the work notebooks found on our [Samples Github](https://github.com/fiddler-labs/fiddler-samples).


Version History
-------------
### 0.7.0
   - ##### **Dataset Refactor**
       -  Datasets refactored to be members of a Project
           - *This is a change promoting Datasets to be first class within Fiddler. It will affects both the UI and several API in Fiddler*
       - Many API utilizing Projects will now require `project_id` passed as a parameter
   - ##### **New Features**
       - Added `fdl.update_model()` to client
           - *update the specified model, with model binary and package.py from
              the specified model_dir*
       - Added `fdl.get_model()` to client
           - *download the model binary, package.py and model.yaml to the given
              output dir.*
       - Added `fdl.publish_events_batch()` to client
           - *Publishes a batch events object to Fiddler Service.*
           - *Note: Support for other batch methods including `fdl.publish_events_log()`
              and `fdl.publish_parquet_s3()` will be deprecated in the near future
              in favor of `fdl.publish_events_batch()`*
   - #### **Changes**
       - Simplified logic within `fld.upload-dataset()`
       - Added client/server handshake for checking version compatibilities
           - *Warning issued in case of mismatch*
       - Deleted redundant APIs
           - `fdl.create_surrogate_model()`
           - `fdl.upload_model_sklearn()`
       - Restructured APIs to be more duck typing-friendly (relaxing data type restrictions)
       - Patches for minor bug-fixes


### 0.6.18
   - ##### **Features**
       - Minor updates to ease use of binary classification labels

### 0.6.17
   - ##### **Features**
       - Added new arguments to `ModelInfo.from_dataset_info()`
           - `preferred_explanation_method` to express a preferred default explanation algorithm for a model
           - `custom_explanation_names` to support user-provided explanation algorithms which the user will implement on their model object via package.py.

### 0.6.16
   - ##### **Features**
       - Minor improvements to `publish_events_log()` to circumvent datatype conversion issues

### 0.6.15
   - ##### **Features**
       - Added strict name checks

### 0.6.14
   - ##### **Features**
       - Added client-native multithreading support for `publish_events_log()`
       using new parameters `num_threads` and `batch_size`

### 0.6.13
   - ##### **Features**
       - Added `fdl.generate_sample_events()` to client
         -  *API for generating monitoring traffic to test out Fiddler*
       - Added `fdl.trigger_pre_computation()` to client
         -  *Triggers various precomputation steps within the Fiddler service based on input parameters.*
       -  Optionally add proxies to FiddlerApi() init

### 0.6.12
   - ##### **Features**
       - Added `fdl.publish_parquet_s3()` to client
         -  *Publishes parquet events file from S3 to Fiddler instance.
            Experimental and may be expanded in the future.*

### 0.6.10
   - ##### **Features**
       - Added `fdl.register_model()` to client
           -  *Register a model in fiddler. This will generate a surrogate model,
               which can be replaced later with original model.*
