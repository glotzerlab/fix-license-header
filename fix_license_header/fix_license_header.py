# Copyright (c) 2021-2024 The Regents of the University of Michigan
# Part of fix-license-header, released under the BSD 3-Clause License.

"""Add license header to files.

This script operates on text files and replaces the initial comment block with a
license header. It is designed to be used with pre-commit.

The header is constructed from the first N lines from ``license-file`` (when
provided) and the given additional header lines. The comment prefix is added to
the start of each header line. with the given comment prefix.

For each file given in the arguments, it checks if the first commented lines in
the file match the header. When they fail to match, the script rewrites the
initial comments in the file with the given header.
"""

import argparse
import sys


def fix_file(f, header_lines, prefix, keep_before, keep_after):
    """Fix one file.

    Return 0 if the file is not modified, 1 if it is.
    """
    line = f.readline()
    if line.endswith(b'\r\n'):
        line_ending = b'\r\n'
    else:
        line_ending = b'\n'

    before = b''
    after = b''
    file_header = []
    while (line.startswith(prefix)
           or any([line.startswith(s) for s in keep_before])):
        if any([line.startswith(s) for s in keep_before]):
            before += line
        elif any([line.startswith(s) for s in keep_after]):
            after += line
        else:
            file_header.append(line[len(prefix):].strip())
        line = f.readline()

    # read the contents of the file
    file_contents = line + f.read()

    # check if the header is correct
    if file_header == header_lines \
            and (file_contents == b'' or file_contents.startswith(line_ending)):
        return 0

    # header doesn't match, rewrite file
    f.seek(0)
    f.truncate()
    f.write(before)
    for line in header_lines:
        f.write(prefix + line + line_ending)
    if len(after) > 0:
        f.write(line_ending)
        f.write(after)
    if len(file_contents) > 0 and not file_contents.startswith(line_ending):
        f.write(line_ending)
    f.write(file_contents)

    return 1


def main(argv=None):
    """The main entrypoint."""
    parser = argparse.ArgumentParser('Fixes the license headers in files.',)
    parser.add_argument('--license-file', help='License file to read', type=str)
    parser.add_argument('--start',
                        help='Number of lines to ignore (default: 0)',
                        type=int,
                        default=0)
    parser.add_argument('--num',
                        help='Number of lines to read (default: 1)',
                        type=int,
                        default=1)
    parser.add_argument('--add',
                        action='append',
                        help='Line to add after the license file '
                        '[can specify multiple times]',
                        type=str)
    parser.add_argument('--keep-before',
                        action='append',
                        help='Keep lines starting with this before the header '
                        '[can specify multiple times]',
                        type=str)
    parser.add_argument('--keep-after',
                        action='append',
                        help='Keep lines that start with this after the header '
                        '[can specify multiple times]',
                        type=str)
    parser.add_argument('--comment-prefix',
                        help='Comment prefix',
                        type=str,
                        default='#')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    # build the header
    header_lines = []
    if args.license_file is not None:
        with open(args.license_file, 'rb') as license_file:
            for _ in range(args.start):
                license_file.readline()
            for _ in range(args.num):
                header_lines.append(license_file.readline().strip())

    if args.add is not None:
        for line in args.add:
            header_lines.append(line.encode('utf-8'))

    keep_before = []
    if args.keep_before is not None:
        keep_before = [s.encode('utf-8') for s in args.keep_before]

    keep_after = []
    if args.keep_after is not None:
        keep_after = [s.encode('utf-8') for s in args.keep_after]

    return_value = 0

    for filename in args.filenames:
        with open(filename, 'r+b') as f:
            status = fix_file(f=f,
                              header_lines=header_lines,
                              prefix=args.comment_prefix.encode('utf-8') + b' ',
                              keep_before=keep_before,
                              keep_after=keep_after)
            return_value |= status
            if status:
                print(f'Updated license header in {filename}')

    sys.exit(return_value)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
