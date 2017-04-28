#!/bin/bash
tmp=$(elm-test --report json)
#echo $tmp
elm-test --report json > raw_results.txt
#echo '$tmp' > raw_result.txt
