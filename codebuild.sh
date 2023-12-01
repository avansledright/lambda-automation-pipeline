#!/bin/bash
mv $CODEBUILD_SRC_DIR/lambda_tests.json .
mv $CODEBUILD_SRC_DIR/lambda_tests.zip .
unzip lambda_tests.zip
echo "AUTOMATED LAMBDA TESTING PIPELINE"

lambda_functions=$(jq .Lambdas[] lambda_tests.json)
length=$(jq '.Lambdas | length' lambda_tests.json)

echo "TOTAL LAMBDAS = $length"


lambda_info=$(jq .Lambdas lambda_tests.json)
str_lambda=$(echo $lambda_info | jq -r tostring)
python3 main.py $str_lambda

echo "FINISHED TESTING"