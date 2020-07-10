mongodump --archive="prod.20200710.gz" --gzip --db=O24Mc-prod
mongorestore --gzip --archive="prod.20200710.gz" 
