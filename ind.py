#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
import typing as t
from pathlib import Path


def product_list(products: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Вывод списка товаров
    """
    if products:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20
        )
        print(line)
        print(
            '| {:^25} | {:^15} | {:^14} |'.format(
                "Товар",
                "Магазин",
                "Стоимость"
            )
        )
        print(line)

        for product in products:
            print(
                '| {:^25} | {:^15} | {:^14} |'.format(
                    product.get('prod', ''),
                    product.get('shop', ''),
                    product.get('cost', 0)
                )
            )
            print(line)

    else:
        print("Список продуктов пуст.")


def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
       """
       CREATE TABLE IF NOT EXISTS shops(
           shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
           shop_title TEXT NOT NULL
       )
       """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prods(
            prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_name TEXT NOT NULL,
            shop_id INTEGER NOT NULL,
            prod_cost REAL NOT NULL,
            FOREIGN KEY(shop_id) REFERENCES shops(shop_id)
        )
        """
    )
    conn.close()


def add_product(
        database_path: Path,
        name: str,
        shop: str,
        cost: float
) -> None:
    """
    Ввод информации о товарах.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT shop_id FROM shops WHERE shop_title = ? 
        """,
        (shop,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO shops (shop_title) VALUES (?)
            """,
            (shop,)
        )
        shop_id = cursor.lastrowid
    else:
        shop_id = row[0]

    cursor.execute(
        """
        INSERT INTO prods (prod_name, shop_id, prod_cost)
        VALUES(?, ?, ?)
        """,
        (name, shop_id, cost)
    )
    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать все продукты.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT prods.prod_name, shops.shop_title, prods.prod_cost
        FROM prods
        INNER JOIN shops ON shops.shop_id = prods.shop_id
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return [
        {
            "prod": row[0],
            "shop": row[1],
            "cost": row[2],
        }
        for row in rows
    ]


def select_by_shop(
        database_path: Path, shop: str
) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать товары из конкретного магазина.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT prods.prod_name, shops.shop_title, prods.prod_cost
        FROM prods
        INNER JOIN shops ON shops.shop_id = prods.shop_id
        WHERE shops.shop_title == ?
        """,
        (shop,)
    )
    rows = cursor.fetchall()

    conn.close()
    return [
        {
            "prod": row[0],
            "shop": row[1],
            "cost": row[2]
        }
        for row in rows
    ]


def main(command_line=None):
    """
    Главная функция программы.
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "products.db"),
        help="Имя файла базы данных"
    )

    parser = argparse.ArgumentParser("products")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.1"
    )
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Добавить новый продукт"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Название продукта"
    )
    add.add_argument(
        "-s",
        "--shop",
        action="store",
        help="Название магазина"
    )
    add.add_argument(
        "-c",
        "--cost",
        action="store",
        type=float,
        required=True,
        help="Стоимость товара"
    )

    list = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Отобразить список товаров"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Выбрать товары из магазина"
    )
    select.add_argument(
        "-s",
        "--shop",
        action="store",
        type=str,
        required=True,
        help="Название магазина"
    )

    args = parser.parse_args(command_line)

    db_path = Path(args.db)
    create_db(db_path)

    if args.command == "add":
        add_product(db_path, args.name, args.shop, args.cost)

    elif args.command == "list":
        product_list(select_all(db_path))

    elif args.command == "select":
        product_list(select_by_shop(db_path, args.shop))


if __name__ == '__main__':
    main()
