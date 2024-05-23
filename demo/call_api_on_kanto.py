# %%
import pandas as pd
from japan_postalcode_latlon_mapping.JapanPostcodeMapping import FetchPostalCodeData
from japan_postalcode_latlon_mapping.utils import file_inputoutput as fio
from japan_postalcode_latlon_mapping.utils import datatype_operation as dto

# -----------------------
# get Kanto Postal Code List
# -----------------------


def get_postalcode_list(
    postalcode_master_path: str,
    region_master_path: str,
    schema_path: str,
    target_region: str,
) -> list:
    ken_all_info = fio.read_json(schema_path)
    ken_all_datatype = dto.dict_flatten(ken_all_info["properties"], "type")

    df_postalcode = pd.read_csv(
        postalcode_master_path,
        encoding=ken_all_info["encoding"],
        names=list(ken_all_datatype.keys()),
        dtype=ken_all_datatype,
    )

    df_region = pd.read_csv(region_master_path)
    prefecure_list = df_region.loc[
        df_region["region"] == target_region, "prefecture"
    ].values
    return list(
        df_postalcode.loc[
            df_postalcode["prefecture"].isin(prefecure_list), "postalcode"
        ].unique()
    )


args = (
    "../data/input/KEN_ALL.csv",
    "../data/input/prefecture_master.csv",
    "../data/schema/KEN_ALL_schema.json",
    "関東",
)

kanto_postalcode_list = sorted(get_postalcode_list(*args))


# %%
# -----------------------
# API call on kanto area
# -----------------------
FPCD = FetchPostalCodeData(
    config_path="../config/yahoo_api.yaml",
    output_path="../data/output/postalcode_kanto_20240524.csv",
    postalcode_list=kanto_postalcode_list,
)
FPCD.call_api()

# %%
FPCD.save_dataframe_format()

# %%
FPCD.result_df["Property.Station"]
