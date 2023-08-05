from vsw.commands import verify


def test_main():
    verify.execute("software", "XGLt7XwLkZrYLGsSf2TZEz", "https://files.pythonhosted.org/packages/07/83/a94950cf449b3fd253efe1a1e0953f6a0846cd0d8842accf925d744f176a/aa-gen-0.0.13.tar.gz", "schema2", None)


def test_retrieve_results():
    verify.retrieve_result("01168b93-ea56-452e-b7ca-e14d4be1bfca")


def test_check_credential():
    verify.check_credential("1234", "python")