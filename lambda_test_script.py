import process_NG_data

event = {'Records': [{'sns':{'message': 'test message from script test event'}}]}

process_NG_data.lambda_handler(event, None)
