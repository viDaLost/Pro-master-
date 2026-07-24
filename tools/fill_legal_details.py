#!/usr/bin/env python3
"""Заполняет юридические реквизиты в статических HTML-файлах сайта."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {
    '[[FULL_LEGAL_NAME]]': 'Полное наименование организации или ФИО исполнителя',
    '[[LEGAL_STATUS]]': 'Статус (ИП / ООО / физлицо — плательщик НПД)',
    '[[INN]]': 'ИНН',
    '[[OGRN]]': 'ОГРН/ОГРНИП (или «не применяется»)',
    '[[REGISTRATION_AUTHORITY]]': 'Орган регистрации (или «не применяется»)',
    '[[LEGAL_ADDRESS]]': 'Адрес места нахождения / адрес для обращений',
    '[[LEGAL_EMAIL]]': 'Электронная почта',
    '[[HOSTING_PROVIDER]]': 'Российский хостинг-провайдер',
    '[[HOSTING_LOCATION_RU]]': 'Город/регион размещения серверов в РФ',
    '[[RKN_NOTIFICATION_STATUS]]': 'Статус уведомления РКН',
    '[[RKN_REGISTRY_NUMBER]]': 'Номер в реестре операторов или «уточняется»',
}

def main():
    values = {}
    print('Заполнение реквизитов ProДЕРЕVO. Вводите только достоверные сведения.\n')
    for token, label in FIELDS.items():
        while True:
            value = input(f'{label}: ').strip()
            if value:
                values[token] = value
                break
            print('Поле не должно быть пустым.')
    files = [ROOT/'index.html', ROOT/'legal.html', ROOT/'privacy.html']
    for path in files:
        text = path.read_text(encoding='utf-8')
        for token, value in values.items():
            text = text.replace(token, value)
        path.write_text(text, encoding='utf-8')
        print(f'Обновлён: {path.name}')
    remaining = []
    for path in files:
        text = path.read_text(encoding='utf-8')
        remaining.extend((path.name, token) for token in re.findall(r'\[\[[A-Z0-9_]+\]\]', text))
    if remaining:
        print('Внимание: остались незаполненные токены:', remaining)
        raise SystemExit(1)
    print('\nГотово. Запустите: python tools/check_compliance.py')

if __name__ == '__main__':
    main()
