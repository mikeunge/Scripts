#!/usr/bin/env python3
from lib import fs
from lib import parser

def main():
    files = ['./data/DBUserModel.ts']
    for file in files:
        if not fs.file_exists(file):
            print(f'file {file} does not exist')
            continue
        schemas = parser.parse_schema(file)
        print(schemas[0])

if __name__ == '__main__':
    main()