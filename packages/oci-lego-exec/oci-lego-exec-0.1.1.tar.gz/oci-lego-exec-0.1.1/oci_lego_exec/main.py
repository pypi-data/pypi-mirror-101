import logging
from json import dumps
from oci_lego_exec.arguments import args_parser
from oci_lego_exec.oci_dns import OciDns

LOG = logging.getLogger(name=__name__)
PROPAGATION_TIMEOUT = 60
CHECK_INTERVAL = 15
TTL = 60


def main():
    args = args_parser()
    if args.debug:
        level = getattr(logging, 'DEBUG', None)
    else:
        level = getattr(logging, 'INFO', None)

    logging.basicConfig(level=level)

    exit_code = 1
    try:
        if args.command == 'timeout':
            print(dumps({"timeout": PROPAGATION_TIMEOUT, "interval": CHECK_INTERVAL}))
            exit_code = 0
            return exit_code

        dns = OciDns()
        if args.command == 'present':
            dns.add_txt_record(args.fqdn, args.data, TTL)
        elif args.command == 'cleanup':
            dns.del_txt_record(args.fqdn)
        else:
            raise NotImplementedError("Command {} not implemented".format(args.command))

        exit_code = 0
    except Exception as e:
        print("Something went wrong: {}. Try to --debug it".format(e))

    return exit_code


if __name__ == '__main__':
    exit(main())
