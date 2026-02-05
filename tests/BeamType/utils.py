# /BeamType/utils.py

def log_info(message):
    '''Log Information'''
    print(f"[INFO]: {message}")

def log_warning(message):
    '''Log Warning'''
    print(f"[WARNING]: {message}")

def log_error(message):
    '''Log Error'''
    print(f"[ERROR]: {message}")

def validate_input(input_data: str) -> bool:
    '''Input Validation'''
    if not input_data:
        log_error("The data been inputed must not be empty")
        return False
    return True

def  validate_non_negative(name: str, data: float) -> bool:
    '''Non-negative Validation'''
    if data<0:
        log_error(f"The data of {name} must be non-negative")