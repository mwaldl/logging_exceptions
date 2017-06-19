import logging
import argparse
import logging_exceptions

parser = argparse.ArgumentParser()
logging_exceptions.update_parser(parser)


def foo():
    log = logging.getLogger("main.foo")
    log.info("Logging is enabled for logger 2.")
    for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
        log.log(level, "Logging at level %s.", level)

def raise_error(value):
    try:
        raise ValueError("Test value Error")
    except ValueError as e:
        logging_exceptions.attach(e, "raise_error called with value %s", value)
        raise

def raise_error_contextmngr(value):
    e = ValueError("Another ValueError")
    log = logging.getLogger("main.inside_ctxt")
    log.info("Before with-context. This is logged directly")
    with logging_exceptions.log_to_exception(log, e):
        log.debug("This is DEBUG ... %s", value)
        log.info("This is an INFO ... %s", value)
        log.warning("This is a WARNING ... %s", value)
        log.error("This is an ERROR ... %s", value)
        log.critical("This is CRITICAL ... %s", value)
    log.info("After with-context. This is logged directly")
    raise e

def raise_error_contextmngr2(value):
    e = ValueError("Another ValueError")
    log = logging.getLogger("main.inside_ctxt")
    log.info("Before with-context. This is logged directly")
    with logging_exceptions.log_to_exception(log, e):
        log.debug("This is DEBUG ... %s", value)
        log.info("This is an INFO ... %s", value)
        log.warning("This is a WARNING ... %s", value)
        log.error("This is an ERROR ... %s", value)
        log.critical("This is CRITICAL ... %s", value)
        log.info("Raising inside with context")
        raise e

if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig()
    logging_exceptions.use_colored_output(True)
    logging_exceptions.config_from_args(args)
    log = logging.getLogger("main1")
    log.info("Logging is enabled for logger 1.")

    for level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
        log.log(level, "Logging at level %s.", level)

    foo()

    try:
        raise_error(24)
    except Exception as e:
        logging_exceptions.log_exception(e, logging.INFO)

    try:
        raise_error(124)
    except Exception as e:
        logging_exceptions.log_exception(e, logger=log)

    try:
        raise_error(42)
    except Exception as e:
        logging_exceptions.log_exception(e, logging.WARNING, logger=logging.getLogger("main.exception"))

    try:
        raise_error_contextmngr(120)
    except Exception as e:
        logging_exceptions.log_exception(e, logging.WARNING)
    try:
        raise_error_contextmngr(555)
    except Exception as e:
        logging_exceptions.log_exception(e)

    try:
        raise_error_contextmngr2(12345)
    except Exception as e:
        logging_exceptions.log_exception(e)




    log.info("Almost there")
    raise_error_contextmngr(-1)
