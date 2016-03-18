**elasticsearch-delete-snapshot.py**

Deletes Elasticsearch snapshots by timerange using the curator Python API

#USAGE:

`elasticsearch-delete-snapshot.py  -r <repository> -o <older_than> -i <ignore_if_newer_not_exist> -t <timestring>`

This will delete any snapshot that is older than than older_than days. 
However, The script will not delete any snapshot if there are no snapshot availabe that are newer than ignore_if_newer_not_exist parameter to maintain a certain level of data retention.

#EXAMPLES:

  `python elasticsearch-delete-snapshot.sh  -r my_backup -o 30 -i 10 -t %Y%m%d`

Delete al snapshots in my_backup repository that are older than 30 days as long as we have snapshots from the last 10 days. Time filtering is done by the time string that should exist in the snapshot name.

#REQUIREMENTS:

python

pip : `sudo yum install python-pip`

elasticsearch-py: `pip install elasticsearch`

curator : `pip install elasticsearch-curator`

[the aws cloud plugin](https://github.com/elastic/elasticsearch-cloud-aws)

create an S3 repository:
```
PUT _snapshot/testing
{
  "type": "s3",
  "settings": {
    "bucket": "bucket_name" ,
    "base_path" : "backups/es",
    "endpoint" : "s3.amazonaws.com"
  }
}
```




