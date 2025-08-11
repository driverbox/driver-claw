import argparse
import os
import shutil

import archive
import config
from driver_scraper import DriverScraper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download and package drivers and tools.')
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
        '-x',
        '--no-archive',
        action='store_true',
        help='Do not create a zip archive of the downloaded files'
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
    args = parser.parse_args()

    if not args.retry_failed and os.path.exists(args.output_dir):
        shutil.rmtree(args.output_dir)

    try:
        scraper = DriverScraper(args.output_dir)
        failed = scraper.scrape(scraper.load_failed() if args.retry_failed else config.BASE_CONFIG,
                                args.error_handling)
    except FileNotFoundError:
        print('Nothing to retry.')
        exit(1)

    if len(failed) > 0:
        print(f'Total of {len(failed)} download(s) failed.')
        print('You may use -r/--retry-failed option to try again.')

    if len(failed) == 0 and not args.no_archive:
        archive.zip(args.archive_name,
                    *(args.include_files or []),
                    args.output_dir,
                    level=args.compress_level)
