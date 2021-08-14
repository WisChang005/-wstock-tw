from src.wstock_tw import wstock


def test_verify_the_stock_inventory_not_empty():
    assert wstock.twse
    assert wstock.tpex


def test_the_id_3048_in_twse_and_not_in_tpex():
    # 益登
    assert ("3048" in wstock.twse)
    assert ("3048" not in wstock.tpex)


def test_the_id_8476_no_in_twse_in_tpex():
    # 大洋環球控股
    assert ("8476" not in wstock.twse)
    assert ("8476" in wstock.tpex)


def test_stock_is_opened():
    assert (wstock.open_state in (True, False))
