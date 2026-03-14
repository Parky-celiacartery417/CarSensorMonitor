"""HTML parser for CarSensor.net listing pages.

Extracts structured car data from listing page HTML using BeautifulSoup.
Prices on CarSensor are in 万円 (10,000 yen units).
Images use lazy loading with data-original attribute.
"""

import logging
import re

from bs4 import BeautifulSoup, Tag

from app.scraper.translator import (
    translate_body_type,
    translate_color,
    translate_fuel_type,
    translate_maker,
    translate_transmission,
)

logger = logging.getLogger(__name__)


def parse_price(main_el: Tag | None, sub_el: Tag | None) -> int | None:
    """Convert 万円 price parts to yen. E.g. '219' + '.8' = 2,198,000."""
    if main_el is None:
        return None
    try:
        main_text = main_el.get_text(strip=True).replace(",", "")
        sub_text = sub_el.get_text(strip=True) if sub_el else ""

        if not main_text or main_text == "---" or main_text == "応談":
            return None

        combined = main_text + sub_text
        value = float(combined)
        return int(value * 10_000)
    except (ValueError, TypeError):
        return None


def parse_mileage(text: str | None) -> int | None:
    """Parse mileage text like '3.5万km' to km integer (35000)."""
    if not text:
        return None
    text = text.strip()
    if text in ("---", "不明"):
        return None
    try:
        match = re.search(r"([\d.]+)\s*万\s*km", text)
        if match:
            return int(float(match.group(1)) * 10_000)
        match = re.search(r"([\d,]+)\s*km", text)
        if match:
            return int(match.group(1).replace(",", ""))
    except (ValueError, TypeError):
        pass
    return None


def parse_displacement(text: str | None) -> int | None:
    """Parse displacement text like '2000cc' to integer."""
    if not text:
        return None
    try:
        match = re.search(r"([\d,]+)\s*cc", text, re.IGNORECASE)
        if match:
            return int(match.group(1).replace(",", ""))
    except (ValueError, TypeError):
        pass
    return None


def parse_year(text: str | None) -> int | None:
    """Parse year from spec text like '2025' or '令和7年'."""
    if not text:
        return None
    try:
        match = re.search(r"(19|20)\d{2}", text)
        if match:
            return int(match.group(0))
    except (ValueError, TypeError):
        pass
    return None


def extract_carsensor_id(href: str | None) -> str | None:
    """Extract listing ID from detail URL like /usedcar/detail/AU1234567890/index.html."""
    if not href:
        return None
    match = re.search(r"/detail/([A-Z]{2}\d+)/", href)
    if match:
        return match.group(1)
    return None


def parse_listing_page(html: str, base_url: str = "https://www.carsensor.net") -> list[dict]:
    """Parse a CarSensor listing page and return list of car data dicts."""
    soup = BeautifulSoup(html, "lxml")
    cars = []

    cassettes = soup.select("div.cassetteWrap")
    if not cassettes:
        cassettes = soup.select("div.cassette")

    for cassette in cassettes:
        try:
            car = parse_cassette(cassette, base_url)
            if car and car.get("carsensor_id"):
                cars.append(car)
        except Exception as e:
            logger.warning(f"Failed to parse cassette: {e}")
            continue

    logger.info(f"Parsed {len(cars)} cars from listing page")
    return cars


def parse_cassette(cassette: Tag, base_url: str) -> dict | None:
    """Parse a single car cassette element into a data dict."""
    # Detail link and ID
    title_link = cassette.select_one("h3.cassetteMain__title a")
    if not title_link:
        return None

    href = title_link.get("href", "")
    carsensor_id = extract_carsensor_id(href)
    if not carsensor_id:
        # Try from cassette id attribute
        cassette_inner = cassette.select_one("div.cassette") or cassette
        cid = cassette_inner.get("id", "")
        if "_cas" in cid:
            carsensor_id = cid.replace("_cas", "")

    if not carsensor_id:
        return None

    detail_url = f"{base_url}{href}" if href.startswith("/") else href

    # Title = model name
    title_text = title_link.get_text(strip=True)

    # Maker name - first <p> in carInfoContainer
    maker_ja = None
    info_container = cassette.select_one("div.cassetteMain__carInfoContainer")
    if info_container:
        first_p = info_container.find("p", recursive=False)
        if first_p:
            maker_ja = first_p.get_text(strip=True)

    maker = translate_maker(maker_ja) or maker_ja

    # Image
    img_el = cassette.select_one("div.cassetteMain__mainImg img")
    image_url = None
    if img_el:
        image_url = img_el.get("data-original") or img_el.get("src")
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

    # Prices
    total_price = parse_price(
        cassette.select_one("span.totalPrice__mainPriceNum"),
        cassette.select_one("span.totalPrice__subPriceNum"),
    )
    body_price = parse_price(
        cassette.select_one("span.basePrice__mainPriceNum"),
        cassette.select_one("span.basePrice__subPriceNum"),
    )

    # Body type and color from carBodyInfoList
    body_type_ja = None
    color_ja = None
    body_info_items = cassette.select("ul.carBodyInfoList li.carBodyInfoList__item")
    if len(body_info_items) >= 1:
        body_type_ja = body_info_items[0].get_text(strip=True)
    if len(body_info_items) >= 2:
        color_text = body_info_items[1].get_text(strip=True)
        color_ja = color_text

    # Specs from specList
    specs = {}
    spec_boxes = cassette.select("dl.specList div.specList__detailBox")
    for box in spec_boxes:
        dt = box.select_one("dt.specList__title")
        dd = box.select_one("dd.specList__data")
        if dt and dd:
            label = dt.get_text(strip=True)
            value = dd.get_text(strip=True)
            specs[label] = value

    # Parse individual specs
    year = parse_year(specs.get("年式"))
    mileage_km = parse_mileage(specs.get("走行距離"))
    displacement_cc = parse_displacement(specs.get("排気量"))

    transmission_ja = specs.get("ミッション")
    transmission = translate_transmission(transmission_ja)

    inspection_expiry = specs.get("車検")
    repair_history = specs.get("修復歴")

    fuel_type_ja = specs.get("燃料")
    fuel_type = translate_fuel_type(fuel_type_ja)

    # Dealer info
    dealer_name = None
    dealer_location = None
    shop_el = cassette.select_one("div.cassetteSub__shop a")
    if shop_el:
        dealer_name = shop_el.get_text(strip=True)
    area_el = cassette.select_one("div.cassetteSub__area")
    if area_el:
        dealer_location = area_el.get_text(strip=True).replace("\n", " ").strip()

    return {
        "carsensor_id": carsensor_id,
        "maker": maker or "Unknown",
        "maker_ja": maker_ja,
        "model": title_text or "Unknown",
        "model_ja": title_text,
        "grade": None,
        "body_type": translate_body_type(body_type_ja),
        "year": year,
        "mileage_km": mileage_km,
        "total_price_yen": total_price,
        "body_price_yen": body_price,
        "displacement_cc": displacement_cc,
        "transmission": transmission,
        "fuel_type": fuel_type,
        "drive_type": None,
        "color": translate_color(color_ja),
        "color_ja": color_ja,
        "inspection_expiry": inspection_expiry,
        "repair_history": repair_history,
        "dealer_name": dealer_name,
        "dealer_location": dealer_location,
        "image_url": image_url,
        "detail_url": detail_url,
    }


def parse_total_pages(html: str) -> int:
    """Extract total number of pages from pagination."""
    soup = BeautifulSoup(html, "lxml")
    pager = soup.select_one("div.pager")
    if not pager:
        return 1

    # Find the "最後" (last) link
    last_link = None
    for a in pager.select("a"):
        if "最後" in a.get_text():
            last_link = a
            break

    if last_link:
        href = last_link.get("href", "")
        match = re.search(r"index(\d+)\.html", href)
        if match:
            return int(match.group(1))

    # Fallback: find highest page number link
    max_page = 1
    for a in pager.select("a.js-carListBottomPagerBtn"):
        text = a.get_text(strip=True)
        if text.isdigit():
            max_page = max(max_page, int(text))

    return max_page
