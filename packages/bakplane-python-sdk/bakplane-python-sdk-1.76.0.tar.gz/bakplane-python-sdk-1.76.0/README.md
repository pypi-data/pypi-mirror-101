# Bakplane Client for Python
Bakplane is the orchestration backbone for Dominus, FinFlo, and Fabrik.

This SDK can be used to control ingestion sessions, mastering executions, plugin installation, etc. 


## Installation

Installing the bakplane python client takes just a few seconds:

```bash
pip install bakplane-python-sdk
```


## Spark

If you'd like to use Bakplane inside of Spark running in Docker:

```bash
docker run -it --rm -p 8888:8888 --name pyspark jupyter/pyspark-notebook
```

Inside of your notebook run:
```shell script
!pip install bakplane-python-sdk
```

>> Note: use `host.docker.internal` instead of `localhost` when testing.



## Documentation
If you're interested in learning more then read the documentation: https://docs.openaristos.io/

<h1 align="center">
    <img src="https://gist.githubusercontent.com/daefresh/32418b316dda99eb537fcef08b4c88af/raw/f4ed8e6fb4fd343eb61541c76871233d1105d2ec/bakplane_logo.svg" alt="Bakplane"/>
</h1>

Copyright (C) 2021 Aristos Data, LLC