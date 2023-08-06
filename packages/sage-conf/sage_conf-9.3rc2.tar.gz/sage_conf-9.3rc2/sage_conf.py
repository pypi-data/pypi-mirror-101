VERSION = "unknown"

try:
    from sage_root.sage_conf import *
except ImportError:
    raise ValueError('''sage_conf is not installed completely.  Use one of the following:

- python3 -m pip install 'sage_conf[var_tmp]'   # installs Sage distribution as a prebuilt wheel
                                                # and sets a relocation symlink in /var/tmp/

- python3 -m pip install 'sage_conf[opt_sage]'  # installs Sage distribution as a a prebuilt wheel
                                                # and sets a relocation symlink in /opt/sage/
                                                # (needs write access to /opt/sage/)

- python3 -m pip install 'sage_conf[dot_sage]'  # builds the Sage distribution from source
                                                # in a subdirectory of ~/.sage''')

# Entry point 'sage-config'.  It does not depend on any packages.

def _main():
    from argparse import ArgumentParser
    from sys import exit, stdout
    parser = ArgumentParser()
    parser.add_argument('--version', help="show version", action="version",
                       version='%(prog)s ' + VERSION)
    parser.add_argument("VARIABLE", nargs='?', help="output the value of VARIABLE")
    args = parser.parse_args()
    d = globals()
    if args.VARIABLE:
        stdout.write('{}\n'.format(d[args.VARIABLE]))
    else:
        for k, v in d.items():
            if not k.startswith('_'):
                stdout.write('{}={}\n'.format(k, v))

if __name__ == "__main__":
    _main()
