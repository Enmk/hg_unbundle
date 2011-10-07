""" Unbundles the hg repository into new folder.
Uses the windows' cmd.exe to invoke chain of hg commands.

Author: Vasily Nemkov V.Nemkov@gmail.com
"""

import os.path
import subprocess

def extended(l : list, items):
    l.extend(items)
    return l

def unbundle(basePath, filename: str):
    """
    1. Create a directory path from a file name, replacing all '+' with '\'
    2. Create a directory in basePath with path created in step 1.
    3. run 'hg init' in directory created in step 2.
    4. run 'hg unbundle' in directory created in step 2.
    5. run 'hg update'
    """
    if not os.path.isfile(filename):
        raise RuntimeError("invalid file: " + filename)

    fullFilename = os.path.abspath(filename)
    #leave only file name without path and ext
    nameNoExt = os.path.splitext(os.path.split(filename)[1])[0]
    #make a proper path for unbundling and glue that to the base path
    dirname = os.path.join(*extended([basePath], nameNoExt.split('+')))   #1.
    #fullFilename = os.path.relpath(fullFilename, dirname)
    os.makedirs(dirname, exist_ok=False)                                  #2.
    command = """cmd.exe /c hg init && hg unbundle {} && hg update""".format(fullFilename)
    with subprocess.Popen(command.split(), cwd=dirname, shell=False):     #3 && 4 && 5
        pass


def main():
    """
    Process the script arguments to get:
        - List of hg bundle files;
        - Base directory for unbundling the files.
    Process the files one by one.
    """
    import os
    from argparse import ArgumentParser

    parser = ArgumentParser(epilog=__doc__)
    parser.add_argument("files", metavar='FILES', type=str, nargs='+',
                        help="list of files to process")
    parser.add_argument("-o", "--outputdir", dest="outdir", type=str,
                        help="base directory where hg bundle should be extracted")
    args = parser.parse_args()

    if args.outdir is None:
        args.outdir = os.getcwd()
    else:
        if not os.path.isdir(args.outdir):
            print("given base directory doesn't exist : ", args.outdir)

    for i, file in enumerate(args.files):
        print("{}\{} processing {}:".format(i+1, len(args.files), file))
        unbundle(args.outdir, file)


if __name__ == '__main__':
    main()

