#!/bin/bash
set +e
OUTJSON=/tmp/x.json
for K in s c b i p; do sudo ./deploy-project.sh -$K; done
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1/getlistings -d '{ "country_code" : "AU", "price": "$880.00" }'  1> ${OUTJSON}
sudo docker logs project-flask
cat ${OUTJSON} | python -m json.tool

