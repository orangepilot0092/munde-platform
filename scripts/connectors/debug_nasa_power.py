import asyncio
import json
from src.data_atlas.connectors.nasa_power import NASAPowerConnector


async def main():
    connector = NASAPowerConnector()
    print("🔍 Fetching raw data for Pune...")

    try:
        data = await connector.fetch_daily_point_data(
            latitude=18.5204,
            longitude=73.8567,
            start_date="20260601",
            end_date="20260610",
            parameters=["PRECTOTCORR", "T2M_MAX", "T2M_MIN"],
        )

        print("\n✅ API Call Successful!")
        print(f"Top-level keys: {list(data.keys())}")

        properties = data.get("properties", {})
        print(f"Properties keys: {list(properties.keys())}")

        param_data = properties.get("parameter", {})
        print(f"Parameter keys: {list(param_data.keys())}")

        if "PRECTOTCORR" in param_data:
            prectot = param_data["PRECTOTCORR"]
            print(f"PRECTOTCORR keys: {list(prectot.keys())}")

            data_dict = prectot.get("data", {})
            print(f"Number of data points returned: {len(data_dict)}")

            if data_dict:
                first_date = list(data_dict.keys())[0]
                print(f"Sample data for {first_date}: {data_dict[first_date]}")
        else:
            print("⚠️ 'PRECTOTCORR' not found in parameters. Full parameter object:")
            print(json.dumps(param_data, indent=2)[:500])

    except Exception as e:
        print(f"❌ API Call Failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
