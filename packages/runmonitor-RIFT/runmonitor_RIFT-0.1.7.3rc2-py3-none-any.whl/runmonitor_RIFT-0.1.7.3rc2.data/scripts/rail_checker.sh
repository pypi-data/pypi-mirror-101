#!/usr/bin/env bash

RESULT=$(python -c 'import rail_checker; out = rail_checker.modify_prior(); print(out)')

index=0

IFS=',' read -ra ADDR <<< "$RESULT"
for i in "${ADDR[@]}"; do
  echo $i #iterates through the first and second bounds. We'd need to use the sed command, but on the modified arguments. 
done
