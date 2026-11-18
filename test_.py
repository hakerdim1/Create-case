#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор cases_50.json
50 кейсов × 20 предметов, цена кейса ниже минимум 55% (11+ из 20) предметов
"""

import json
import random
import sys

SEED = 20261117
rnd = random.Random(SEED)

# ─── 10 редкостей: ключ, имя, RGB-цвет, диапазон веса, диапазон цены ──────────
TIERS = [
    ("ordinary", "Обычный", [0.70, 0.70, 0.70, 1.0], (28.0, 42.0), (10, 100)),
    ("uncommon", "Необычный", [0.30, 0.80, 0.30, 1.0], (18.0, 26.0), (100, 500)),
    ("rare", "Редкий", [0.29, 0.41, 1.00, 1.0], (9.0, 15.0), (500, 3_000)),
    ("epic", "Эпический", [0.53, 0.27, 1.00, 1.0], (4.0, 7.0), (3_000, 15_000)),
    ("legendary", "Легендарный", [1.00, 0.84, 0.00, 1.0], (1.5, 3.0), (15_000, 60_000)),
    ("divine", "Божественный", [0.00, 1.00, 0.78, 1.0], (0.5, 1.2), (60_000, 200_000)),
    ("mythic", "Мифический", [1.00, 0.50, 0.00, 1.0], (0.15, 0.40), (200_000, 800_000)),
    ("ancient", "Древний", [0.92, 0.15, 0.15, 1.0], (0.04, 0.12), (800_000, 2_500_000)),
    ("eternal", "Вечный", [1.00, 0.20, 0.75, 1.0], (0.008, 0.025), (2_500_000, 10_000_000)),
    ("admin", "Админский", [1.00, 1.00, 1.00, 1.0], (0.0003, 0.0008), (50_000_000, 1_000_000_000)),
]

HIGH_TIERS = {"legendary", "divine", "mythic", "ancient", "eternal", "admin"}

# ─── Раскладка 20 предметов по редкостям ─────────────────────────────────────
COUNTS_NORMAL = {
    "ordinary": 7,
    "uncommon": 5,
    "rare": 4,
    "epic": 2,
    "legendary": 1,
    "divine": 1,
    "mythic": 0,
    "ancient": 0,
    "eternal": 0,
    "admin": 0,
}

COUNTS_ULTRA = {
    "ordinary": 5,
    "uncommon": 4,
    "rare": 3,
    "epic": 2,
    "legendary": 1,
    "divine": 1,
    "mythic": 1,
    "ancient": 1,
    "eternal": 1,
    "admin": 1,
}

assert sum(COUNTS_NORMAL.values()) == 20
assert sum(COUNTS_ULTRA.values()) == 20

# ─── Имена (разделены обычные пушки и ножи/перчатки) ──────────────────────────
GUNS = [
    "P250", "Glock-18", "MP9", "FAMAS", "Galil AR", "AWP", "USP-S", "AK-47",
    "M4A4", "M4A1-S", "AUG", "SSG 08", "Desert Eagle", "SCAR-20", "G3SG1",
    "MAC-10", "UMP-45", "XM1014", "Nova", "MAG-7", "Negev", "M249", "Five-SeveN",
    "Tec-9", "CZ75-Auto", "R8 Revolver", "PP-Bizon", "MP7", "MP5-SD", "SG 553",
]

KNIVES = [
    "★ Тычковые ножи", "★ Керамбит", "★ Нож-бабочка", "★ Перчатки",
    "★ Штык-нож", "★ Медвежий нож", "★ Складной нож", "★ M9 Bayonet",
]

SKINS = {
    "ordinary": ["Песчаные дюны", "Лайм", "Скромная угроза", "Синий глянец",
                 "Затерянная земля", "Магний", "Демонтаж", "Полимер",
                 "Городская угроза", "Пески", "Байкал", "Кобальт"],
    "uncommon": ["Изумрудные завитки", "Фобос", "Найтборд", "Хамелеон",
                 "Пыльник", "Сажа", "Волны", "Холодный синтез",
                 "Зелёный поток", "Малахит", "Хвоя", "Лесной камуфляж"],
    "rare": ["Капилляр", "Закрученный", "Лапки", "Нага",
             "Элитное снаряжение", "Неоновая революция", "Океан",
             "Голубой лёд", "Аквамарин", "Лазурь", "Небесный", "Сапфир"],
    "epic": ["Безлюдный космос", "Скоростной зверь", "Дамаск", "Мортис",
             "Неоар Нуар", "Император", "Пурпурный вихрь", "Аметист",
             "Фиалка", "Нексус", "Индиго", "Сумеречный"],
    "legendary": ["Снежный вихрь", "Вулканический", "Дикое пламя",
                  "История о драконе", "Золотая лихорадка", "Солнечный удар",
                  "Янтарный", "Медовый", "Корона", "Золото"],
    "divine": ["Гамма-волны", "Поток информации", "Чистая вода", "Мятные",
               "Бирюза", "Аура", "Дыхание океана", "Прилив", "Сирена", "Свет"],
    "mythic": ["Мифический зверь", "Огненный шторм", "Мандарин",
               "Коралловый", "Затмение", "Гелиос", "Феникс", "Титан"],
    "ancient": ["Кровь дракона", "Рубиновый", "Алый рассвет", "Багровый",
                "Ярость", "Древний ритуал", "Кармин", "Кровь"],
    "eternal": ["Вечная роза", "Магента", "Сакура", "Розовый кварц",
                "Неон-пурпур", "Фуксия", "Синтвейв", "Пурпурная дымка"],
    "admin": ["ADMIN | hakerdim1", "мелстрой | чекушка",
              "★ Легенда рынка", "★ Нулевой дроп", "★ Админ | Владыка",
              "★ Радужный призрак", "★ Абсолют", "★ Источник"],
}

# ─── Уровни кейсов (сумма = 50) ───────────────────────────────────────────────
CASE_TIERS = [
    ("standard", "Стандарт", 1, 35),
    ("prime", "Прайм", 3, 10),
    ("elite", "Элит", 10, 4),
    ("legendary", "Легендарный", 30, 1),
]

THEMES = ["Микс", "Оружейный склад", "Ночная смена", "Гамма", "Дракон", "Изумруд",
          "Вулкан", "Кибер", "Снег", "Пустыня", "Админ", "Хаос", "Легенды", "Пыль",
          "Неон", "Затмение", "Рубин", "Сапфир"]

ULTRA_CASES = {1, 11, 21, 31, 41}

# ─── Утилиты ────────────────────────────────────────────────────────────────
def nice_price(x):
    x = float(x)
    if x < 10:
        return int(round(x))
    if x < 1_00:
        return int(round(x / 5) * 5)
    if x < 10_00:
        return int(round(x / 50) * 50)
    if x < 100_00:
        return int(round(x / 100) * 100)
    if x < 1_000_00:
        return int(round(x / 1_000) * 1_000)
    if x < 100_000_00:
        return int(round(x / 10_000) * 10_000)
    return int(round(x / 1_000_00) * 1_000_00)

def pick_weapon(key):
    if key == "admin":
        return rnd.choice(KNIVES + ["AWP", "AK-47", "Desert Eagle"])
    if key in HIGH_TIERS:
        return rnd.choice(KNIVES) if rnd.random() < 0.6 else rnd.choice(["AWP", "AK-47", "M4A4", "M4A1-S", "Desert Eagle"])
    return rnd.choice(GUNS)

def unique_name(key, used):
    for _ in range(10_000):
        weapon = pick_weapon(key)
        skin = rnd.choice(SKINS[key])
        n = f"{weapon} | {skin}" if key != "admin" else skin
        if n not in used:
            used.add(n)
            return n
    n = f"{pick_weapon(key)} | {rnd.choice(SKINS[key])} #{len(used)+1}"
    used.add(n)
    return n

def calc_case_price(items):
    prices = sorted(i["price"] for i in items)
    target = prices[8] * 0.90
    if target < 100:
        return max(int(target // 5) * 5, 10)
    if target < 1_000:
        return int(target // 10) * 10
    if target < 10_000:
        return int(target // 50) * 50
    if target < 100_000:
        return int(target // 100) * 100
    return int(target // 500) * 500

# ─── Сборка одного кейса ────────────────────────────────────────────────────
def build_case(idx, tier_key, tier_ru, mult, is_ultra):
    counts = COUNTS_ULTRA if is_ultra else COUNTS_NORMAL
    items, used = [], set()
    for key, name_ru, color, w_rng, p_rng in TIERS:
        for _ in range(counts[key]):
            w = round(rnd.uniform(*w_rng), 8)
            p = nice_price(rnd.uniform(*p_rng) * mult)
            items.append({
                "name": unique_name(key, used),
                "price": p,
                "color": color,
                "tier": name_ru,
                "weight": w,
            })

    sum_w = sum(i["weight"] for i in items)
    for i in items:
        i["chance_percent"] = round(i["weight"] / sum_w * 100, 8)

    ev = sum(i["price"] * i["weight"] for i in items) / sum_w
    case_price = calc_case_price(items)
    theme = rnd.choice(THEMES)
    name = f"КЕЙС {idx:03d} | {tier_ru} | {theme}"
    return name, {
        "price": case_price,
        "desc": (f"{tier_ru} кейс #{idx:03d}" + (" [ULTRA]" if is_ultra else "")
                 + f". 20 предметов. EV≈{ev:.0f}. Шанс = weight/sum_weights×100%."),
        "items": items,
        "weights": [i["weight"] for i in items],
        "sum_weights": round(sum_w, 8),
        "expected_value": round(ev, 0),
        "tier": tier_key,
        "case_multiplier": mult,
        "is_ultra": is_ultra,
    }

# ─── Пул 50 кейсов ──────────────────────────────────────────────────────────
pool = []
for key, ru, mult, count in CASE_TIERS:
    pool.extend([(key, ru, mult)] * count)
rnd.shuffle(pool)
assert len(pool) == 50

cases = {}
for idx, (key, ru, mult) in enumerate(pool, start=1):
    n, c = build_case(idx, key, ru, mult, idx in ULTRA_CASES)
    cases[n] = c

# ─── Валидация ─────────────────────────────────────────────────────────────
errs = []
valid_tiers = {t[1] for t in TIERS}
for name, c in cases.items():
    if len(c["items"]) != 20:
        errs.append(f"{name}: items={len(c['items'])}")
    if abs(sum(c["weights"]) - c["sum_weights"]) > 1e-5:
        errs.append(f"{name}: sum_weights mismatch")
    if abs(sum(i["chance_percent"] for i in c["items"]) - 100) > 0.01:
        errs.append(f"{name}: chance_percent ≠ 100")
    more_expensive = sum(1 for i in c["items"] if i["price"] > c["price"])
    if more_expensive <= 10:
        errs.append(f"{name}: only {more_expensive}/20 items > case price ({c['price']})")
    for i in c["items"]:
        if i["tier"] not in valid_tiers:
            errs.append(f"{name}: bad tier {i['tier']}")

if errs:
    print("ОШИБКИ ВАЛИДАЦИИ:", file=sys.stderr)
    for e in errs[:20]:
        print(" ", e, file=sys.stderr)
    sys.exit(1)

# ─── Запись ────────────────────────────────────────────────────────────────
with open("cases_50.json", "w", encoding="utf-8") as f:
    json.dump(cases, f, ensure_ascii=False, indent=2)

print("✔ cases_50.json готов")
print(f" Кейсов: {len(cases)}")
print(f" Предметов: {sum(len(c['items']) for c in cases.values())}")
print(f" Ultra-кейсов: {sum(1 for c in cases.values() if c['is_ultra'])}")
print(f" Размер файла: ~{len(json.dumps(cases, ensure_ascii=False))//1024} КБ")
