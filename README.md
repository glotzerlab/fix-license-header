# fix-license-header

A hook for running adding license headers to files using [pre-commit].
This script operates on text files and replaces the initial comment block with a
license header.

The header is constructed from the first N lines from ``license-file`` (when
provided) and the given additional header lines. The comment prefix is added to
the start of each header line. with the given comment prefix.

For each file given in the arguments, it checks if the first commented lines in
the file match the header. When they fail to match, the script rewrites the
initial comments in the file with the given header. Specify keep options to
avoid overwriting matching lines before or after the header.

[pre-commit]: https://pre-commit.com/

## Installation

Add the following to `.pre-commit-config.yaml` to use this hook on Python
files:

```yaml
- repo: https://github.com/glotzerlab/fix-license-header
  rev: v0.1.0
  hooks:
  - id: fix-license-header
    types_or: [python]
    args:
    - --license-file=LICENSE
    - --keep-before=#!
```

## Arguments

Specify the license header to write:

* `--license-file` (optional) Set the license file to read.
* `--start` (default: 0) Start reading the license file at this line.
* `--num` (default: 1) Number of lines to read from the file.
* `--add` Additional line to add after those from the file. Specify this
  multiple times for more than one line.

Specify lines to keep:

* `--keep-before` Keep lines starting with this before the header. You can
  specify this option multiple times.
* `--keep-after` Keep lines starting with this after the header. You can
  specify this option multiple times.

Set the comment prefix:

* `--comment-prefix` (default: #) Set the single line comment prefix.
