#! /usr/bin/env sh
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 chem_kit_api.main:app 
