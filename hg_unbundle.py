
#from match_files_in_dir import match_files_in_dir, match_re, match_re

import os.path
import subprocess

def extended(l : list, items):
    l.extend(items)
    return l

"""
1. Create a directory path from a file name, replacing all '+' with '\'
2. Create a directory in basePath with path created in step 1.
3. run hg init in directory created in step 2.
4. do a 'hg unbundle' in directory created in step 2.
5. do a 'hg update'
?6. if a directory is empty after doing this, report to a user.
"""
def unbundle(basePath, filename: str):
    if not os.path.isfile(filename):
        raise RuntimeError("invalid file: " + filename)

    fullFilename = os.path.abspath(filename)
    #leave only file name without path and ext
    nameNoExt = os.path.splitext(os.path.split(filename)[1])[0]

    pathComponents = extended([basePath], nameNoExt.split('+'))
    dirname = os.path.join(*pathComponents) #1.
    #fullFilename = os.path.relpath(fullFilename, dirname)
    os.makedirs(dirname, exist_ok=False)                                  #2.
    command = """cmd.exe /c hg init && hg unbundle {} && hg update""".format(fullFilename)
    with subprocess.Popen(command.split(), cwd=dirname, shell=True):      #3 && 4 && 5
        pass
        #print("doing a \"{}\"".format(command))


""" Get a list of files to process, or find automatically.
Get the directory where the files should be unbundled or use current.
Process the file one by one
"""
def main():
    import os
    from argparse import ArgumentParser

    parser = ArgumentParser("Script to unbundle the mercurial files into the give directory")
    parser.add_argument("files", metavar='FILES', type=str, nargs='+', help="list of files to process")
    parser.add_argument("-o", "--outputdir", dest="outdir", type=str, help="base directory where hg bundle would be extracted, if none specified, current one is used")
    args = parser.parse_args()

    if args.outdir is None:
        args.outdir = os.getcwd()
    else:
        if not os.path.isdir(args.outdir):
            print("given output directory doesn't exist : ", args.outdir)

    for i, file in enumerate(args.files):
        print("{}\{} processing file {}".format(i+1, len(args.files), file))
        unbundle(args.outdir, file)


if __name__ == '__main__':
    main()

