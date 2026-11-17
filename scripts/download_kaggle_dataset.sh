#!/usr/bin/env sh
set -eu

mkdir -p data/raw
curl -L --fail --silent --show-error   'https://www.kaggle.com/api/v1/datasets/download/tunguz/online-retail'   -o data/raw/online-retail.zip
unzip -o data/raw/online-retail.zip -d data/raw
test -f data/raw/Online_Retail.csv
echo 'Dataset ready: data/raw/Online_Retail.csv'
