import os
import shutil
import argparse
import time


def log(log_file, message, level="info"):
    """logging"""
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {level}: {message}\n")
        print(message)


def sync_folders(source_folder, replica_folder, log_file):
    """sync source and replica folders, handling errors and logging."""

    if not os.path.exists(source_folder):
        log(
            log_file,
            f"Error: Source folder '{source_folder}' does not exist.",
            level="error",
        )
        return

    try:
        os.makedirs(
            replica_folder, exist_ok=True
        )  # Create replica folder if needed (without error)
    except OSError as e:
        log(log_file, f"Error creating replica folder: {e}", level="error")
        return

    # create files and folders from replica if they don't exist in source
    for root, dirs, items in os.walk(source_folder):
        for item in items:
            source_path = os.path.join(root, item)
            replica_path = os.path.join(
                replica_folder, os.path.relpath(source_path, source_folder)
            )

            try:
                # Check modification times for efficient copy
                if not os.path.exists(replica_path) or os.path.getmtime(
                    source_path
                ) > os.path.getmtime(replica_path):
                    shutil.copy2(source_path, replica_path)
                    log(log_file, f"Copied {source_path} to {replica_path}")
            except OSError as e:
                log(log_file, f"Error copying file: {e}", level="error")

        for dir_name in dirs:
            source_dir = os.path.join(root, dir_name)
            replica_dir = os.path.join(
                replica_folder, os.path.relpath(source_dir, source_folder)
            )
            try:
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    log(log_file, f"Copied {source_dir} to {replica_dir}")
            except OSError as e:
                log(log_file, f"Error copying folder: {e}", level="error")

    # remove files and folders from replica if they don't exist in source
    for root, dirs, items in os.walk(replica_folder):
        for file_name in items:
            replica_file = os.path.join(root, file_name)
            source_file = os.path.join(
                source_folder, os.path.relpath(replica_file, replica_folder)
            )
            if not os.path.exists(source_file):
                try:
                    os.remove(replica_file)
                    log(log_file, f"Removed {replica_file}")
                except OSError as e:
                    log(log_file, f"Error removing file: {e}", level="error")

        for dir_name in dirs:
            replica_dir = os.path.join(root, dir_name)
            source_dir = os.path.join(
                source_folder, os.path.relpath(replica_dir, replica_folder)
            )
            if not os.path.exists(source_dir):
                try:
                    os.rmdir(replica_dir)
                    log(log_file, f"Removed {replica_dir}")
                except OSError as e:
                    log(log_file, f"Error removing file: {e}", level="error")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_folder", help="Path to source folder")
    parser.add_argument("replica_folder", help="Path to replica folder")
    parser.add_argument("log_file", help="Path to log file")
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Synchronization interval in seconds (default: 60)",
    )
    args = parser.parse_args()

    while True:
        sync_folders(args.source_folder, args.replica_folder, args.log_file)
        time.sleep(args.interval)
