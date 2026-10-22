import csv, random, os
from datetime import datetime, timedelta

random.seed(42)
OUT = "powerbi_data"
os.makedirs(OUT, exist_ok=True)

def w(name, rows, header):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)

# ---------- carriers ----------
cities = ["Москва","Санкт-Петербург","Казань","Екатеринбург","Новосибирск",
          "Ростов-на-Дону","Краснодар","Самара","Воронеж","Мурманск",
          "Архангельск","Красноярск","Хабаровск","Владивосток"]
brands = ["Логистик","Транс","Карго","Экспресс","Доставка","Лайн","Фрахт","Груз","Перевозки","Сервис"]
prefixes = ["Альфа","Бета","Гамма","Дельта","Омега","Профи","Смарт","Юнион","Прайм","Макси"]

carriers = []
for i in range(1, 31):
    name = f"{random.choice(prefixes)}{random.choice(brands)}"
    legal = f'ООО "{name}"'
    inn = str(random.randint(1000000000, 9999999999))
    ogrn = str(random.randint(1000000000000, 9999999999999))
    city = random.choice(cities)
    rating = random.choice([2,3,3,4,4,4,5,5])
    active = random.random() > 0.15
    created = datetime(2024,1,1) + timedelta(days=random.randint(0,120))
    carriers.append([
        i, name, legal, "Россия", inn, ogrn, "",
        f"г. {city}, ул. Примерная, {random.randint(1,100)}",
        f"+7 {random.randint(900,999)} {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}",
        f"info{i}@carrier.ru", rating, active,
        created.strftime("%Y-%m-%d %H:%M:%S"),
        (created + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
    ])

w("carriers.csv", carriers, ["id","name","legal_name","country","inn","ogrn","reg_number",
    "address","phone","email","rating","is_active","created_at","updated_at"])

# ---------- users ----------
roles = ["client"]*45 + ["manager"]*10 + ["admin"]*2 + ["carrier"]*3
users = [[1, "admin", "admin@example.com", "+79000000001", "admin", True, "2024-01-01 08:00:00"]]
for i in range(2, 61):
    role = roles[i-2] if (i-2) < len(roles) else "client"
    users.append([
        i, f"user_{i}", f"user{i}@example.com", f"+7900{1000000+i}", role, True,
        (datetime(2024,1,1) + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
    ])
w("users.csv", users, ["id","username","email","phone","role","is_active","date_joined"])

client_ids = [u[0] for u in users if u[4] == "client"]

# ---------- tariffs ----------
cargo_types = ["documents","package","pallet","furniture","vehicle","hazmat","liquid","other"]
routes = [("Москва","Санкт-Петербург"),("Санкт-Петербург","Москва"),("Москва","Казань"),
          ("Москва","Екатеринбург"),("Екатеринбург","Москва"),("Санкт-Петербург","Мурманск"),
          ("Ростов-на-Дону","Москва"),("Москва","Ростов-на-Дону"),("Новосибирск","Москва"),
          ("Самара","Москва"),("Воронеж","Москва"),("Москва","Новосибирск"),
          ("Казань","Москва"),("Краснодар","Ростов-на-Дону"),("Мурманск","Санкт-Петербург")]

tariffs = []
tid = 1
for cid in range(1, 31):
    for _ in range(random.randint(2, 4)):
        frm, to = random.choice(routes)
        cts = random.sample(cargo_types, random.randint(1, 3))
        dt = random.choice(["standard","express"])
        wf = random.choice([0, 0, 100, 200, 500])
        wt = wf + random.choice([100, 500, 1000, 2000])
        price = round(random.uniform(1500, 25000), 2)
        per_kg = round(price / max(wt, 1), 2)
        dmin = random.randint(1, 5)
        dmax = dmin + random.randint(0, 3) if random.random() > 0.3 else None
        tariffs.append([
            tid, cid, frm, to, cts, wf, wt, dt, price, per_kg,
            dmin, dmax, random.random() > 0.1,
            "2024-01-15 10:00:00", "2024-06-01 12:00:00",
        ])
        tid += 1

w("tariffs.csv", tariffs, ["id","carrier_id","ship_from","ship_to","cargo_type",
    "cargo_weight_from","cargo_weight_to","delivery_type","price","price_per_kg",
    "delivery_days_min","delivery_days_max","is_active","created_at","updated_at"])

# ---------- orders ----------
order_statuses = ["created","assigned","in_transit","cancelled","delivered"]
statuses_weight = [0.12, 0.10, 0.10, 0.08, 0.60]

def gen_order(oid, created):
    cid = random.choice(client_ids)
    t = random.choice(tariffs)

    # t: [0]=id, [1]=carrier_id, [2]=ship_from, [3]=ship_to, [4]=cargo_type(list),
    #    [5]=weight_from, [6]=weight_to, [7]=delivery_type, [8]=price, [9]=price_per_kg,
    #    [10]=dmin, [11]=dmax, [12]=is_active
    cargo = random.choice(t[4])
    weight = round(random.uniform(0.5, 5000), 1)
    dims = f"{random.randint(20,600)}x{random.randint(15,300)}x{random.randint(5,250)}"
    qty = random.randint(1, 5)
    haz = cargo == "hazmat"

    assigned = random.random() > 0.30
    carrier_id = t[1] if assigned else ""
    tariff_id = t[0] if assigned else ""
    dt = t[7]
    price = round(float(t[8]) * random.uniform(0.9, 1.2), 2) if assigned else ""

    status = random.choices(order_statuses, weights=statuses_weight)[0] if assigned else "created"

    ship = created + timedelta(hours=random.randint(2, 48))
    dmin = t[10]
    dmax = t[11] or t[10]
    exp = ship + timedelta(days=random.randint(dmin, dmax)) if assigned else ""

    fact = ""
    if status == "delivered" and exp:
        fact = exp + timedelta(hours=random.randint(-36, 72))

    return [
        oid, f"ORD-2024-{oid:04d}", cid,
        created.strftime("%Y-%m-%d %H:%M:%S"),
        (created + timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d %H:%M:%S"),
        f"Заявка клиента #{oid}",
        cargo, weight, dims, qty, haz,
        t[2], t[3],
        ship.strftime("%Y-%m-%d %H:%M:%S"), dt,
        carrier_id, tariff_id, price, status,
        exp.strftime("%Y-%m-%d %H:%M:%S") if exp else "",
        fact.strftime("%Y-%m-%d %H:%M:%S") if fact else "",
    ]

orders = []
start = datetime(2024, 1, 15, 9, 0, 0)
for i in range(1, 301):
    created = start + timedelta(days=int(i/3), hours=random.randint(0,12), minutes=random.randint(0,59))
    orders.append(gen_order(i, created))

w("orders.csv", orders, ["id","order_number","client_id","created_at","updated_at","raw_data",
    "cargo_type","weight_kg","dimensions","quantity","is_hazardous","ship_from","ship_to",
    "shipment_date","delivery_type","carrier_id","tariff_id","price","order_status",
    "expected_delivery_date","factual_delivery_date"])

# ---------- payments ----------
payments = []
for o in orders:
    oid = o[0]
    amount = o[17] or round(random.uniform(1500, 15000), 2)
    method = random.choice(["prepaid","prepaid","prepaid","postpaid"])
    st = random.choices(["pending","paid","failed","refunded"], weights=[0.15,0.70,0.05,0.10])[0]
    created = o[3]
    paid = o[4] if st == "paid" else ""
    payments.append([
        oid, oid, method, st, float(amount), created,
        o[4], paid,
        f"PAY-{oid:06d}" if st == "paid" else "",
        f"https://pay.example.com/{oid}" if st == "pending" else "",
    ])

w("payments.csv", payments, ["id","order_id","method","status","amount","created_at",
    "updated_at","paid_at","payment_id","payment_url"])

print("Готово! CSV в папке:", OUT)