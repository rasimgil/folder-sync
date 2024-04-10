import argparse
import os
import shutil
import sys
import time
import logging
logger = logging.getLogger()

def synced(file_source: str, file_replica: str) -> bool:
    return os.path.getmtime(file_source) == os.path.getmtime(file_replica)

def log_operation(operation: chr, item_source: str=None, item_replica: str=None) -> None:
    match operation:
        case 'c':
            logger.info(f"[CREATE] {item_replica}")
        case 'p':
            logger.info(f"[COPY] {item_source} > {item_replica}")
        case 'd':
            logger.info(f"[DELETE]: {item_replica}")


def sync_file(file_source: str, file_replica: str) -> None:
    if not os.path.exists(file_replica):
        log_operation('c', file_replica, item_replica=file_replica)
    if not os.path.exists(file_replica) or not synced(file_source, file_replica):
        os.makedirs(os.path.dirname(file_replica), exist_ok=True)
        shutil.copy2(file_source, file_replica)
        log_operation('p', file_source, file_replica)

def sync_directory(dir_source: str, dir_replica: str) -> None:
    for item in os.listdir(dir_source):
        item_source = os.path.join(dir_source, item)
        item_replica = os.path.join(dir_replica, item)
        if os.path.isdir(item_source):
            if not os.path.exists(item_replica):
                os.makedirs(item_replica)
                log_operation('c', item_replica=item_replica)
            sync_directory(item_source, item_replica)
        else:
            sync_file(item_source, item_replica)

    for item in os.listdir(dir_replica):
        item_replica = os.path.join(dir_replica, item)
        item_source = os.path.join(dir_source, item)
        if not os.path.exists(item_source):
            if os.path.isdir(item_replica):
                shutil.rmtree(item_replica)
            else:
                os.remove(item_replica)
            log_operation('d', item_replica)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=str, help="Source folder path", required=True)
    parser.add_argument("-r", "--replica", type=str, help="Replica folder path", required=True)
    parser.add_argument("-i", "--interval", type=int, help="Sync interval", required=True)
    parser.add_argument("-o", "--output", type=str, help="Log file path", required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print("Invalid source folder")
        exit(0)

    logging.basicConfig(filename=args.output, level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(message)s')
    while True:
        try:
            sync_directory(args.source, args.replica)
            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("exiting the program")
            sys.exit(0)
