import sqlite3
import os

def heal():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print("Error: db.sqlite3 not found! Make sure you run this script in the Django project root folder containing the db.sqlite3 file.")
        return

    print("Connecting to database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of all tables currently in the DB
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables currently in DB:", tables)

    # 1. Handle product image table rename if not already done
    if 'shop_productimage' in tables:
        if 'shop_jewelleryimage' in tables:
            print("Renaming old shop_jewelleryimage to shop_jewelleryimage_old_backup...")
            cursor.execute("ALTER TABLE shop_jewelleryimage RENAME TO shop_jewelleryimage_old_backup;")
        print("Renaming shop_productimage to shop_jewelleryimage...")
        cursor.execute("ALTER TABLE shop_productimage RENAME TO shop_jewelleryimage;")
        # update tables list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

    # 2. Handle product table rename if not already done
    if 'shop_product' in tables:
        if 'shop_jewellery' in tables:
            print("Renaming old shop_jewellery to shop_jewellery_old_backup...")
            cursor.execute("ALTER TABLE shop_jewellery RENAME TO shop_jewellery_old_backup;")
        print("Renaming shop_product to shop_jewellery...")
        cursor.execute("ALTER TABLE shop_product RENAME TO shop_jewellery;")
        # update tables list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

    # 3. Check for and add any missing columns in the product table (shop_jewellery)
    if 'shop_jewellery' in tables:
        cursor.execute("PRAGMA table_info(shop_jewellery);")
        cols = [c[1] for c in cursor.fetchall()]
        print("Columns in shop_jewellery table:", cols)

        missing_columns = {
            'occasion': 'VARCHAR(100) NULL',
            'collection': 'VARCHAR(100) NULL',
            'color': 'VARCHAR(20) NULL',
            'gold_value': 'DECIMAL NULL',
            'silver_value': 'DECIMAL NULL',
            'platinum_value': 'DECIMAL NULL',
            'stone_value': 'DECIMAL NULL',
            'making_charges': 'DECIMAL NULL',
            'gst': 'DECIMAL NULL',
            'is_manual_price': 'BOOLEAN DEFAULT 0',
            'total_price': 'DECIMAL DEFAULT 0',
            'in_stock': 'BOOLEAN DEFAULT 1',
            'platinum_purity': 'VARCHAR(10) NULL',
            'platinum_weight': 'DECIMAL NULL',
            'silver_purity': 'VARCHAR(20) NULL',
            'silver_weight': 'DECIMAL NULL',
            'stone_type': 'VARCHAR(20) NULL',
            'is_featured': 'BOOLEAN DEFAULT 0',
            'badge': 'VARCHAR(20) NULL',
            'diamond_weight': 'DECIMAL NULL',
            'diamond_clarity': 'VARCHAR(50) NULL',
            'diamond_color': 'VARCHAR(50) NULL',
            'gold_purity': 'VARCHAR(10) NULL',
            'gold_weight': 'DECIMAL NULL',
        }

        for col_name, col_type in missing_columns.items():
            if col_name not in cols:
                print(f"Adding column '{col_name}' to shop_jewellery...")
                try:
                    cursor.execute(f"ALTER TABLE shop_jewellery ADD COLUMN {col_name} {col_type};")
                except Exception as e:
                    print(f"Error adding column {col_name}: {e}")
        
        print("Database schema successfully healed!")
    else:
        print("Error: shop_jewellery table not found and could not be resolved from shop_product.")

    conn.commit()
    conn.close()
    print("Done! Database is now aligned with Django models.")

if __name__ == '__main__':
    heal()
