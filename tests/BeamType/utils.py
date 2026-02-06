# /beamtype/utils.py

def log_info(message):
    '''Log Information'''
    print(f"[INFO]: {message}")

def log_warning(message):
    '''Log Warning'''
    print(f"[WARNING]: {message}")

def log_error(message):
    '''Log Error'''
    print(f"[ERROR]: {message}")

def validate_2_num(data: str):
    if data.isdigit():
        return int(data)
    else:
        try:
            return float(data)
        except ValueError:
            log_error("The data is not a number")
            return False

def validate_2_int(data: str):
    try:
        return int(data)
    except ValueError:
        log_error("The data is not an integrate")
        return False

def validate_2_float(data: str):
    if data.isdigit():
        log_warning("It seems that the data is an integrate, but float is required")
    try:
        return float(data)
    except ValueError:
        log_error("The data is not a float")
        return False

def validate_input(input_data: str) -> bool:
    '''Input Validation'''
    if not input_data:
        log_error("The data been inputed must not be empty")
        return False
    return True

def  validate_non_negative(data) -> bool:
    '''Non-negative Validation'''
    if data<0:
        log_error(f"The data must be non-negative")
        return False
    return True