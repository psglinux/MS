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
HOSTIP=127.0.0.1


DEBUG=0
if [ "x$ENDEBUG" != "x" ]; then
	DEBUG=1
fi

print_logs() {
	if [ $DEBUG -eq 1 ]; then
		sudo docker logs project-flask
	fi
}

debug_print() {
	if [ $DEBUG -eq 1 ]; then
		print_logs
		cat ${1}
	fi
}

debug_json() {
	if [ $DEBUG -eq 1 ]; then
		print_logs
		cat ${1} | python -m json.tool
	fi
}


# LOGIN and get token.
# XXX TODO  How to get this token from this login page via CURL
# and pass onto the next set of APIs ?
#TOKEN=$(curl -s -X POST -F 'username=clala@ab.com' -F 'password=ohboy'  http://${HOSTIP}/login | jq -r '.id_token')
#echo $TOKEN

set -e
# Should return a listing using FORM data
curl -X POST -F "country_code=AU" -F "zipcode=3810" -F "weekly_price=\$980.00" http://$HOSTIP/getlistings 1> ${OUTJSON} 2>/dev/null
debug_json ${OUTJSON}

# Should return a listing using JSON
PARS='{ "accommodates" : 2, "country_code" : "AU", "zipcode" : "3810" }'
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://$HOSTIP/getlistings -d "${PARS}"  2>/dev/null 1> ${OUTJSON}
debug_json ${OUTJSON}

# Should return a 404
PARS='{ "country_code" : "AU" }'
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://$HOSTIP/getlistings -d "${PARS}" 2>/dev/null 1> ${OUTJSON}
print_logs
grep 404 ${OUTJSON} >/dev/null 2>&1

