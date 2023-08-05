import argparse


def args_parser():
    parser = argparse.ArgumentParser(description='Solving the DNS-01 challenge being executed by lego '
                                                 'https://go-acme.github.io/lego/dns/exec/')

    parser.add_argument('command', type=str,
                        help='Lego command, "present", "cleanup" or "timeout"')

    parser.add_argument('fqdn', type=str, nargs="?", default="example.com",
                        help='Record FQDN for DNS-01 challenge')

    parser.add_argument('data', type=str, nargs="?", default="token",
                        help='Record data (token) for DNS-01 challenge')

    parser.add_argument('--debug', default=False, action='store_true',
                        help='Shows detailed process')

    return parser.parse_args()
