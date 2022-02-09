import sys

class Logger:
    '''A very simple logger which logs to arbitrary streams based on a verbosity setting provided.'''
    
    def __init__(self, verbose=True, infostream=sys.stdout, criticalstream=sys.stderr) -> None:
        self.verbose = verbose
        self.infostream = infostream
        self.criticalstream = criticalstream
    
    def set_verbose(self, verbose: bool) -> None:
        self.verbose = verbose
    
    def get_verbose(self) -> bool:
        return self.verbose
    
    def info_verbose(self, msg: str) -> None:
        if self.verbose:
            print("[*] " + msg, file=self.infostream)

    def info(self, msg: str) -> None:
        print("[*] " + msg, file=self.infostream)
    
    def critical(self, msg: str) -> None:
        print("[X] " + msg, file=self.criticalstream)