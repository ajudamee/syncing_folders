
import os
import argparse
import hashlib
import shutil
import time
import string

#function that handles command line arguments
def commandLine():

    # Create an argument parser with descriptions and default help formatting
    parser = argparse.ArgumentParser(description="Syncronize folders",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # Define command line arguments
    parser.add_argument("log", help="log path")
    parser.add_argument("src", help="Source path")
    parser.add_argument("dst", help="Destination path")
    parser.add_argument("interval", type=int, help="interval")

    # Parse the command line arguments and convert them to a dictionary
    args = parser.parse_args()
    config = vars(args)

    return config    

#function that generates map file paths to their corresponding MD5 hashes
def mapHashFiles(path):
    fileHash = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            fullFilePath = os.path.join(root,file)
            filePath = os.path.relpath(fullFilePath,path)
            md5_hash = MD5(os.path.join(root, file))
            fileHash[filePath] = md5_hash 

    return fileHash

#function that calculates the MD5 hash of a file
def MD5(fileName):
    with open(fileName, 'rb') as file_obj:
        file_contents = file_obj.read()
        md5_hash = hashlib.md5(file_contents).hexdigest()

        return md5_hash

#function that compares two dictionaries representing file paths and their hashes   
def compareFolders(src, dst):
        if src == dst:
            return {}

        else:
            Scronly = set(src.keys()) - set(dst.keys())
            Dstonly = set(dst.keys()) - set(src.keys())

            differences = {
                'files only in source': Scronly,
                'files only in replica': Dstonly,
            }
        return differences

#function that creates empty folders in the destination path based on the source path
def emptyFolders(srcPath, dstPath, logPath):

    newFolderPath = ""

    for dirPath, dirnames, filenames in os.walk(srcPath):
        if not dirnames and not filenames:
            relativePath = os.path.relpath(dirPath, srcPath)
            newFolderPath = os.path.join(dstPath, relativePath)
            if not os.path.exists(newFolderPath):
                os.mkdir(newFolderPath)
                print('created: ' + newFolderPath + '\n')
                with open(logPath, 'a') as log:
                    log.write('created: ' + newFolderPath + '\n')

        for dirPath, dirnames, filenames in os.walk(dstPath):
            if not dirnames and not filenames:
                folderPath = dirPath
                if folderPath != newFolderPath:
                    shutil.rmtree(folderPath)
                    print('removed: ' + folderPath + '\n')
                    with open(logPath, 'a') as log:
                        log.write('removed: ' + folderPath + '\n')

#function that synchronizes folders based on the differences found   
def syncFolders(differences, srcPath, dstPath, logPath):
    print('Syncing folders...')
    print(differences)
    with open(logPath, 'a') as log:
        log.write('Syncing folders...\n')
    emptyFolders(srcPath, dstPath, logPath)
    for key, value in differences.items():

        if key == 'files only in replica':
            for item in value:
                fullItemPath = os.path.join(dstPath, item)
                print('removed: ' + fullItemPath + '\n')
                os.remove(os.path.join(dstPath, item))
                with open(logPath, 'a') as log:
                    log.write('removed: ' + item + '\n')

        if key == 'files only in source':
            for item in value:
                fullItemPath = os.path.join(srcPath, item)
                dest = os.path.join(dstPath, item)
                destPath = os.path.dirname(dest)
                os.makedirs(destPath, exist_ok=True)

                print('copied: ' + dest + '\n')
                shutil.copy2(fullItemPath, dest)
                with open(logPath, 'a') as log:
                    log.write('copied: ' + dest + '\n')

#main function that runs the synchronization process in a loop
def main():
    while True:
        config = commandLine()
        srcPath = config['src']
        dstPath = config['dst']
        logPath = config['log']
        interval = config['interval']
        srcHash = mapHashFiles(srcPath)
        destHash = mapHashFiles(dstPath)

        syncFolders(compareFolders(srcHash, destHash), srcPath, dstPath, logPath)   
        time.sleep(interval)

if __name__ == "__main__":
    main()
