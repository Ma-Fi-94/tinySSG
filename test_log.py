import log
import io


def test_logger_get_set_verbose():
    logger = log.Logger(verbose=True)
    assert logger.get_verbose() == True

    logger.set_verbose(False)
    assert logger.get_verbose() == False

    logger.set_verbose(True)
    assert logger.get_verbose() == True


def test_logger_critical():
    captured_output = io.StringIO()
    logger = log.Logger(verbose=True, criticalstream=captured_output)
    logger.critical("abcdefg")
    assert captured_output.getvalue() == "[X] abcdefg\n"

    captured_output = io.StringIO()
    logger = log.Logger(verbose=False, criticalstream=captured_output)
    logger.critical("abcdefg")
    assert captured_output.getvalue() == "[X] abcdefg\n"


def test_logger_info_verbose():
    captured_output = io.StringIO()
    logger = log.Logger(verbose=True, infostream=captured_output)
    logger.info_verbose("abcdefg")
    assert captured_output.getvalue() == "[*] abcdefg\n"

    captured_output = io.StringIO()
    logger = log.Logger(verbose=False, infostream=captured_output)
    logger.info_verbose("abcdefg")
    assert captured_output.getvalue() == ""


def test_logger_info():
    captured_output = io.StringIO()
    logger = log.Logger(verbose=True, infostream=captured_output)
    logger.info("abcdefg")
    assert captured_output.getvalue() == "[*] abcdefg\n"

    captured_output = io.StringIO()
    logger = log.Logger(verbose=False, infostream=captured_output)
    logger.info("abcdefg")
    assert captured_output.getvalue() == "[*] abcdefg\n"
