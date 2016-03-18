import sys
import elasticsearch
import curator
from optparse import OptionParser


def main(argv):
    parser = OptionParser()
    parser.add_option("-p", "--prefix", dest="prefix", action="store", help="prefix to indices filter ")
    parser.add_option("-r", "--repository", dest="repository", action="store", help="repository name")

    (opts, args) = parser.parse_args()
    if not opts.repository:  # if repository is not given
        print 'repository not given'
        usage()
        sys.exit()
    if not opts.prefix:  # if repository is not given
        print 'prefix not given'
        usage()
        sys.exit()

    client = elasticsearch.Elasticsearch([
        {'host': 'localhost', 'port': 9200}
    ])

    indices_list = curator.get_indices(client)
    _filter = curator.build_filter(kindOf='prefix', value=opts.prefix)
    working_list = curator.apply_filter(indices_list, **_filter)


    res = curator.create_snapshot(client, indices=working_list, name=None, prefix='curator-',
                                  repository=opts.repository, ignore_unavailable=True, include_global_state=False,
                                  partial=False, wait_for_completion=True, request_timeout=21600,
                                  skip_repo_validation=False)

    print res


def usage():
    print 'usage : snapshot.py -p <prefix> -r <repository>'


if __name__ == "__main__":
    main(sys.argv[1:])
