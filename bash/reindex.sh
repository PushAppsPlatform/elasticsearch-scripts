#!/bin/bash
# parsing the command line arguments and passing
# them to the correct script variables
while [[ $# > 1 ]]
    do
    key="$1"

    case $key in
        -prefix)
        PREFIX="$2"
        shift # past argument
        ;;
        -source)
        SOURCE="$2"
        shift # past argument
        ;;
        -target)
        TARGET="$2"
        shift # past argument
        ;;
        -help)
        help
        exit -1
        ;;
        *)
           # unknown option
        ;;
    esac
    shift # past argument or value
done

# exit on error
set -e

help() {
  printf "Usage: reindex.sh -prefix article -source http://localhost:9200 -target http://domain.com:9200\n"
}

# run every command in this script, using this method
# in order to avoid continuation after an error
safeRunCommand() {
    typeset cmnd="$*"
    typeset ret_code

    echo ${LOGGER_PREFIX} cmnd=${cmnd}
    eval ${cmnd}
    ret_code=$?
    if [ ${ret_code} != 0 ]; then
      printf "Error : [%d] when executing command: '$cmnd'. Exit now\n" ${ret_code}
      return ${ret_code}
    fi
}

# check required vars for deployment
checkInputArguments() {
    if [ ! "$PREFIX" ]; then
        printf "Error : Please specify the prefix using -prefix\n"
        help
        return 999
    fi

    if [ ! "$SOURCE" ]; then
        printf "Error : Please specify the source host using -source\n"
        help
        return 999
    fi

    if [ ! "$TARGET" ]; then
        printf "Error : Please specify the target host using -target\n"
        help
        return 999
    fi
}

main() {
  set +e
  #echo curl -XGET $SOURCE/_cat/indices/$PREFIX?pretty=true | cut -d $' ' -f3
  list="$(curl -XGET $SOURCE/_cat/indices/$PREFIX?pretty=true -v | cut -d $' ' -f3)"
  #list="$(curl -XGET http://52.5.223.179:9200)"
  for item in $list
  do
    echo "migrating" $item "..."
    #"$(/usr/local/bin/elasticdump --input=$SOURCE/$item --output=$item.json --type=data)"
    "$(/usr/local/bin/elasticdump --bulk=true --output=$TARGET/$item --input=$SOURCE/$item)"
    #rm -f $item.json
  done
}


# 0.
safeRunCommand "checkInputArguments"

#1.
#safeRunCommand "main"
main

