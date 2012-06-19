#! /usr/bin/env python
#
# pypdf_merge_tool.py
#
# A very simple, minimalist Python command-line tool for merging PDF files.

# Licensed under the MIT License
# Copyright (C) 2012 Nicholas Kim
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import sys
import time
from pyPdf import utils, PdfFileReader, PdfFileWriter

def get_cmdline_arguments():
    """Retrieve command line arguments."""
    
    from optparse import OptionParser
    
    usage_string = "%prog [-o output_name] file1, file2 [, ...]"

    parser = OptionParser(usage_string)
    parser.add_option(
        "-o", "--output",
        dest="output_filename",
        default=time.strftime("output_%Y%m%d_%H%M%S"),
        help="specify output filename (exclude .pdf extension); default is current date/time stamp"
    )
    
    options, args = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    return options, args
    
def main():
    options, filenames = get_cmdline_arguments()
    output_pdf_name = options.output_filename + ".pdf"
    files_to_merge = []

    # get PDF files
    for f in filenames:
        try:
            next_pdf_file = PdfFileReader(open(f, "rb"))
        except(utils.PdfReadError):
            print >>sys.stderr, "%s is not a valid PDF file." % f
            sys.exit(1)
        except(IOError):
            print >>sys.stderr, "%s could not be found." % f
            sys.exit(1)
        else:
            files_to_merge.append(next_pdf_file)

    # merge page by page
    output_pdf_stream = PdfFileWriter()
    for f in files_to_merge:
        for i in range(f.numPages):
            output_pdf_stream.addPage(f.getPage(i))

    # create output pdf file
    try:
        output_pdf_file = open(output_pdf_name, "wb")
        output_pdf_stream.write(output_pdf_file)
    finally:
        output_pdf_file.close()

    print "%s successfully created." % output_pdf_name


if __name__ == "__main__":
    main()
