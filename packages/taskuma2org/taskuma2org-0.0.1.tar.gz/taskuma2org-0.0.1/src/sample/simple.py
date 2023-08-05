import os
import click
import tempfile


MEMACS_ARGUMENT = 'memacs_csv \
--timestamp-field "start" \
--fieldnames "task, est, taskumaduration, start, end, rate, \
taskumaproj, section, map, memo, check, taskumatag, dummy" \
--delimiter "," \
--timestamp-format "%Y/%m/%d %H:%M" \
--output-format "{task}" \
--properties "taskumaduration,taskumaproj,section,memo,taskumatag" \
'


def return_input_file_name(infile, skip):
    if skip:
        return skip_first_two_lines(infile)
    else:
        return infile


def make_memacs_argument(infile, outfile=None):
    if outfile:
        return_value = MEMACS_ARGUMENT + " -f " + infile + " -o " + outfile
    else:
        return_value = MEMACS_ARGUMENT + " -f " + infile

    return return_value


def skip_first_two_lines(infile):
    """return file name which is made from infile with removing first two lines"""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as tfp:
        fp = open(infile, "r+", encoding="utf-8")
        i = 0
        for a_line in fp:
            if i < 2:
                i = i + 1
            else:
                tfp.write(a_line)
        fp.close()
        return tfp.name


@click.command()
@click.argument("filename", type=click.STRING, required=True)
@click.option(
    "--output",
    type=click.Path(exists=True, writable=True, resolve_path=True),
)
@click.option(
    "--skip/--no-skip",
    default=False,
    help="whether or not to skip the first two lines of the csv file.",
)
def wrapper(filename, output, skip):
    """convert taskuma log file to org-mode.
    taskuma log as csv file
    """
    inputfile = return_input_file_name(filename, skip)
    spec_arg = make_memacs_argument(inputfile, output)
    exit_status = os.system(spec_arg)
    if inputfile != filename:
        os.remove(inputfile)
    exit(exit_status)
