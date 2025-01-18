# ADBDeleter

a tool for delete file securely on Android

## Requirements

python(3.6+)

pip

## Usage

Syntax:adbdeleter [options] [target_file_path] [mode]

Options:

-f(Force but dangerous and need device rooted)delete your files in root mode

Modes:

fast (and insecure mode):1 write zeros and 1 android rm command

safe (slow but secure mode):37 write randoms 1 write zeros and 1 android rm command



Steps:

connect to your device and enable usb debugging

next run this tool

Example:

adbdeleter /sdcard/test.txt safe

adbdeleter /sdcard/Pictures/DCIM/xxx.png safe

adbdelter /sdcard/notimportfile.txt fast



## Principle

This tool use 38 times android dd command to delete your data in target file,so use to delete files your files may not be recoverable.

## Questions

Q:Why it shows permission error?

A:Becuase Linux permission mechanism block it,maybe you are deleting important system files,do not do it