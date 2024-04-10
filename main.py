import argparse
import os
import shutil
import sys
import time
import logging

logger = logging.getLogger()


def synced(file_source: str, file_replica: str) -> bool:
    return os.path.getmtime(file_source) == os.path.getmtime(file_replica)


def log_operation(message: str, verbose: bool, level: logging.INFO) -> None:
    timestamp = f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
    if verbose:
        print(f"{timestamp}, {message}")
    logger.log(level, message)



def sync_file(file_source: str, file_replica: str) -> None:
    try:
        if not os.path.exists(file_replica):
            message = f"CREATE {file_replica}"
            log_operation(message, args.verbose, logging.INFO)
        if not os.path.exists(file_replica) or not synced(file_source, file_replica):
            os.makedirs(os.path.dirname(file_replica), exist_ok=True)
            shutil.copy2(file_source, file_replica)
            message = f"COPY {file_source} {file_replica}"
            log_operation(message, args.verbose, logging.INFO)
    except FileNotFoundError:
        message = f"File not found: {file_source}"
        log_operation(message, args.verbose, logging.ERROR)
    except PermissionError:
        message = f"Permission denied: {file_replica}"
        log_operation(message, args.verbose, logging.ERROR)
    except Exception as e:
        message = f"An error has occurred during copying {file_source}"
        log_operation(message, args.verbose, logging.ERROR)


def sync_directory(dir_source: str, dir_replica: str) -> None:
    for item in os.listdir(dir_source):
        item_source = os.path.join(dir_source, item)
        item_replica = os.path.join(dir_replica, item)
        if os.path.isdir(item_source):
            try:
                if not os.path.exists(item_replica):
                    os.makedirs(item_replica)
                    # FILE CREATED
                    message = f"CREATE {item_replica}"
                    log_operation(message, args.verbose, logging.INFO)
                sync_directory(item_source, item_replica)
            except FileNotFoundError:
                message = f"Directory not found: {item_source}"
                log_operation(message, args.verbose, logging.ERROR)
            except PermissionError:
                message = f"Permission denied: {item_replica}"
                log_operation(message, args.verbose, logging.ERROR)
            except Exception as e:
                message = (
                    f"An error has occurred creating directory {item_replica}: {e}"
                )
                log_operation(message, args.verbose, logging.ERROR)
        else:
            sync_file(item_source, item_replica)

    for item in os.listdir(dir_replica):
        item_replica = os.path.join(dir_replica, item)
        item_source = os.path.join(dir_source, item)
        if not os.path.exists(item_source):
            try:
                if os.path.isdir(item_replica):
                    shutil.rmtree(item_replica)
                else:
                    os.remove(item_replica)
                message = f"DELETE {item_replica}"
                log_operation(message, args.verbose, logging.INFO)
            except FileNotFoundError:
                message = f"File not found: {item_replica}"
                log_operation(message, args.verbose, logging.ERROR)
            except PermissionError:
                message = f"Permission denied: {item_replica}"
                log_operation(message, args.verbose, logging.ERROR)
            except Exception as e:
                message = f"An Error has occurred deleting {item_replica}"
                log_operation(message, args.verbose, logging.ERROR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--source", type=str, help="Source folder path", required=True
    )
    parser.add_argument(
        "-r", "--replica", type=str, help="Replica folder path", required=True
    )
    parser.add_argument(
        "-i", "--interval", type=int, help="Sync interval", required=True
    )
    parser.add_argument("-o", "--output", type=str, help="Log file path", required=True)
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print("Invalid source folder.")
        exit(0)

    logging.basicConfig(
        filename=args.output,
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s %(message)s",
    )

    while True:
        try:
            log_operation("START", args.verbose, logging.INFO)
            sync_directory(args.source, args.replica)
            log_operation("END", args.verbose, logging.INFO)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("Exiting the program.")
            sys.exit(0)
        except Exception as e:
            message = f"An unexpected error has occurred: {e}"
            log_operation(message, args.verbose, logging.ERROR)
