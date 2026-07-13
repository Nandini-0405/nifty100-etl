from src.screener.engine import ScreenerEngine
import pandas as pd
import os


os.makedirs(
    "output",
    exist_ok=True
)

engine = ScreenerEngine()

presets = [

    "quality_compounder",

    "value_pick",

    "growth_accelerator",

    "dividend_champion",

    "debt_free_blue_chip",

    "turnaround_watch"

]

writer = pd.ExcelWriter(

    "output/screener_output.xlsx",

    engine="openpyxl"

)

for preset in presets:

    print(
        f"\nRunning {preset}..."
    )

    try:

        df = engine.apply_filters(
            preset
        )

        df = engine.calculate_composite_score(
            df
        )

        columns = [

            col

            for col in [

                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "asset_turnover",
                "free_cash_flow_cr",
                "dividend_yield_pct",
                "pe_ratio",
                "pb_ratio",
                "composite_quality_score"

            ]

            if col in df.columns

        ]

        export_df = df[
            columns
        ].sort_values(

            by="composite_quality_score",

            ascending=False

        )

        export_df.to_excel(

            writer,

            sheet_name=preset[:31],

            index=False

        )

        print(

            f"Saved {len(export_df)} rows"

        )

    except Exception as e:

        print(

            f"Error in "

            f"{preset}: {e}"

        )

writer.close()

engine.close()

print(
    "\nCreated:"
)

print(
    "output/screener_output.xlsx"
)