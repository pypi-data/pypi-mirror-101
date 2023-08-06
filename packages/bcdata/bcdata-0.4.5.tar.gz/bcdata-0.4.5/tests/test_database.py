from bcdata import database


def test_connection():
    db = database.Database()
    assert "crd" in db.schemas
