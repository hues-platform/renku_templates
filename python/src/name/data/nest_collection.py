import requests
import pandas as pd
import logging
import ast
import time
from .user_credentials import rest_user, rest_pwd

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("rest client")

class NESTClient(object):
    """Calss to connect to api.nestcloud and query data"""

    def __init__(
        self,
        username = rest_user,
        password = rest_pwd,
        domain="api.nestcloud.ch",
        url="https://api.nestcloud.ch",
    ):
        self.username = username
        self.password = password
        self.domain = domain
        self.url = url
        logger.debug("Client initialized")

    def get_NEST_access_token(self):

        url = self.url + "/user/token"

        # headers = {"Content-Type": "application/json", "accept": "application/json"}
        data = {"username": self.username, "password": self.password}

        # response = requests.request("POST", url, headers=headers, data=data)
        response = requests.request("POST", url, data=data)
        response.raise_for_status()

        try:
            response_dict = ast.literal_eval(response.text)
        except Exception as error:
            print(
                "ERROR: Could not evaluate request response as literal. Response:"
            )
            print(response.text)
            raise error

        self.NEST_access_token = response_dict["access_token"]
        self.token_time = time.time()

        return self.NEST_access_token

    def get_timeseries_data(
        self,
        start_date,
        end_date,
        agg_unit='minutes',
        agg_interval=1,
        agg_function='last',
        timeseries_id: list[str] = None,
        api_url: list[str] = None,
        tz="Europe/Zurich",
    ):
        """Method to get timeseries data from the API. It returns a list of dataframes, corresponding to the list of timeseries_id or api_url provided. Each dataframe has a 'timestamp' column and a 'value' column and are sorted by the timestamp (ascending).
        Parameters
        ----------
        start_date: str
            starting date of the time series data to be obtained
        end_date: str
            final date of the time series data to be obtained
        agg_unit: str
            time unit of data aggregation. Options: ["minutes", "hours", "days"]. The returned time series will have time step of agg_interval agg_units (e.g. 3 hours)
        agg_interval: int
            time step size of the aggregation. The unit is given by agg_unit
        agg_function: str
            aggregation function to be applied for each time step. Options: ["min", "max", "avg", "first", "last"].
        timeseries_id: list of str
            list of strings containing the timeseries_ids to be obtained through the API call
        api_url: list of str
            list of the API urls (up to the time series id) to be queried.
        """

        if timeseries_id is None and api_url is None:
            raise ValueError(
                "Either 'timeseries_id' or 'api_url' must be provided."
            )
        elif timeseries_id is not None and api_url is not None:
            logger.debug(
                "If both 'timeseries_id' and 'api_url' are provided, 'timeseries_id' is ignored."
            )

        agg_units_options = ["minutes", "hours", "days"]
        if agg_unit not in agg_units_options:
            raise ValueError(
                f"'agg_unit' argument must be one of {agg_units_options}"
            )

        agg_function_options = ["min", "max", "avg", "first", "last"]
        if agg_function not in agg_function_options:
            raise ValueError(
                f"'agg_function' argument must be one of {agg_function_options}"
            )

        url = self.url + "/nest/data"

        if api_url is None:
            API_call_list = [
                f"{url}?numericid={ts_id}&startDate={start_date}&endDate={end_date}&aggIntervall={agg_interval}&aggUnit={agg_unit}&aggFunction={agg_function}"
                for ts_id in timeseries_id
            ]
        if api_url is not None:
            API_call_list = [
                f"{api_url_i}&startDate={start_date}&endDate={end_date}&aggIntervall={agg_interval}&aggUnit={agg_unit}&aggFunction={agg_function}"
                for api_url_i in api_url
            ]

        session = requests.Session()

        if hasattr(self, "NEST_access_token"):
            if (time.time() - self.token_time) > 7.5:
                self.get_NEST_access_token()
        else:
            self.get_NEST_access_token()
        headers = {
            "Accept": "application/sparql-results+json",
            "Authorization": f"Bearer {self.NEST_access_token}",
        }
        timeseries_list = []

        for API_call in API_call_list:
            logger.info(f"Getting timeseries data for:\n {API_call}")
            try:
                timeseries = session.get(url=API_call, headers=headers)
            except Exception as e:
                logger.error(e)
            timeseries.raise_for_status()

            timeseries = timeseries.json()

            timeseries = pd.DataFrame(data=timeseries[1]["timeseries"])

            timeseries["timestamp"] = pd.to_datetime(
                timeseries["timestamp"], format="mixed", utc=True
            )
            timeseries["timestamp"] = timeseries["timestamp"].dt.tz_convert(tz)

            timeseries["value"] = timeseries["value"].astype(float)

            timeseries = timeseries.sort_values(by="timestamp", ascending=True)

            timeseries_list.append(timeseries)
        session.close()
        return timeseries_list

    def get_metadata(self):
        raise NotImplementedError("Method not yet implemented.")
        return metadata