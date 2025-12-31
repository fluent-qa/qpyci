import qpyci.commands as c


def test_all():
    c.check_format()
    c.ci()
    c.generate_badge()
    c.cleanup()
