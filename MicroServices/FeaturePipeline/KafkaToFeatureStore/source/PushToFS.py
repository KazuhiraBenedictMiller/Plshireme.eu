from typing import Dict

import Config

import hopsworks
import pandas as pd


def PushToFS(feature_group_name: str, feature_group_version: int, data: Dict) -> None:
    """
    Gets Data to be written to the Feature Group Name with Feature Group Version.
    Given the Data, it simply pushes it to the Feature Store at Feature Group Name and Feature Group Version Locations.

    Args:
        feature_group_name (str): Name of the Feature Group in the Feature Store to write to
        feature_group_version (int): Version of the Feature Group (Used for Data Versioning) to write to
        data (Dict): Actual Candle OHLC Data to be Pushed

    Returns:
        None
    """

    project = hopsworks.login(
        project=Config.HopsworksProjectName, api_key_value=Config.HopsworksAPIKey
    )

    featurestore = project.get_feature_store()

    # Get or Create the feature_group_name Feature Group
    featuregroup = featurestore.get_or_create_feature_group(
        name=feature_group_name,
        version=feature_group_version,
        description='BTCUSD 1Min OHLC Data',
        # Primary Key to Fetch and Join Data
        primary_key=['product_id', 'timestamp'],
        event_time='timestamp',
        # To Enable Online Serving (Online Feature Store)
        online_enabled=True,
    )

    # breakpoint()

    # Transforming Data into a Pandas DF
    datadf = pd.DataFrame(data)

    # Insert Data into Feature Group
    featuregroup.insert(datadf)
