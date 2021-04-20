#!/usr/bin/env bash

# test script of "/param" API endpoint

# expected:
#   {
#       "status":"ok",
#       "action":{"hasParameter":false},
#       "trigger":{"hasParameter":true,"parameterEnv":"humidity","parameterValue":{"humidity":63}}
#   }
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"implicature": "HighTemperature"}' \
  localhost:445/param;

# expected:
#   {
#       "status":"ok",
#       "action":{"hasParameter":true,"parameterEnv":"temperature","parameterValue":{"temperature":23}},
#       "trigger":{"hasParameter":true,"parameterEnv":"brightness","parameterValue":{"brightness":24}}
#   }
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"implicature": "HighTemperature", "skipCount": 2}' \
  localhost:445/param;
