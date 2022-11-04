#!/usr/bin/python
import logging
import logging.config

#logging.config.fileConfig("app-logging.conf")
#
#logging.basicConfig(filename='/tmp/appname.log', filemode='w', level=logging.DEBUG)
## create logger
#logger = logging.getLogger("simpleExample")
#
## "application" code
#logger.debug("debug message")
#logger.info("info message")
#logger.warn("warn message")
#logger.error("error message")
#logger.critical("critical message")

"""
Aplication calls this function and gets a logger back
"""
def InitializeLogger(appname="default"):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S.%f',
                        filename='/tmp/'+appname+'.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(name)-12s: %(levelname)-8s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S' )
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    return (logging.getLogger(appname))

if __name__ == '__main__':
    print("hello")
    lgr = InitializeLogger(appname="myapp")
    lgr.info("hello first logging")
    print("done with logger")

