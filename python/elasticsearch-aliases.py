import sys
import elasticsearch
import curator
from optparse import OptionParser

# exmample: print 'usage : python ./elasticsearch-aliases.py --prefix articles --alias articles_last_month --timestring %Y%m%d --range 30'
def main(argv):
    parser = OptionParser()
    parser.add_option("--timestring", dest="timestring", action="store",
                      help="timestring of the datestamp in an index name")
    parser.add_option("--range", dest="range", action="store", help="the time range of the alias ( days )")
    parser.add_option("--prefix", dest="prefix", action="store", help="prefix to filter indices")
    parser.add_option("--host", dest="host", action="store", help="host, default : localhost")
    parser.add_option("--port", dest="port", action="store", help="port, default : 9200")
    parser.add_option("--alias", dest="alias", action="store", help="alias name")

    host = 'localhost'
    port = 9200
    timeout = 21600
    (opts, args) = parser.parse_args()
    if not opts.range:  # if repository is not given
        print 'range not given'
        usage()
        sys.exit()
    if not opts.timestring:  # if repository is not given
        print 'timestring not given'
        usage()
        sys.exit()
    if not opts.alias:  # if repository is not given
        print 'alias not given'
        usage()
        sys.exit()
    if not opts.prefix:  # if repository is not given
        print 'prefix not given'
        usage()
        sys.exit()
    if  opts.host:  # if host is  given
        host = opts.host
    if  opts.port:  # if port is  given
        host = int(opts.port)
    #if  opts.timeout:  # if port is  given
    #    host = int(opts.timeout)

    client = elasticsearch.Elasticsearch([
        {'host': host, 'port': port, 'timeout' : timeout}
    ])

    # first add the new indices to the alias
    indices = curator.get_indices(client)
    _filter = curator.build_filter(kindOf='prefix', value=opts.prefix)
    prefix_indices = curator.apply_filter(indices, **_filter)
    _filter = curator.build_filter(kindOf='newer_than', value=int(opts.range)-1, time_unit='days',
    timestring=opts.timestring)
    new_prefix_indices = curator.apply_filter(prefix_indices, **_filter)
    for index in new_prefix_indices:
        print 'adding index ' + index  + ' to alias ' + opts.alias
        curator.add_to_alias(client, index, opts.alias)

    alias_list = curator.get_alias(client, opts.alias)
    #if not alias_list:
    #    sys.exit()
    # remove old indices from alias
    _filter = curator.build_filter(kindOf='older_than', value=int(opts.range), time_unit='days',
    timestring=opts.timestring)
    old_indices = curator.apply_filter(alias_list, **_filter)
    for index in old_indices:
        print 'removing index ' + index + ' from alias ' + opts.alias + ' ...'
        curator.remove_from_alias(client, index, opts.alias)




def usage():
    print 'usage : python ./elasticsearch-aliases.py --host <host> --port <port> --prefix <indices prefix> --alias <alias name> --timestring <timestring> --range <range in days>'



if __name__ == "__main__":
    main(sys.argv[1:])
