#!/usr/bin/env bash

# test script of "/modify" API endpoint

# expected - {"action":false,"status":"ok","trigger":false}
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"modifyType": "remove", "implicature": "HighTemperature"}' \
  localhost:445/modify;
