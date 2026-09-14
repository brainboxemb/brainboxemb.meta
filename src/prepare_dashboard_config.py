#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
from typing import Any

import yaml

DASHBOARD_OVERRIDE_KEYS = {
    "branch",
    "include_workflows",
    "exclude_workflows",
    "workflow_labels",
    "hide_reusable_only_workflows",
    "branch_cleanup_ignore_branches",
}


def load_yaml(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def catalog_groups(catalog: dict[str, Any], default_owner: str) -> list[dict[str, Any]]:
    if catalog.get("schema_version") != 1:
        raise ValueError("repositories/catalog.yml must use schema_version: 1")

    repositories = catalog.get("repositories")
    if not isinstance(repositories, list):
        raise ValueError("repositories/catalog.yml must contain a repositories list")

    groups: dict[str, list[str | dict[str, Any]]] = {}
    seen: set[str] = set()

    for item in repositories:
        if not isinstance(item, dict):
            raise ValueError(f"Catalog repository entry must be a mapping: {item!r}")

        full_name = str(item.get("repository") or "").strip()
        if full_name.count("/") != 1:
            raise ValueError(f"Catalog repository must use owner/name: {full_name!r}")
        owner, name = full_name.split("/", 1)
        if not owner or not name:
            raise ValueError(f"Catalog repository must use owner/name: {full_name!r}")
        if full_name in seen:
            raise ValueError(f"Duplicate catalog repository: {full_name}")
        seen.add(full_name)

        group = str(item.get("dashboard_group") or "").strip()
        if not group:
            raise ValueError(f"Catalog repository is missing dashboard_group: {full_name}")

        dashboard = item.get("dashboard") or {}
        if not isinstance(dashboard, dict):
            raise ValueError(f"dashboard override must be a mapping: {full_name}")
        if dashboard.get("visible", True) is False:
            continue

        entry: dict[str, Any] = {"name": name}
        if owner != default_owner:
            entry["owner"] = owner
        for key in DASHBOARD_OVERRIDE_KEYS:
            if key in dashboard:
                entry[key] = dashboard[key]

        rendered: str | dict[str, Any]
        rendered = name if set(entry) == {"name"} else entry
        groups.setdefault(group, []).append(rendered)

    return [
        {"name": group_name, "repositories": entries}
        for group_name, entries in groups.items()
    ]


def build_runtime_config(
    config_path: pathlib.Path,
    catalog_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    config = load_yaml(config_path)
    dashboard = config.get("dashboard")
    if not isinstance(dashboard, dict):
        raise ValueError("dashboard.yml must contain a dashboard mapping")

    owner = str(dashboard.get("owner") or "").strip()
    if not owner:
        raise ValueError("dashboard.owner is required")

    if catalog_path is None:
        configured = config.get("catalog")
        if not configured:
            raise ValueError("dashboard.yml must contain catalog: <path>")
        catalog_path = pathlib.Path(str(configured))
        if not catalog_path.is_absolute():
            catalog_path = config_path.parent / catalog_path

    catalog = load_yaml(catalog_path)
    runtime = dict(config)
    runtime["groups"] = catalog_groups(catalog, owner)
    return runtime


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the existing dashboard runtime config from the canonical repository catalog"
    )
    parser.add_argument("--config", type=pathlib.Path, default=pathlib.Path("dashboard.yml"))
    parser.add_argument("--catalog", type=pathlib.Path)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path(".dashboard.runtime.yml"),
    )
    args = parser.parse_args()

    runtime = build_runtime_config(args.config, args.catalog)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(runtime, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    repository_count = sum(len(group["repositories"]) for group in runtime["groups"])
    print(
        f"Wrote {args.output} with {repository_count} repositories in "
        f"{len(runtime['groups'])} groups"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
