#!/usr/bin/env bash

# test script of "/type" API endpoint

# expected - {"action":false,"status":"ok","trigger":false}
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"implicature": "HighTemperature", "intent": "modify.enter"}' \
  localhost:445/type;

# expected - {"action":false,"status":"ok","trigger":true}
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"implicature": "HighSecurity", "intent": "modify.sleep"}' \
  localhost:445/type;