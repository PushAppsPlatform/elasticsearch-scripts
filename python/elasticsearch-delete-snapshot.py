import sys
import elasticsearch
import curator
from optparse import OptionParser


def main(argv):
    parser = OptionParser()
    parser.add_option("-r", "--repository", dest="repository", action="store", help="repository name")
    parser.add_option("-t", "--timestring", dest="timestring", action="store",
                      help="timestring of the datestamp in an index name")
    parser.add_option("-o", "--older_than", dest="older_than", action="store", help="older than ( days )")
    parser.add_option("-i", "--ignore_if_newer_not_exist", dest="ignore_if_newer_not_exist", action="store",
                      help="don't perform deletion if there are no snapshots newer than this range")
    parser.add_option("-s", "--host", dest="host", action="store", help="host, default : localhost")
    parser.add_option("-p", "--port", dest="port", action="store", help="port, default : 9200")
    #parser.add_option("-m", "--timeout", dest="timeout", action="store", help="timeout (sec), default : 21600")
    
    host = 'localhost'
    port = 9200
    timeout = 21600
    (opts, args) = parser.parse_args()
    if not opts.repository:  # if repository is not given
        print 'repository not given'
        usage()
        sys.exit()
    if not opts.older_than:  # if repository is not given
        print 'older_then not given'
        usage()
        sys.exit()
    if not opts.timestring:  # if repository is not given
        print 'timestring not given'
        usage()
        sys.exit()
    if not opts.ignore_if_newer_not_exist:  # if repository is not given
        print 'ignore_if_newer_not_exist not given'
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
    snapshots_list = curator.get_snapshots(client, opts.repository)
    _filter = curator.build_filter(kindOf='newer_than', value=int(opts.ignore_if_newer_not_exist), time_unit='days',
                                   timestring=opts.timestring)
    snapshots_verification_list = curator.apply_filter(snapshots_list, **_filter)
    if not snapshots_verification_list:
        print 'no new snapshots available, existing'
        sys.exit()

    _filter = curator.build_filter(kindOf='older_than', value=int(opts.older_than), time_unit='days',
                                   timestring=opts.timestring)
    snapshots_to_delete_list = curator.apply_filter(snapshots_list, **_filter)
    print ', '.join(snapshots_to_delete_list)
    for snapshot in snapshots_to_delete_list:
        print 'deleting snapshot ' + snapshot + ' ...'
        res = curator.delete_snapshot(client,snapshot, opts.repository)
        if not res:
            print 'error! could not delete snapshot ' + snapshot


def usage():
    print 'usage : elasticsearch-delete-snapshot.py  -r <repository> -o <older_than> -i <ignore_if_newer_not_exist> -t <timestring> '


if __name__ == "__main__":
    main(sys.argv[1:])
