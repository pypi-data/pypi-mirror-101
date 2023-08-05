def test_query(query):
    assert query["CodEstatus"] == "5000"


def test_verify(sat_connector, query):
    response = sat_connector.verify(query["IdSolicitud"])
    return response


def test_download(sat_connector, package_ids):
    downloads = sat_connector.download(package_ids)
    return downloads
