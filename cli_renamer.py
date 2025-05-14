import os
import argparse

def rename_files(folder, prefix, extension_filter=None, dry_run=False):
    if not os.path.isdir(folder):
        print("Provided path is not a valid directory.")
        return

    renamed_files = []
    for filename in os.listdir(folder):
        if extension_filter and not filename.endswith(extension_filter):
            continue

        old_path = os.path.join(folder, filename)
        new_filename = f"{prefix}_{filename}"
        new_path = os.path.join(folder, new_filename)

        if not dry_run:
            os.rename(old_path, new_path)

        renamed_files.append((filename, new_filename))

    with open("log.txt", "w") as log_file:
        for old, new in renamed_files:
            log_file.write(f"{old} -> {new}\n")

    print(f"{'Dry run: would rename' if dry_run else 'Renamed'} {len(renamed_files)} file(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files in a folder.")
    parser.add_argument("folder", help="Folder containing files to rename")
    parser.add_argument("prefix", help="Prefix to add to filenames")
    parser.add_argument("--ext", help="Only rename files with this extension, e.g., .txt")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the renaming without changing files")

    args = parser.parse_args()
    rename_files(args.folder, args.prefix, args.ext, args.dry_run)
