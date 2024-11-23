#!/usr/bin/env python

import argparse
import fitz


def dump_pdf_streams(pdf_file, output_file, base_xref, end_xref):
    """
    Extracts stream objects from a PDF file and writes them to an output file.

    Args:
        pdf_file (str): Path to the PDF file.
        output_file (str): Path to the output file where streams will be dumped.
        base_xref (int): Starting xref index.
        end_xref (int): Ending xref index.
    """
    try:
        with fitz.open(pdf_file) as pdf:
            if end_xref > pdf.xref_length():
                print(
                    f"End xref exceeds available objects ({pdf.xref_length()}). Adjusting."
                )
                end_xref = pdf.xref_length()

            chunks = []
            for xref in range(base_xref, end_xref):
                stream = pdf.xref_stream(xref)
                if stream:
                    chunks.append(stream)

            if not chunks:
                print(
                    f"No stream objects found in the range {base_xref} to {end_xref}."
                )
                return

            with open(output_file, "wb") as output:
                for chunk in chunks:
                    output.write(chunk)

            print(f"Successfully dumped {len(chunks)} streams to {output_file}.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pdf-stream-dumper.py")
    parser.add_argument("pdf_file", help="Path to the PDF file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output_streams.bin",
        help="Filename to dump stream content to (default: output_streams.bin).",
    )
    parser.add_argument(
        "-b",
        "--basexref",
        type=int,
        default=20,
        help="Base xref to start dumping from (default: 20).",
    )
    parser.add_argument(
        "-e",
        "--endxref",
        type=int,
        default=None,
        help="End xref to stop dumping (default: last xref in file).",
    )

    args = parser.parse_args()

    if args.endxref is None:
        with fitz.open(args.pdf_file) as pdf:
            args.endxref = pdf.xref_length()

    dump_pdf_streams(args.pdf_file, args.output, args.basexref, args.endxref)
