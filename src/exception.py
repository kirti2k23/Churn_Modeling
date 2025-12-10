class MyCustomException(Exception):

    def __init__(self, error:Exception):

        # If error is already a string, noe tarceback needed
        if isinstance(error,str):
            super().__init__(error)
            return

        # Traceback original error location
        tb = error.__traceback__

        # Go to last frame where it actually crashed
        while tb.tb_next is not None:
            tb = tb.tb_next
        
        # Extract filename and lineno
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno

        # Build your own message
        message = f'{error} has occurred in {filename} at {lineno}'

        # Initialize base Exception with this message
        super().__init__(message)

# try:
#     a = 10/0
# except Exception as e:
#     raise(MyCustomException(e))