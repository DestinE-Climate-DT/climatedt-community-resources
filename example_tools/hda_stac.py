from typing import Any


def fetch_all_items(
    search_url: str,
    body: dict[str, Any],
    auth_headers: dict[str, str],
    timeout: int = 30,
    retries: int = 3,
) -> list[dict[str, Any]]:
    """POST a STAC search and follow all 'next' pagination links until exhausted.

    The API returns at most ``limit`` items per page. Pass this function the
    same body you would pass to a single ``request_json`` call and it will
    collect every page automatically.
    """
    from hda_http import request_json

    all_items: list[dict[str, Any]] = []
    current_body = dict(body)

    while True:
        page = request_json(
            "POST",
            search_url,
            headers=auth_headers,
            json_body=current_body,
            timeout=timeout,
            retries=retries,
        )
        features = page.get("features", [])
        all_items.extend(features)

        next_link = next(
            (lnk for lnk in page.get("links", []) if lnk.get("rel") == "next"),
            None,
        )
        if not next_link or not next_link.get("body"):
            break
        current_body = next_link["body"]

    return all_items


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
