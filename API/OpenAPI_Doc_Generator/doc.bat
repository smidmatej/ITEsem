@echo off
java -jar lib/swagger-codegen-cli-3.0.7.jar generate -i envi-server-swagger.yaml -l html2 -o doc/

