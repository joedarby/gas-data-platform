import process_NG_data
import get_NG_data


message = get_NG_data.lambda_handler(None, None)

event = {'Records': [{'sns':{'message': message}}]}

process_NG_data.lambda_handler(event, None)
