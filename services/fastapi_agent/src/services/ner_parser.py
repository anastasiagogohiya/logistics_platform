# fastapi_agent/src/services/ner_parser.py
"""
Парсинг текста полученного из фронта.
Используется NER (Natasha) + словари для приведения к кодам моделей.
"""

import re
import logging
from typing import Dict, Any
from datetime import datetime
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)
from dateparser import parse as parse_date

logger = logging.getLogger(__name__)

# ---------- Инициализация компонентов ----------
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

# ---------- Словари для приведения к кодам моделей ----------
CARGO_TYPE_MAP = {
    'документы': 'documents',
    'документ': 'documents',
    'бумаги': 'documents',
    'посылка': 'package',
    'пакет': 'package',
    'коробка': 'package',
    'коробки': 'package',
    'паллет': 'pallet',
    'паллеты': 'pallet',
    'мебель': 'furniture',
    'диван': 'furniture',
    'шкаф': 'furniture',
    'стол': 'furniture',
    'стул': 'furniture',
    'автомобиль': 'vehicle',
    'машина': 'vehicle',
    'мотоцикл': 'vehicle',
    'опасный': 'hazmat',
    'взрывоопасный': 'hazmat',
    'химикаты': 'hazmat',
    'жидкость': 'liquid',
    'жидкости': 'liquid',
    'силос': 'liquid',
}
# Если ничего не найдено, по умолчанию будет 'other'

# ---------- Словарь для отображения (человекочитаемые названия) ----------
CARGO_NAME_MAP = {
    'documents': 'Документы',
    'package': 'Посылка',
    'pallet': 'Паллета',
    'furniture': 'Мебель',
    'vehicle': 'Автомобиль',
    'hazmat': 'Опасный груз',
    'liquid': 'Жидкость',
    'other': 'Другое',
}

DELIVERY_TYPE_MAP = {
    r'экспресс': 'express',
    r'срочн': 'express',
    r'быстр': 'express',
    r'стандарт': 'standard',
    r'обычн': 'standard',
    r'классич': 'standard',
}
# По умолчанию будет 'standard'

# ---------- Основная функция ----------
def extract_entities(text: str) -> Dict[str, Any]:
    """
    Принимает сырой текст пользователя и возвращает словарь с полями:
        ship_from       - город отправления (строка)
        ship_to         - город назначения (строка)
        cargo_type      - код типа груза (один из CargoChoice)
        delivery_type   - код типа доставки ('standard' или 'express')
        weight_kg       - вес в кг (float)
        dimensions      - габариты в формате "Д×Ш×В" (строка) или None
        quantity        - количество единиц груза (int) или None
        is_hazardous    - bool (опасный ли груз)
        shipment_date   - дата отгрузки в формате ISO (YYYY-MM-DD) или None
        confidence      - оценка уверенности (0..1) по критическим полям
    """
    logger.info(f"🔍 Парсим текст: {text[:100]}...")
    result = {
        "ship_from": None,
        "ship_to": None,
        "cargo_type": "other",
        "delivery_type": "standard",
        "weight_kg": None,
        "dimensions": None,
        "quantity": None,
        "is_hazardous": False,
        "shipment_date": None,
        "confidence": 0.0,
    }

    # ---------- 1. Прогон через Natasha ----------
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)
    doc.tag_ner(ner_tagger)

    logger.info(f"🔍 Все сущности от Natasha: {[(span.type, span.text) for span in doc.spans]}")
    entities = []
    for span in doc.spans:
        if span.type in ('LOC', 'DAT', 'NUM'):
            norm = span.normalize(morph_vocab) if span.type == 'LOC' else span.text
            if span.type == 'LOC' and norm is None:
                norm = span.text  # fallback
            entities.append({
                'type': span.type,
                'text': span.text,
                'start': span.start,
                'stop': span.stop,
                'normalized': norm
            })
    logger.info(f"✅ Отфильтрованные сущности (LOC, DAT, NUM): {entities}")

    # ---------- 2. Города (LOC) ----------
    locs = [e for e in entities if e['type'] == 'LOC']
    if locs:
        origin = None
        destination = None
        for loc in locs:
            # Используем нормализованную форму или исходный текст
            normalized = loc['normalized'] if loc['normalized'] is not None else loc['text']
            before = text[max(0, loc['start'] - 10):loc['start']]
            after = text[loc['stop']:min(len(text), loc['stop'] + 10)]
            if re.search(r'(из|от)\s*$', before, re.IGNORECASE):
                origin = normalized
                logger.debug(f"✅ Город отправления (предлог 'из/от'): {origin}")
            elif re.search(r'^(в|до)\s*', after, re.IGNORECASE):
                destination = normalized
                logger.debug(f"✅ Город назначения (предлог 'в/до'): {destination}")

        if not origin and not destination and len(locs) >= 2:
            origin = locs[0]['normalized'] or locs[0]['text']
            destination = locs[1]['normalized'] or locs[1]['text']
            logger.debug(f"🏙️ Города по порядку: {origin} -> {destination}")
        elif origin and not destination and len(locs) >= 2:
            for loc in locs:
                city = loc['normalized'] or loc['text']
                if city != origin and loc['start'] > locs[0]['start']:
                    destination = city
                    break
            logger.debug(f"🏙️ Дополнительное определение назначения: {destination}")

        # Присваиваем как есть (без дополнительной нормализации)
        result['ship_from'] = origin
        result['ship_to'] = destination
        logger.info(f"🏙️ Распознаны города: откуда='{result['ship_from']}', куда='{result['ship_to']}'")
    else:
        logger.warning("⚠️ Города не найдены")

    # ---------- 3. Дата ----------
    dates = [e for e in entities if e['type'] == 'DAT']
    if dates:
        date_str = dates[0]['text']
        parsed = parse_date(date_str, languages=['ru'])
        if parsed:
            result['shipment_date'] = parsed.date().isoformat()
            logger.info(f"📅 Дата из Natasha: {result['shipment_date']}")
    else:
        # Резерв: ДД.ММ.ГГГГ
        date_match = re.search(r'(\d{2}\.\d{2}\.\d{4})', text)
        if date_match:
            try:
                dt = datetime.strptime(date_match.group(1), "%d.%m.%Y")
                result['shipment_date'] = dt.date().isoformat()
                logger.info(f"📅 Дата по резервной регулярке: {result['shipment_date']}")
            except ValueError:
                logger.warning("⚠️ Не удалось распарсить дату из регулярки")
        else:
            logger.warning("⚠️ Дата не найдена")

    # ---------- 4. Вес ----------
    weight_match = re.search(r'(\d+[,.]?\d*)\s*(?:кг|килограмм|тонн|т)', text, re.IGNORECASE)
    if weight_match:
        result['weight_kg'] = float(weight_match.group(1).replace(',', '.'))
        logger.info(f"⚖️ Вес: {result['weight_kg']} кг")
    else:
        logger.warning("⚠️ Вес не найден")

    # ---------- 5. Тип груза (через словарь) ----------
    detected_cargo = None
    for keyword, code in CARGO_TYPE_MAP.items():
        if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
            detected_cargo = code
            logger.debug(f"Тип груза по ключевому слову '{keyword}' → {code}")
            break
    if not detected_cargo:
        cargo_phrase = re.search(
            r'(?:перевезти|перевези|доставить|отправить)\s+([А-Яа-яёЁ\s-]+?)(?:\s+из|\s+в|\s+от|\s+до|$)',
            text, re.IGNORECASE
        )
        if cargo_phrase:
            phrase = cargo_phrase.group(1).strip().lower()
            for keyword, code in CARGO_TYPE_MAP.items():
                if keyword in phrase:
                    detected_cargo = code
                    logger.debug(f"Тип груза из фразы '{phrase}' → {code}")
                    break
    result['cargo_type'] = detected_cargo or 'other'
    logger.info(f"📦 Тип груза: {result['cargo_type']}")

    # ---------- 6. Количество ----------
    qty_match = re.search(r'(\d+)\s*(?:шт|штук|короб|паллет|место|мест)', text, re.IGNORECASE)
    if qty_match:
        result['quantity'] = int(qty_match.group(1))
        logger.info(f"📦 Количество: {result['quantity']}")

    # ---------- 7. Габариты ----------
    dim_match = re.search(
        r'(\d+)\s*[хx×]\s*(\d+)\s*[хx×]\s*(\d+)(?:\s*см|\s*м)?',
        text, re.IGNORECASE
    )
    if dim_match:
        result['dimensions'] = f"{dim_match.group(1)}×{dim_match.group(2)}×{dim_match.group(3)}"
        logger.info(f"📐 Габариты: {result['dimensions']}")

    # ---------- 8. Опасный груз ----------
    hazardous_keywords = ['опасный', 'взрывоопасный', 'химикаты', 'огнеопасный', 'токсичный', 'радиоактивный']
    result['is_hazardous'] = any(kw in text.lower() for kw in hazardous_keywords)
    if result['cargo_type'] == 'hazmat':
        result['is_hazardous'] = True
    logger.info(f"⚠️ Опасный груз: {result['is_hazardous']}")

    # ---------- 9. Тип доставки ----------
    detected_delivery = None
    for pattern, code in DELIVERY_TYPE_MAP.items():
        if re.search(pattern, text, re.IGNORECASE):
            detected_delivery = code
            logger.debug(f"Тип доставки по шаблону '{pattern}' → {code}")
            break
    result['delivery_type'] = detected_delivery or 'standard'
    logger.info(f"🚚 Тип доставки: {result['delivery_type']}")

    # ---------- 10. Уверенность ----------
    critical = ['ship_from', 'ship_to', 'weight_kg', 'shipment_date']
    found = sum(1 for f in critical if result.get(f) is not None)
    result['confidence'] = found / len(critical)
    logger.info(f"📊 Уверенность: {result['confidence']:.2f}")

    logger.info(f"✅ Результат парсинга: {result}")
    return result