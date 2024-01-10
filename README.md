# Folder Synchronization Script

This script facilitates the synchronization of two folders, ensuring that the content of the destination folder matches that of the source folder. It provides a command-line interface for specifying the source and destination folders, along with other parameters.

## Table of Contents
- [Introduction](#introduction)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [How it Works](#how-it-works)
- [Command Line Arguments](#command-line-arguments)
- [Logging](#logging)
- [Main Loop](#main-loop)

## Introduction

The script employs a hashing mechanism to identify differences between the source and destination folders. It supports various synchronization actions, including creating new folders in the destination, removing folders not present in the source, and copying files from the source to the destination.

## Usage

To use the script, execute it from the command line with the required arguments. The script will continuously run in a loop, periodically checking for changes in the source and updating the destination accordingly.

```bash
python script.py log_path source_path destination_path interval
```

- log_path: Path to the log file where synchronization activities are recorded.
- source_path: Path to the source folder.
- destination_path: Path to the destination folder.
- interval: Time interval (in seconds) between synchronization checks.

## Dependencies
The script requires the following dependencies:

- Python 3.x

## How it Works
1. Hashing Files:
The script calculates MD5 hashes for each file in the source and destination folders to identify changes.

2. Comparing Folders:
The MD5 hashes are compared to find files unique to each folder.

3. Synchronization Actions:
Folders with no content in the source are created in the destination.
Folders with no content in the destination are removed.
Files present only in the destination are removed.
Files present only in the source are copied to the destination.

4. Logging:
All synchronization activities are logged to a specified log file.

## Command Line Arguments
- log: Path to the log file.
- src: Path to the source folder.
- dst: Path to the destination folder.
- interval: Time interval between synchronization checks (in seconds).

## Logging
The script logs synchronization activities to the specified log file. Each action, such as folder creation, removal, or file copying, is recorded with a timestamp.

## Main Loop
The script runs in an infinite loop, periodically checking for changes in the source folder and updating the destination accordingly. The synchronization process is logged at each iteration.
