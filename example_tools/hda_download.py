import shutil
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlparse

import requests
from tqdm.auto import tqdm

from hda_http import _request_with_retry
from hda_stac import extract_all_items, extract_item_assets


def _relative_path_from_href(
    href: str,
    fallback_name: str | None,
    collection_id: str | None = None,
    item_id: str | None = None,
) -> Path:
    """Derive a sanitized relative filesystem path from an asset href's URL path."""
    decoded_path = unquote(urlparse(href).path)
    segments = [s for s in PurePosixPath(decoded_path).parts if s not in ("", "/", ".", "..")]
    if collection_id and item_id:
        for i in range(len(segments) - 1):
            if segments[i] == collection_id and segments[i + 1] == item_id:
                segments = segments[i + 2:]
                break
    if not segments:
        segments = [
            s
            for s in PurePosixPath(fallback_name or "").parts
            if s not in ("", "/", ".", "..")
        ]
    if not segments:
        segments = ["downloaded_asset"]
    return Path(*segments)


def _resolve_destination_path(base_dir: Path, relative_path: Path) -> Path:
    """Join relative_path under base_dir, raising if it would escape base_dir."""
    destination = (base_dir / relative_path).resolve()
    if not destination.is_relative_to(base_dir.resolve()):
        raise ValueError(f"Resolved asset path escapes destination directory: {destination}")
    return destination


def _apply_existing_policy(path: Path, existing_policy: str) -> bool:
    """Handle a pre-existing destination per existing_policy.

    Returns True if the caller should skip the download.
    """
    if existing_policy not in ("skip", "overwrite"):
        raise ValueError(
            f"Unsupported existing_policy: {existing_policy}. Supported: skip, overwrite"
        )
    if not path.exists():
        return False
    if existing_policy == "skip":
        return True
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return False


def download_item_archive(
    download_url: str,
    item_id: str,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    chunk_size: int = 8192,
    existing_policy: str = "skip",
) -> str:
    """Download an item's whole-item zip archive via downloadLink and return the filename."""
    destination = Path(f"{item_id}.zip")
    if _apply_existing_policy(destination, existing_policy):
        print(f"Skipping existing archive: {destination}")
        return str(destination)

    response = _request_with_retry(
        method="GET",
        url=download_url,
        headers=headers,
        timeout=timeout,
        retries=3,
        stream=True,
    )

    total_size = int(response.headers.get("Content-Length", 0))
    print("Downloading ...")

    with destination.open("wb") as fp, tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc="Downloading",
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                fp.write(chunk)
                progress_bar.update(len(chunk))

    return str(destination)


def download_item_assets(
    search_json: dict[str, Any],
    collection_id: str,
    auth_headers: dict[str, str],
    request_timeout: int,
    chunk_size: int = 8192,
    existing_policy: str = "skip",
) -> dict[str, int]:
    """Download every asset from every item returned by a search with a progress bar.

    Returns a summary dict with ``total``, ``successful``, ``failed``, ``skipped``.
    """
    items = extract_all_items(search_json)
    total_assets = sum(len(extract_item_assets(item)) for item in items)

    print(f"Found {len(items)} items containing {total_assets} assets.")

    session = requests.Session()
    session.headers.update(auth_headers)

    successful = 0
    failed = 0
    skipped = 0

    try:
        with tqdm(total=total_assets, desc="Overall", position=0, dynamic_ncols=True) as overall_bar:
            for item in items:
                item_id = item.get("id")
                if not item_id:
                    print("Skipping item with no id.")
                    continue

                assets = extract_item_assets(item)
                destination_dir = Path(collection_id) / item_id

                if _apply_existing_policy(destination_dir, existing_policy):
                    print(f"\nItem: {item_id}")
                    print(f"  Skipping existing item: {destination_dir}")
                    skipped += len(assets)
                    overall_bar.update(len(assets))
                    continue

                destination_dir.mkdir(parents=True, exist_ok=True)
                print(f"\nItem: {item_id}")

                for asset in assets:
                    href = asset["href"]
                    asset_label = (
                        asset.get("name")
                        or unquote(Path(urlparse(href).path).name)
                        or "asset"
                    )

                    relative_path = _relative_path_from_href(
                        href, asset.get("name"), collection_id=collection_id, item_id=item_id
                    )
                    destination = _resolve_destination_path(destination_dir, relative_path)
                    destination.parent.mkdir(parents=True, exist_ok=True)

                    if destination.exists():
                        print(f"  Skipping existing file: {destination}")
                        skipped += 1
                        overall_bar.update(1)
                        continue

                    try:
                        with session.get(href, timeout=request_timeout, stream=True) as response:
                            response.raise_for_status()
                            content_length = response.headers.get("Content-Length")
                            total_size = int(content_length) if content_length else None

                            with tqdm(
                                total=total_size,
                                desc=asset_label,
                                unit="B",
                                unit_scale=True,
                                unit_divisor=1024,
                                dynamic_ncols=True,
                                position=1,
                                leave=False,
                            ) as file_bar:
                                with destination.open("wb") as fp:
                                    for chunk in response.iter_content(chunk_size=chunk_size):
                                        if not chunk:
                                            continue
                                        fp.write(chunk)
                                        file_bar.update(len(chunk))

                        successful += 1

                    except requests.RequestException as exc:
                        failed += 1
                        print(f"  Failed {asset_label}: {exc}")

                    finally:
                        overall_bar.update(1)

    finally:
        session.close()

    print("\nDownload complete")
    print(f"  Successful : {successful}")
    print(f"  Failed     : {failed}")
    print(f"  Skipped    : {skipped}")

    return {"total": total_assets, "successful": successful, "failed": failed, "skipped": skipped}
