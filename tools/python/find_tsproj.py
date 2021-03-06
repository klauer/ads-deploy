# vi: sw=4 ts=4 sts=4 expandtab
import os
import pathlib
import re
import sys

project_re = re.compile(
    r"^Project.*?=\s*\"(.*?)\",\s*\"(.*?)\"\s*,\s*(.*?)\"\s*$",
    re.MULTILINE
    )

solution_fn, *ip_addresses = sys.argv[1:]
solution_path = pathlib.Path(solution_fn).parent

with open(solution_fn, 'rt') as f:
    solution_text = f.read()


projects = [match[1].replace('\\', '/')
            for match in project_re.findall(solution_text)
            if os.path.splitext(match[1])[1] not in ('.tcmproj', )
            ]

print('Found projects:\n    ', '\n    '.join(projects), file=sys.stderr)

ip_addresses = [
    ip_address
    for ip_address in ip_addresses
    if not ip_address.startswith('10.0.')      # ignore docket NAT
    and not ip_address.startswith('192.168.')  # ignore local address
    and not ip_address.startswith('169.254.')  # ignore local address
    and not ip_address.startswith('134.')      # ignore SLAC
]

with open(solution_path / "deploy_config.py", 'wt', newline='\r\n') as f:
    print(f'projects = {projects!r}', file=f)
    ip_error = None
    if not ip_addresses:
        print(f'local_net_id = "UNKNOWN"', file=f)
        ip_error = '\n'.join(
            ('Unable to find an IP address to match with the local net ID.',
             'This must be set for the IOC to work.')
        )
    else:
        for index, ip_address in enumerate(ip_addresses):
            comment = '' if index == 0 else '# '
            print(f'{comment}local_net_id = "{ip_address}.1.1"', file=f)

        if len(ip_addresses) > 1:
            ip_error = '\n'.join(
                ('Multiple IP addresses found. You may need to specify ',
                 'the correct local_net_id in deploy_config.py')
            )

    if ip_error:
        print()
        print('* NOTE *')
        print(ip_error)
        print('* NOTE *')
        print()
        print('# TODO: check local_net_id above; it should match Windows',
              file=f)
