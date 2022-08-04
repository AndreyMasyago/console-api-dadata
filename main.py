from dadata import Dadata

import json
import sqlite3


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


class Klass:
    def __init__(self):
        self.id = 0
        self.value = ""
        self.unrestricted_value = ""

    def print(self):
        print("=====       ", self.id, "        =====")
        print("value: ", self.value)
        print("unrestricted_value: ", self.unrestricted_value)


if __name__ == '__main__':
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()

    #
    #
    cursor.execute("""DROP TABLE IF EXISTS settings
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS settings(
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        apikey TEXT DEFAULT 'c8c03d3a7321ea0ba36ebe1e46de06b7083d9d5e' NOT NULL,
        language TEXT DEFAULT ru NOT NULL
        );   
    """)
    conn.commit()

    cursor.execute("""INSERT INTO settings(url) VALUES('url');
    """)
    conn.commit()

    cursor.execute("SELECT * FROM settings;")
    conn.commit()

    cur_settings = cursor.fetchone()
    print("settings")
    print(cur_settings)


    token = "c8c03d3a7321ea0ba36ebe1e46de06b7083d9d5e"
    dadata = Dadata(token)

    # print("balans = ", dadata.get_balance())


    print("Che nada")
    # query = input()
    query = "Николаева 2 2"

    result = dadata.suggest("address", query, 3)

    # result = dadata.suggest("https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address", query, 3)

    print(len(result), "results\n")

    jsonString = json.dumps(result)

    parsed = json.loads(jsonString)

    dict_supa_parsed = dict()

    obj = Klass()
    j = 0
    for p in result:
        tmp_obj = Klass()
        tmp_obj.value = p.get('value')
        tmp_obj.unrestricted_value = p.get('unrestricted_value')
        tmp_obj.id = j

        dict_supa_parsed[j] = tmp_obj
        j = j + 1

    print()
    print("DICT")

    for key in dict_supa_parsed:
        print("=====       ", key, "        =====")
        print("value: ", dict_supa_parsed[key].value)
        print("unrestricted_value: ", dict_supa_parsed[key].unrestricted_value)

    print()

    print("Выбери чё-нить. Ну.")
    # asked = input()

    asked = 2
    asked = safe_cast(asked, int)

    # safe_cast('tst', int) # will return None
    # safe_cast('tst', int, 0) # will return 0

    while asked is None or dict_supa_parsed.get(asked) is None:
        print("Choose from [ 0 - ", len(dict_supa_parsed) - 1, "] array.")
        # asked = input()
        asked = 2
        asked = safe_cast(asked, int)

    # ПОЛУЧИЛИ ТОЧНЫЙ ЗАПРОС

    print("Запросили", asked)
    query = dict_supa_parsed[asked].unrestricted_value

    result2 = dadata.suggest("address", query, 1)

    print(result2[0]['data']['geo_lat'])
    print(result2[0]['data']['geo_lon'])
