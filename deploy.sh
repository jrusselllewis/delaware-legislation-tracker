rm delaware_legislation_deploy.zip
# mkdir package
# pip install requests --target ./package/
# zip -r9 ./delaware_legislation_deploy.zip .
zip -g delaware_legislation_deploy.zip legislation_crawler.py
zip -g delaware_legislation_deploy.zip helpers.py
aws lambda update-function-code --function-name testLambdaS3 --zip-file fileb://delaware_legislation_deploy.zip
