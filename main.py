from dadata import Dadata

import json
import sqlite3
import logging


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

    testing_marker = True

    if testing_marker:
        # TEST usage only. Delete before real using. Dropping and creating settings table
        try:
            drop_table_query = "DROP TABLE IF EXISTS settings"
            cursor.execute(drop_table_query)
            conn.commit()

    # TODO: apikey NOT NULL ?
            create_table_query = "CREATE TABLE IF NOT EXISTS settings(\
                userid INTEGER PRIMARY KEY AUTOINCREMENT,\
                url TEXT DEFAULT 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address' NOT NULL,\
                apikey TEXT,\
                language TEXT DEFAULT ru NOT NULL\
                );\
            "
            cursor.execute(create_table_query)
            conn.commit()
        except sqlite3.Error as err:
            logging.exception("Error occurred while recreating settings table")

        try:
            fill_table_query = "INSERT INTO settings(url) VALUES('url');"
            cursor.execute(fill_table_query)
            conn.commit()
        except sqlite3.Error as err:
            logging.exception("Error occurred while filling settings table")

    try:
        select_everything_from_settings_table_query = "SELECT * FROM settings;"
        cursor.execute(select_everything_from_settings_table_query)
        conn.commit()
        cur_settings = cursor.fetchone()
        print("settings")
        print(cur_settings)
        print()
    except sqlite3.Error as err:
        logging.exception("Error occurred while selecting from settings table")

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
