#!/bin/bash
set +e
# If rebuild is needed, pass "rebuild" as the first param to the script
if [ "x$1" == "xrebuild" ]; then
	for K in s c b i p; do sudo ./deploy-project.sh -$K; done
fi

OUTJSON=/tmp/x.json
if [ -r ${OUTJSON} ]; then
	rm -f ${OUTJSON}
fi
set -e

# Should return a listing
PARS='{ "country_code" : "AU", "zipcode" : "3810" }'
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1/getlistings -d "${PARS}"  1> ${OUTJSON}
sudo docker logs project-flask
cat ${OUTJSON} | python -m json.tool

# Should return a 404
PARS='{ "country_code" : "AU" }'
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1/getlistings -d "${PARS}"  1> ${OUTJSON}
sudo docker logs project-flask
grep 404 ${OUTJSON} >/dev/null 2>&1

