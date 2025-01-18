import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_data (
                Material TEXT,
                BaseRate REAL,
                MaintenanceRate REAL,
                RepairRate REAL,
                DemolitionRate REAL,
                EnvironmentalFactor REAL,
                SocialFactor REAL,
                DelayFactor REAL
            )
        """)

        self.cursor.execute("SELECT COUNT(*) FROM cost_data")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany("""
                INSERT INTO cost_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                ("Steel", 3000, 50, 200, 100, 10, 0.5, 0.3),
                ("Concrete", 2500, 75, 150, 80, 8, 0.6, 0.2)
            ])
            self.conn.commit()

    def fetch_all_cost_data(self):
        self.cursor.execute("SELECT * FROM cost_data")
        return self.cursor.fetchall()