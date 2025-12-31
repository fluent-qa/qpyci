import qpyci.commands as c


def test_badge():
    c.generate_badge()


def test_ci():
    c.ci()


def test_clean():
    c.cleanup()
