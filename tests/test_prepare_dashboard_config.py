import importlib.util
import pathlib
import tempfile
import unittest

MODULE = pathlib.Path(__file__).parents[1] / "src" / "prepare_dashboard_config.py"
spec = importlib.util.spec_from_file_location("prepare_dashboard_config", MODULE)
prepare = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(prepare)


class PrepareDashboardConfigTests(unittest.TestCase):
    def test_build_runtime_config_from_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "repositories").mkdir()
            (root / "dashboard.yml").write_text(
                "dashboard:\n  owner: brainboxemb\ncatalog: repositories/catalog.yml\n",
                encoding="utf-8",
            )
            (root / "repositories" / "catalog.yml").write_text(
                """schema_version: 1
repositories:
  - repository: brainboxemb/tool.one
    category: tooling
    dashboard_group: Tooling
  - repository: other/example
    category: experiment
    dashboard_group: Experiments
    dashboard:
      branch: develop
""",
                encoding="utf-8",
            )

            config = prepare.build_runtime_config(root / "dashboard.yml")

        self.assertEqual(
            config["groups"],
            [
                {"name": "Tooling", "repositories": ["tool.one"]},
                {
                    "name": "Experiments",
                    "repositories": [
                        {"name": "example", "owner": "other", "branch": "develop"}
                    ],
                },
            ],
        )

    def test_duplicate_repository_is_rejected(self):
        catalog = {
            "schema_version": 1,
            "repositories": [
                {"repository": "brainboxemb/one", "dashboard_group": "A"},
                {"repository": "brainboxemb/one", "dashboard_group": "B"},
            ],
        }
        with self.assertRaisesRegex(ValueError, "Duplicate catalog repository"):
            prepare.catalog_groups(catalog, "brainboxemb")

    def test_hidden_repository_stays_in_catalog_but_not_dashboard_groups(self):
        catalog = {
            "schema_version": 1,
            "repositories": [
                {
                    "repository": "brainboxemb/hidden",
                    "dashboard_group": "Experiments",
                    "dashboard": {"visible": False},
                }
            ],
        }
        self.assertEqual(prepare.catalog_groups(catalog, "brainboxemb"), [])


if __name__ == "__main__":
    unittest.main()
