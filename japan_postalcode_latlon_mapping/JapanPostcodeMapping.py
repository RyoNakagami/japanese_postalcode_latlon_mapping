from dataclasses import dataclass
from .utils import file_inputoutput as fio

import requests
import pandas as pd


@dataclass(repr=False)
class FetchPostalCodeData:

    config_path: str
    output_path: str
    postalcode_list: list

    def __post_init__(self):
        self.__api_info = fio.read_yaml(self.config_path)["yahoo_postalcode_api"]
        self.__client_id = self.__api_info["client_id"]
        self.__api_url = self.__api_info["api_url"]

    def request_postalcode_info(self, postalcode) -> list:
        payload = {
            "appid": self.__client_id,
            "output": "json",
            "query": postalcode,
        }

        default = [
            dict(
                {
                    "Id": "",
                    "Gid": "",
                    "Name": "",
                    "Geometry": dict({"Type": "", "Coordinates": ""}),
                    "Category": [],
                    "Description": "",
                    "Style": [],
                    "Property": dict(
                        {
                            "Uid": "",
                            "CassetteId": "",
                            "Country": dict({"Code": "", "Name": ""}),
                            "Address": "",
                            "GovernmentCode": "",
                            "AddressMatchingLevel": "",
                            "PostalName": "",
                            "Station": [],
                            "OpenForBusiness": "",
                            "Detail": dict({"PcUrl1": ""}),
                        }
                    ),
                }
            )
        ]

        r = requests.get(self.__api_url, params=payload)
        res = r.json()
        try:
            return res["Feature"]
        except KeyError:
            return default

    def call_api(self) -> None:
        self.api_result = list(map(self.request_postalcode_info, self.postalcode_list))

    def save_dataframe_format(self) -> None:
        data = pd.DataFrame(
            {"postalcode": self.postalcode_list, "api_result": self.api_result}
        ).explode("api_result")

        self.result_df = pd.merge(
            data["postalcode"].reset_index(drop=True),
            pd.json_normalize(data["api_result"]),
            left_index=True,
            right_index=True,
        )

        self.result_df.to_csv(self.output_path)
