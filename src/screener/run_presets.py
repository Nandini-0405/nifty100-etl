from src.screener.engine import ScreenerEngine


engine = ScreenerEngine()

presets = [

    "quality_compounder",

    "value_pick",

    "growth_accelerator",

    "dividend_champion",

    "debt_free_blue_chip",

    "turnaround_watch"

]


for preset in presets:

    print("\n" + "=" * 60)

    print(f"Running preset: {preset}")

    try:

        df = engine.apply_filters(
            preset
        )

        df = engine.calculate_composite_score(
            df
        )

        print(
            "Companies found:",
            len(df)
        )

        if len(df) > 0:

            columns_to_show = []

            if "company_id" in df.columns:

                columns_to_show.append(
                    "company_id"
                )

            if "return_on_equity_pct" in df.columns:

                columns_to_show.append(
                    "return_on_equity_pct"
                )

            if "debt_to_equity" in df.columns:

                columns_to_show.append(
                    "debt_to_equity"
                )

            if "composite_quality_score" in df.columns:

                columns_to_show.append(
                    "composite_quality_score"
                )

            print(

                df[
                    columns_to_show
                ].head(10)

            )

    except Exception as e:

        print(

            f"Error while running "

            f"{preset}: {e}"

        )


engine.close()

print("\nDone.")