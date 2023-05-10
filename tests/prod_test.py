#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from pathlib import Path
import sqlite3
import pytest
from ind import create_db, add_product, select_all, select_by_shop


class TestProd:
    """
    Тест программы для списка продуктов
    """

    def test_create_db(self):
        """
        Проверка создания БД.
        """
        database_path = "test.db"
        if Path(database_path).exists():
            Path(database_path).unlink()

        create_db(database_path)
        assert Path(database_path).is_file()
        Path(database_path).unlink()


    def test_add_product(self):
        """
        Проверка добавления записи о товаре.
        """
        database_path = "test.db"
        create_db(database_path)
        add_product(database_path, 'молоко', 'пятерочка', 55.9)
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM prods
            """
        )
        row = cursor.fetchone()
        assert row == (1, 'молоко', 1, 55.9)
        conn.close()
        Path(database_path).unlink()


    def test_select_all(self):
        """
        Проверка выбора всего списка
        """
        database_path = "test.db"
        create_db(database_path)
        add_product(database_path, 'хлеб', 'магнит', 30.0)
        add_product(database_path, 'ноутбук', 'ситилинк', 50000.0)
        add_product(database_path, 'макароны', 'магнит', 44.4)

        r_output = [
            {'prod': 'хлеб', 'shop': 'магнит', 'cost': 30.0},
            {'prod': 'ноутбук', 'shop': 'ситилинк', 'cost': 50000.0},
            {'prod': 'макароны', 'shop': 'магнит', 'cost': 44.4}
        ]
        assert select_all(database_path) == r_output
        Path(database_path).unlink()


    def test_select_by_shop(self):
        """
        Проверка выбора товаров из одного магазина
        """
        database_path = "test.db"
        create_db(database_path)
        add_product(database_path, 'хлеб', 'магнит', 30.0)
        add_product(database_path, 'ноутбук', 'ситилинк', 50000.0)
        add_product(database_path, 'макароны', 'магнит', 44.4)
        r_output = [
            {'prod': 'хлеб', 'shop': 'магнит', 'cost': 30.0},
            {'prod': 'макароны', 'shop': 'магнит', 'cost': 44.4}
        ]
        assert select_by_shop(database_path, 'магнит') == r_output
        Path(database_path).unlink()