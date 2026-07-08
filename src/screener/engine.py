import sqlite3
import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(self):

        # Connect SQLite
        self.conn = sqlite3.connect(
            "db/nifty100.db"
        )

        # Load financial ratios
        self.df = pd.read_sql(
            """
            SELECT
                fr.*,
                s.broad_sector
            FROM financial_ratios fr
            LEFT JOIN sectors s
            ON fr.company_id = s.company_id
            """,
            self.conn
        )

        # Load screener config
        with open(
            "config/screener_config.yaml",
            "r"
        ) as file:

            self.config = yaml.safe_load(file)

    def get_data(self):

        return self.df.copy()

    def get_preset(
        self,
        preset_name
    ):

        if preset_name not in self.config:

            raise ValueError(
                f"Preset '{preset_name}' not found."
            )

        return self.config[preset_name]
            # ---------------------------------
    # Apply Preset Filters
    # ---------------------------------

    def apply_filters(
        self,
        preset_name
    ):

        filters = self.get_preset(
            preset_name
        )

        df = self.df.copy()

        for rule, threshold in filters.items():

            # -----------------------------
            # Minimum Filters
            # -----------------------------

            if rule.endswith("_min"):

                column = rule.replace(
                    "_min",
                    ""
                )

                if column in df.columns:

                    if column == "interest_coverage":

                        # Debt Free behaves as infinity
                        df = df[
                            (df[column] >= threshold)
                            |
                            (df[column].isna())
                        ]

                    else:

                        df = df[
                            df[column] >= threshold
                        ]

            # -----------------------------
            # Maximum Filters
            # -----------------------------

            elif rule.endswith("_max"):

                column = rule.replace(
                    "_max",
                    ""
                )

                if column in df.columns:

                    # D/E exception
                    if column == "debt_to_equity":

                        financial = df[
                            df["broad_sector"] == "Financials"
                        ]

                        non_financial = df[
                            df["broad_sector"] != "Financials"
                        ]

                        non_financial = non_financial[
                            non_financial[column] <= threshold
                        ]

                        df = pd.concat(
                            [
                                financial,
                                non_financial
                            ],
                            ignore_index=True
                        )

                    else:

                        df = df[
                            df[column] <= threshold
                        ]

        return df
    # ---------------------------------
    # Composite Quality Score
    # ---------------------------------

    def calculate_composite_score(self, df):

        df = df.copy()

        metrics = [
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "asset_turnover"
        ]

        score_columns = []

        for metric in metrics:

            if metric in df.columns:

                minimum = df[metric].min()
                maximum = df[metric].max()

                if maximum > minimum:

                    score_col = metric + "_score"

                    df[score_col] = (
                        (
                            df[metric] - minimum
                        )
                        /
                        (
                            maximum - minimum
                        )
                    ) * 100

                else:

                    score_col = metric + "_score"

                    df[score_col] = 50

                score_columns.append(score_col)

        df["composite_quality_score"] = (
            df[score_columns]
            .mean(axis=1)
            .round(2)
        )

        return df


    # ---------------------------------
    # Custom Filter
    # ---------------------------------

    def custom_filter(
        self,
        custom_rules
    ):

        df = self.df.copy()

        for rule, threshold in custom_rules.items():

            if rule.endswith("_min"):

                column = rule.replace(
                    "_min",
                    ""
                )

                if column in df.columns:

                    df = df[
                        df[column] >= threshold
                    ]

            elif rule.endswith("_max"):

                column = rule.replace(
                    "_max",
                    ""
                )

                if column in df.columns:

                    df = df[
                        df[column] <= threshold
                    ]

        df = self.calculate_composite_score(df)

        return df.sort_values(
            "composite_quality_score",
            ascending=False
        )


    # ---------------------------------
    # Close DB
    # ---------------------------------

    def close(self):

        self.conn.close()


# ---------------------------------
# Main
# ---------------------------------

if __name__ == "__main__":

    engine = ScreenerEngine()

    print("Rows Loaded :", len(engine.df))

    print("\nAvailable Presets:")

    for preset in engine.config:

        print("-", preset)

    print("\nRunning Quality Compounder...\n")

    result = engine.apply_filters(
        "quality_compounder"
    )

    result = engine.calculate_composite_score(
        result
    )

    print(
        result[
            [
                "company_id",
                "return_on_equity_pct",
                "composite_quality_score"
            ]
        ].head(10)
    )

    print("\nCompanies Returned :", len(result))

    engine.close()