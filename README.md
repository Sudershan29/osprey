# Data Streaming as a Service (DSaaS)

A prototype for the extraction, storage, validation and distribution of public epidemiological data for analysis.

## Installation

1. git clone https://github.com/NSF-RESUME/DSaaS.git osprey 

   Ensure to clone into `osprey` folder

### Running

All the server components are made available within a series of dockerfiles provided in Dockerfile.
To install the components, the following steps can be followed:

```
# Build and create necessary volumes

source scripts/prepare_start.sh

    This step involves creating database for the first time, and setting up authentications for globus

# Runs the entire service in background 

docker compose up -d

```

### Debugging

docker compose exec <service-name> bash

Eg. docker compose exec web flask shell

### Using the client.

Update the URL of the server in `osprey/client/client.py` and access the client API as per example in `osprey/examples/app.py`.

