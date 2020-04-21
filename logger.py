import logging as log

log.basicConfig(
    # filename='XPQE.log',
    # filemode='w',
    format='%(asctime)s [%(levelname)s] : %(name)s@%(lineno)d -> %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S %p',
    level=log.INFO
)

