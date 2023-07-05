import re
from . import utils

def check_schema_start(str):
    return re.search("new Schema\(\{", str)

def check_schema_end(str):
    return re.search("\}\);", str)
        
def parse_schema(path):
    f = open(path, 'r')
    data = f.readlines()

    schemas = [] # array[array[]]
    cur_schema = []

    isSchema = False
    for d in data:
        if not isSchema:
            isSchema = check_schema_start(d)
            if not isSchema: # if still no schema -- opt-out
                continue

        # check if we hit then end of the model schema -- if so, reset
        if check_schema_end(d):
            isSchema = False
            schemas.append(cur_schema)

        cur_schema.append(utils.clean(d))

    return schemas
