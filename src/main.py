import argparse
import os
import shutil
from contextlib import contextmanager, redirect_stdout

import archive
import config
from driver_claw import DriverClaw


@contextmanager
def setup_print(silent: bool):
    if silent:
        with open(os.devnull, 'w') as f, redirect_stdout(f):
            yield
    else:
        yield


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find and download the latest common hardware drivers, and diagnostic tool.')
    parser.add_argument(
        '-o',
        '--output-dir',
        type=str,
        default='drivers',
        help='Output directory for downloaded drivers (default: drivers)'
    )
    parser.add_argument(
        '-e',
        '--error-handling',
        choices=['exit', 'ignore', 'log'],
        default='log',
        help='How to handle download errors: exit (stop on error), ignore (continue), log (log failures and continue)'
    )
    parser.add_argument(
        '-r',
        '--retry-failed',
        action='store_true',
        help='Retry only the failed downloads from the previous run'
    )
    parser.add_argument(
        '-n',
        '--archive-name',
        type=str,
        default='driver-pack.zip',
        help='Name of the output archive file (default: driver-pack.zip)'
    )
    parser.add_argument(
        '-l',
        '--compress-level',
        type=int,
        default=5,
        choices=range(0, 10),
        help='Compression level for the archive (0-9, default: 5)'
    )
    parser.add_argument(
        '-f',
        '--include-files',
        type=str,
        nargs='+',
        action='extend',
        help='File or directory name to include in the archive'
    )
    parser.add_argument(
        '-s',
        '--silent',
        action='store_true',
        help='Suppress all output messages'
    )

    group_archive = parser.add_mutually_exclusive_group()
    group_archive.add_argument(
        '-a',
        '--archive-only',
        action='store_true',
        help='Only create archive from existing output directory, skip scraping'
    )
    group_archive.add_argument(
        '-x',
        '--no-archive',
        action='store_true',
        help='Do not create a zip archive of the downloaded files'
    )

    args = parser.parse_args()

    with setup_print(args.silent):
        if not args.archive_only:
            if not args.retry_failed and os.path.exists(args.output_dir):
                shutil.rmtree(args.output_dir)

            try:
                claw = DriverClaw(args.output_dir)
                failed = claw.start(claw.load_failed() if args.retry_failed else config.BASE_CONFIG,
                                    args.error_handling)
            except FileNotFoundError:
                print('Nothing to retry.')
                exit(1)

            if len(failed) > 0:
                print(f'Total of {len(failed)} download(s) failed.')
                print('You may use -r/--retry-failed option to try again.')
                exit(1)
            if args.no_archive:
                exit(0)

        if not os.path.exists(args.output_dir):
            print(
                f"Error: Output directory '{args.output_dir}' does not exist.")
            exit(1)
        if not os.listdir(args.output_dir):
            print(f"Error: Output directory '{args.output_dir}' is empty.")
            exit(1)

        archive.zip(args.archive_name,
                    *(args.include_files or []),
                    args.output_dir,
                    level=args.compress_level,
                    silent=args.silent)
