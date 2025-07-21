import argparse
import os
import shutil
import sys
from pathlib import Path

import archive
import config
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download and package drivers and tools.")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="drivers",
        help="Output directory for downloaded drivers (default: drivers)"
    )
    parser.add_argument(
        "-e",
        "--error-handling",
        choices=["exit", "ignore", "log"],
        default="log",
        help="How to handle download errors: exit (stop on error), ignore (continue), log (log failures and continue)"
    )
    parser.add_argument(
        "-r",
        "--retry-failed",
        action="store_true",
        help="Retry only the failed downloads from the previous run"
    )
    parser.add_argument(
        "-x",
        "--no-archive",
        action="store_true",
        help="Do not create a zip archive of the downloaded files"
    )
    parser.add_argument(
        "-n",
        "--archive-name",
        type=str,
        default="driver-pack.zip",
        help="Name of the output archive file (default: driver-pack.zip)"
    )
    parser.add_argument(
        "-l",
        "--compress-level",
        type=int,
        default=5,
        choices=range(0, 10),
        help="Compression level for the archive (0-9, default: 5)"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    log_file = output_dir.joinpath("failed_downloads")
    failed_downloads: dict[str, list] = {}

    if args.retry_failed:
        download_configs = utils.load_failed_downloads(log_file)
        if not download_configs:
            print("No failed downloads to retry.")
            sys.exit(1)
    else:
        download_configs = config.BASE_CONFIG

        if log_file.exists():
            log_file.unlink()

    if not args.retry_failed:
        shutil.rmtree(output_dir, ignore_errors=True)
        for d in download_configs.keys():
            os.makedirs(output_dir.joinpath(d), exist_ok=True)

    with utils.get_browser() as browser:
        for category, items in download_configs.items():
            for item in items:
                print(f"Downloading [{category.title()}] {item['path']}...")

                path = output_dir.joinpath(category, item["path"])
                os.makedirs(path, exist_ok=True)

                try:
                    utils.download_and_save(*item["url"](browser), path=path)
                except Exception as e:
                    print(f"Failed: {e}")

                    if args.error_handling == "exit":
                        sys.exit(1)
                    elif args.error_handling == "log":
                        failed_downloads.setdefault(category, [])
                        failed_downloads[category].append(item)

    if args.error_handling == "log" and failed_downloads:
        utils.save_failed_downloads(log_file, failed_downloads)
        print(f"Failed downloads logged to {log_file}.")

    if len(failed_downloads) == 0 and not args.no_archive:
        archive.zip(args.archive_name,
                    "conf",
                    str(output_dir),
                    level=args.compress_level)
