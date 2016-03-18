reindex.sh

reindex data from one elasticsearch index to another

#USAGE: 

`reindex.sh -prefix <indices_prefix> -source <source_host> -target <target_host>`

#OPTIONS:
  - help          Show this message


#EXAMPLES:

`reindex.sh -prefix article -source http://localhost:9200 -target http://domain.com:9200`

this reindex data from all indices that start with the prefix article in http://localhost:9200 into http://domain.com:9200. only data is being reindexed.

#requirements:

[elasticsearch-dump](https://github.com/taskrabbit/elasticsearch-dump) : `npm install elasticdump`

