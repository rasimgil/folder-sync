import argparse
import time

# main():
#   if args.folder_source is None:
#       print("argument error.")
#       exit
#   if args.folder_replica is None:
#       create_folder(args.folder_replica)
#   if timer = interval:
#       for file in args.folder_source:
#           file_replica = args.folder_replica[file]
#           if file_replica != file or file_replica is None:
#               sync(file, folder_replica)


def create_folder(path_replica):
    raise NotImplementedError()


def get_replica_file(file_source, path_replica):
    raise NotImplementedError()


def file_modified(file_source, file_replice):
    raise NotImplementedError()


def sync(file_source, folder_replica):
    raise NotImplementedError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Source folder path")
    parser.add_argument("--replica", help="Replica folder path")
    parser.add_argument("--interval", type=int, help="Sync interval")
    parser.add_argument("-o", help="Log file path")
    args = parser.parse_args()

    if args.source is None:
        print("Argument error 1")
        exit()

    if args.replica is None:
        create_folder(args.replica)

    timer = None
    if timer == args.interval:
        for file_source in args.source:
            file_replica = get_replica_file(file_source, args.replica)
            if file_modified(file_source, file_replica) or file_replica is None:
                sync(file_source, args.replica)
