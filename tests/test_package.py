import importlib

def test_package_metadata():
    mod = importlib.import_module("flzk")
    assert hasattr(mod, "DESCRIPTION")
    assert mod.DESCRIPTION.startswith("Verifiable")
