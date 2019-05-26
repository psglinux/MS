#!/bin/sh

/usr/bin/memcached   --user=memcached   --listen=0.0.0.0   --port=11211   --memory-limit=64   --conn-limit=1024   --threads=4   --max-reqs-per-event=20   --verbose
