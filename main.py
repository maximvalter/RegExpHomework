import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    contacts = list(csv.reader(f))
header = contacts[0]

# Регулярка для телефонов
phone_re = re.compile(
    r"(?:\+7|8)\s*\(?(?P<code>\d{3})\)?[\s-]?"
    r"(?P<p1>\d{3})[\s-]?(?P<p2>\d{2})[\s-]?(?P<p3>\d{2})"
    r"(?:\s*\(?(?:доб\.?)\s*(?P<ext>\d+)\)?)?")

people = {}

for row in contacts[1:]:
    # Упорядочивание ФИО
    fio = " ".join(row[:3]).split()
    last, first, sur = (fio + ["", "", ""])[:3]
    # Упорядочивание телефона
    phone = phone_re.sub(lambda m: f"+7({m['code']}){m['p1']}-{m['p2']}-{m['p3']}" + (f" доб.{m['ext']}" if m['ext'] else ""), row[5])
    # Объединение дублей
    key = (last, first)
    data = [last, first, sur, row[3], row[4], phone, row[6]]
    if key in people:
        people[key] = [a or b for a, b in zip(people[key], data)]
    else:
        people[key] = data

with open("phonebook.csv", "w", encoding="cp1251", newline="") as f:
    csv.writer(f, delimiter=";").writerows([header] + list(people.values()))
