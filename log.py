class Logger:
    '''A very simple logger which logs to screen based on verbosity.'''
    
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
    
    def info_verbose(self, msg: str) -> None:
        if self.verbose:
            print("[*] " + msg)

    def info(self, msg: str) -> None:
        print("[*] " + msg)
    
    def critical(self, msg: str) -> None:
        print("[X] " + msg)
