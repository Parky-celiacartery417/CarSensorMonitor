"""Japanese-to-English dictionary for CarSensor data normalization.

Extensible mapping module — add new entries as they're discovered during scraping.
"""

MAKERS: dict[str, str] = {
    "トヨタ": "Toyota",
    "ホンダ": "Honda",
    "日産": "Nissan",
    "マツダ": "Mazda",
    "スバル": "Subaru",
    "スズキ": "Suzuki",
    "ダイハツ": "Daihatsu",
    "三菱": "Mitsubishi",
    "レクサス": "Lexus",
    "いすゞ": "Isuzu",
    "光岡": "Mitsuoka",
    "日野": "Hino",
    "メルセデス・ベンツ": "Mercedes-Benz",
    "BMW": "BMW",
    "アウディ": "Audi",
    "フォルクスワーゲン": "Volkswagen",
    "ポルシェ": "Porsche",
    "ボルボ": "Volvo",
    "ジャガー": "Jaguar",
    "ランドローバー": "Land Rover",
    "フェラーリ": "Ferrari",
    "ランボルギーニ": "Lamborghini",
    "マセラティ": "Maserati",
    "アルファロメオ": "Alfa Romeo",
    "フィアット": "Fiat",
    "プジョー": "Peugeot",
    "シトロエン": "Citroen",
    "ルノー": "Renault",
    "MINI": "MINI",
    "ジープ": "Jeep",
    "クライスラー": "Chrysler",
    "シボレー": "Chevrolet",
    "フォード": "Ford",
    "キャデラック": "Cadillac",
    "テスラ": "Tesla",
    "ヒョンデ": "Hyundai",
}

BODY_TYPES: dict[str, str] = {
    "セダン": "Sedan",
    "ハッチバック": "Hatchback",
    "ワゴン": "Wagon",
    "クーペ": "Coupe",
    "オープン": "Convertible",
    "SUV・クロカン": "SUV",
    "ミニバン": "Minivan",
    "コンパクトカー": "Compact",
    "軽自動車": "Kei Car",
    "ステーションワゴン": "Station Wagon",
    "ピックアップトラック": "Pickup Truck",
    "バン": "Van",
    "トラック": "Truck",
    "バス": "Bus",
    "キャンピングカー": "Camper",
    "福祉車両": "Welfare Vehicle",
}

COLORS: dict[str, str] = {
    "ホワイト": "White",
    "白": "White",
    "ブラック": "Black",
    "黒": "Black",
    "シルバー": "Silver",
    "グレー": "Gray",
    "レッド": "Red",
    "赤": "Red",
    "ブルー": "Blue",
    "青": "Blue",
    "グリーン": "Green",
    "緑": "Green",
    "イエロー": "Yellow",
    "黄": "Yellow",
    "オレンジ": "Orange",
    "ブラウン": "Brown",
    "茶": "Brown",
    "ベージュ": "Beige",
    "ゴールド": "Gold",
    "金": "Gold",
    "パープル": "Purple",
    "紫": "Purple",
    "ピンク": "Pink",
    "ワインレッド": "Wine Red",
    "ガンメタリック": "Gunmetal",
    "パール": "Pearl White",
    "ホワイトパール": "Pearl White",
    "ライトブルー": "Light Blue",
    "ダークブルー": "Dark Blue",
    "ライトグリーン": "Light Green",
    "ダークグリーン": "Dark Green",
}

TRANSMISSIONS: dict[str, str] = {
    "AT": "AT",
    "MT": "MT",
    "CVT": "CVT",
    "インパネAT": "AT",
    "インパネCVT": "CVT",
    "コラムAT": "AT",
    "フロアAT": "AT",
    "フロアMT": "MT",
    "フロアCVT": "CVT",
    "セミAT": "Semi-AT",
}

FUEL_TYPES: dict[str, str] = {
    "ガソリン": "Gasoline",
    "軽油": "Diesel",
    "ハイブリッド": "Hybrid",
    "電気": "Electric",
    "LPG": "LPG",
    "CNG": "CNG",
}

DRIVE_TYPES: dict[str, str] = {
    "2WD": "2WD",
    "4WD": "4WD",
    "FF": "FF",
    "FR": "FR",
    "MR": "MR",
    "RR": "RR",
    "AWD": "AWD",
}

SPEC_LABELS: dict[str, str] = {
    "年式": "year",
    "走行距離": "mileage",
    "排気量": "displacement",
    "車検": "inspection",
    "修復歴": "repair_history",
    "ミッション": "transmission",
    "燃料": "fuel_type",
    "駆動": "drive_type",
    "ハンドル": "steering",
    "色": "color",
    "ドア数": "doors",
    "定員": "capacity",
}


def translate(value: str | None, dictionary: dict[str, str]) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return dictionary.get(value, value)


def translate_maker(ja: str | None) -> str | None:
    return translate(ja, MAKERS)


def translate_color(ja: str | None) -> str | None:
    return translate(ja, COLORS)


def translate_body_type(ja: str | None) -> str | None:
    return translate(ja, BODY_TYPES)


def translate_transmission(ja: str | None) -> str | None:
    return translate(ja, TRANSMISSIONS)


def translate_fuel_type(ja: str | None) -> str | None:
    return translate(ja, FUEL_TYPES)


def translate_drive_type(ja: str | None) -> str | None:
    return translate(ja, DRIVE_TYPES)
