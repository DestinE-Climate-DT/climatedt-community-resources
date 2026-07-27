from typing import Any


def extract_first_item(search_json: dict[str, Any]) -> dict[str, Any]:
    """Return first item from STAC search response or fail with context."""
    features = search_json.get("features", [])
    if not features:
        raise ValueError(
            "Search returned no features. Narrow or adjust search filters "
            "(datetime, bbox, limit) and try again."
        )
    return features[0]


def extract_all_items(search_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Return all items from a STAC search response or fail with context."""
    features = search_json.get("features", [])
    if not features:
        raise ValueError(
            "Search returned no features. Narrow or adjust search filters "
            "(datetime, bbox, limit) and try again."
        )
    return features


def extract_item_assets(item: dict[str, Any]) -> list[dict[str, str]]:
    """Return individual asset entries with href from a single item.

    The aggregate ``downloadLink`` asset is excluded because it represents
    a whole-item archive rather than an individual file.
    """
    assets = item.get("assets")

    if not isinstance(assets, dict) or not assets:
        raise ValueError("Search result item does not include a non-empty assets object")

    extracted_assets: list[dict[str, str]] = []
    for asset_name, asset_details in assets.items():
        if str(asset_name) == "downloadLink":
            continue

        if not isinstance(asset_details, dict):
            continue

        href = asset_details.get("href")
        if not isinstance(href, str) or not href.strip():
            continue

        normalized_asset: dict[str, str] = {"name": str(asset_name), "href": href}

        asset_type = asset_details.get("type")
        asset_title = asset_details.get("title")
        if isinstance(asset_type, str) and asset_type:
            normalized_asset["type"] = asset_type
        if isinstance(asset_title, str) and asset_title:
            normalized_asset["title"] = asset_title

        extracted_assets.append(normalized_asset)

    if not extracted_assets:
        raise ValueError("Search result item assets do not contain valid href values")

    return extracted_assets


def extract_first_item_assets(search_json: dict[str, Any]) -> list[dict[str, str]]:
    """Return individual asset entries with href from the first item."""
    return extract_item_assets(extract_first_item(search_json))
