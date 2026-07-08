import sqlite3
import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect("db/nifty100.db")

        self.df = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        with open(
            "config/screener_config.yaml",
            "r"
        ) as file:

            self.config = yaml.safe_load(file)

    def get_data(self):

        return self.df.copy()

    def get_preset(self, preset_name):

        if preset_name not in self.config:

            raise ValueError(
                f"{preset_name} not found."
            )

        return self.config[preset_name]

    def close(self):

        self.conn.close()


if __name__ == "__main__":

    engine = ScreenerEngine()

    print("Rows Loaded:", len(engine.df))

    print("\nAvailable Presets:")

    for preset in engine.config:

        print("-", preset)

    engine.close()