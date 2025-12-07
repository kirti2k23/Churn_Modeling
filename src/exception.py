class MyCustomException(Exception):

    def __init__(self, error:Exception):
        tb = error.__traceback__

        while tb.tb_next is not None:
            tb = tb.tb_next
        
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno

        message = f'{error} has occurred in {filename} at {lineno}'

        super().__init__(message)

