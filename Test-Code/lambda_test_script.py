import sys

sys.path.insert(0, '/home/joe/PycharmProjects/gas-data-platform/Lambda-NG-process-data')
sys.path.insert(1, '/home/joe/PycharmProjects/gas-data-platform/Lambda-NG-get-file')

import get_NG_data
import process_NG_data

message = get_NG_data.lambda_handler(None, None)

event = {'Records': [{'Sns':{'Message': message}}]}

process_NG_data.lambda_handler(event, None)
