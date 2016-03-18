#elasticsearch-alias.py

alias maintenance - remove old indices from alias and add new indices to the same alias, according to string and date filtering

#USAGE: 

`python ./elasticsearch-aliases.py --prefix <indices prefix> --alias <alias name> --timestring <timestring> --range <range in days> [OPTIONS]`

#OPTIONS:

  -- help&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Show this message

  -- prefix&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; indices prefix to filter by (Required)

  -- alias&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; alias name to work on (Required)

  -- timestring&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; timestring format that should be part of the relevant indices name (Required)

  -- range&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; range in days to include new indices in the alias, and to exclude older indices from it (Required)

  -- host&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Elasticsearch cluster host ( default :  localhost)

  -- port&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Elasticsearch cluster port ( default : 9200)

#EXAMPLES:

  `python ./elasticsearch-aliases.py --host 10.0.0.1 --port 9200 --prefix articles --alias articles_last_month --timestring %Y%m%d --range 30'`

This uses http://10.0.0.1:9200 to connect to elasticsearch , searches for indices that their name begin with articles. If there name contains
    a creation date which is less than 30 days old they will be added to the alias, if the date is older than 30 days they will be removed from the alias
    if the current date is November 17th, 2015, index articles_20151116 will be added to the alias and index articles_20151016 will be removed from it

#REQUIREMENTS:

python
pip : `sudo yum install python-pip`

elasticsearch-py: `pip install elasticsearch`

curator : `pip install elasticsearch-curator`
