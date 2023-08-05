import importlib.metadata
import importlib.util
import io
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import ClassVar, Dict, List
from zipfile import ZipFile

import requests

from PIModelManager.pandora_model import PandoraModel

logger = logging.getLogger("PIModelManager")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
ch.setFormatter(formatter)

logger.addHandler(ch)


class ModelManager:
    """Singleton class that manages ML models"""

    __instance: ClassVar[object] = None

    _config: ClassVar[Dict] = {}

    _credentials: ClassVar[Dict[str, str]] = {}
    _container: ClassVar[str] = None
    _login_url: ClassVar[str] = None
    _get_files_url: ClassVar[str] = None
    _download_file_url: ClassVar[str] = None

    _available_files: ClassVar[List[str]] = []
    _downloaded_models: ClassVar[List[PandoraModel]] = []

    def __new__(cls):
        if ModelManager.__instance is None:
            ModelManager.__instance = object.__new__(cls)
        return ModelManager.__instance

    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token):
            self.token = token

        def __call__(self, r):
            r.headers["authorization"] = "Bearer " + self.token
            return r

    @classmethod
    def set_credentials(
        cls,
        grant_type: str,
        client_id: str,
        client_secret: str,
        scope: str,
        container: str,
        login_url: str,
        get_files_url: str,
        download_file_url: str,
    ):
        """Set credentials for the ModelManager

        Args:
            grant_type (str): Type of grant
            client_id (str): The consumer key
            client_secret (str): The consumer secret
            scope (str): The control scope
            container (str): The name of the storage container
            login_url (str): The sts login url
            get_files_url (str): The URL for getting a list of available files in a container. Put variables in curly brackets.
            download_file_url (str): The URL for downloading a specific file from a container. Put variables in curly brackets.
        """

        if not all(
            [
                grant_type,
                client_id,
                client_secret,
                scope,
                container,
                login_url,
                get_files_url,
                download_file_url,
            ]
        ):
            raise Exception("Argument is empty or None.")

        cls._credentials = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": scope,
        }

        cls._container = container
        cls._login_url = login_url
        cls._get_files_url = get_files_url
        cls._download_file_url = download_file_url

    @classmethod
    def __authenticate(cls):
        """Authenticate with the server.

        Raises:
            Exception: In case the credentials are not previously set using 'set_credentials' method.

        Returns:
            str: Access token
        """
        if not cls._credentials or not cls._login_url:
            raise Exception("Credentials not set. Use method set_credentials.")

        # Authentication request
        response = requests.post(cls._login_url, data=cls._credentials)
        if response.status_code == 200:
            result = json.loads(response.text)

            return result["access_token"]

        return None

    @classmethod
    def download_models(cls, config: List[Dict]) -> None:
        """Download all models described in a config.

        Args:
            config (List[Dict]): a list of dictionaries describing ML models.

        Raises:
            Exception: if the config file is invalid.
        """

        cls._config = config

        for model in cls._config:
            download_scenario = model.get("download_scenario", None)
            if download_scenario == "pip":
                if model["model_type"] == "spacy":
                    cls.__download_model_pip(model)
                else:
                    raise Exception(
                        f"Invalid config file - pip not supported for model type {model['model_type']}"
                    )
            elif download_scenario == "dataservices":
                cls.__download_model_dataservices(model)
            else:
                raise Exception("Invalid config file - missing download scenario.")

    @classmethod
    def __download_model_pip(cls, model: Dict[str, str]) -> None:
        """Download a model as a pip package.

        Args:
            model (Dict[str, str]): model description from a config file

        Raises:
            Exception: if the config file is invalid.
        """

        if model["model_type"] == "spacy":
            name = model.get("name", None)
            version = model.get("version", None)

            if name and version:
                if cls.__pip_package_is_available(name, version):
                    logger.info(f"Package {name}-{version} is already installed.")
                else:
                    package = name + "-" + version
                    subprocess.check_call(
                        [sys.executable, "-m", "spacy", "download", package, "--direct"]
                    )

                pandora_model = PandoraModel(
                    type=model["model_type"],
                    language=model["language"],
                    size=model["size"],
                    name=name,
                    client=model.get("client", "default"),
                    version=version,
                    path=model.get("path", name),
                )

                if pandora_model not in cls._downloaded_models:
                    cls._downloaded_models.append(pandora_model)
            else:
                raise Exception(
                    "Invalid config file - missing name and/or version fields."
                )
        else:
            Exception(
                f"Invalid config file - pip not supported for model type {model['model_type']}"
            )

    @classmethod
    def __pip_package_is_available(cls, name: str, version: str) -> bool:
        """Check if a pip package is already installed

        Args:
            name (str): name of the package
            version (str): version of the package

        Returns:
            bool: if the package is installed or not
        """

        try:
            if importlib.util.find_spec(name):
                if importlib.metadata.version(name) == version:
                    return True
        except Exception:
            return False

        return False

    @classmethod
    def __download_model_dataservices(cls, model: Dict[str, str]) -> None:
        """Download a model from dataservices.

        Args:
            model (Dict[str, str]): model description from a config file

        Raises:
            Exception: if the config file is invalid.
        """
        if not cls._credentials:
            raise Exception("Authentication credentials have not been set.")

        cls.__update_available_files()

        language = model["language"]
        name = model["name"]
        client = model.get("client", "default")
        version = model["version"]

        query = "_".join([language, name, client, version])

        matched_models = [f for f in cls._available_files if f.startswith(query)]
        if len(matched_models) == 0:
            raise Exception(f"Specified model {query} not found in dataservices.")
        elif len(matched_models) > 1:
            raise Exception(
                f"More than one models match the one provided in the config file: {query}."
            )
        else:
            filename = matched_models[0]
            extension = filename.split("_")[-1]

            if extension == ".zip":
                model_filename = filename.rstrip(".zip")
                temp_path = Path(Path.cwd(), "models", language, name, client, version)
            else:
                model_filename = filename
                temp_path = Path(
                    Path.cwd(), "models", language, name, client, version, filename
                )

            pandora_model = PandoraModel(
                type=model["model_type"],
                language=language,
                size=model.get("size", None),
                name=name,
                client=client,
                version=version,
                path=None,
                filename=model_filename,
            )

            if temp_path.exists():
                # Update model object path and add to _downloaded_models
                pandora_model.path = temp_path
                if pandora_model not in cls._downloaded_models:
                    cls._downloaded_models.append(pandora_model)
                    logger.info(f"Model already downloaded in {temp_path}")
            else:
                # Download the model and add to _downloaded_models
                access_token = cls.__authenticate()
                url = cls._download_file_url.replace("{container}", cls._container)
                url = url.replace("{filename}", filename)
                response = requests.get(url, auth=cls.BearerAuth(access_token))

                if response.status_code == 200:
                    if extension == ".zip":
                        dir = Path(
                            Path.cwd(),
                            "models",
                            pandora_model.language,
                            pandora_model.name,
                            pandora_model.client,
                            pandora_model.version,
                        )
                        dir.mkdir(parents=True, exist_ok=True)

                        zf = ZipFile(io.BytesIO(response.content), "r")

                        if not zf.namelist():
                            raise Exception(f"Zip file {filename} is empty.")

                        zf.extractall(dir)

                        pandora_model.path = dir
                        cls._downloaded_models.append(pandora_model)

                        logger.info(f"Extracted model to: {pandora_model.path}")
                    else:
                        dir = Path(
                            Path.cwd(),
                            "models",
                            pandora_model.language,
                            pandora_model.name,
                            pandora_model.client,
                            pandora_model.version,
                        )
                        dir.mkdir(parents=True, exist_ok=True)
                        path = Path(dir, pandora_model.filename)

                        with open(path, "wb") as f:
                            f.write(response.content)

                        pandora_model.path = path
                        cls._downloaded_models.append(pandora_model)

                        logger.info(f"Saved model to: {pandora_model.path}")

    @classmethod
    def __get_files(cls, token: str):
        """Returns a list of available model files.

        Args:
            token (str): Authentication bearer token

        Returns:
            List[str]: List of all available model files
        """
        url = cls._get_files_url.replace("{container}", cls._container)
        response = requests.get(url, auth=cls.BearerAuth(token))
        if response.status_code == 200:
            return [dict(x)["name"] for x in json.loads(response.text)]
        else:
            return []

    @classmethod
    def __update_available_files(cls):
        access_token = cls.__authenticate()
        cls._available_files = cls.__get_files(access_token)

    @classmethod
    def get_model_path(cls, **kwargs):
        """Finds the matching model based on the provided keyword arguments and returns its path.

        Raises:
            Exception: if more than one models are matching the provided arguments
            Exception: if no models are matching the provided arguments

        Returns:
            Path: the local model directory
        """
        
        matching_models = [
            x
            for x in cls._downloaded_models
            if all([getattr(x, attr) == value for (attr, value) in kwargs.items()])
        ]

        if(len(matching_models) > 1):
            raise Exception(f"More than one models are matching your arguments: {kwargs}")
        elif(len(matching_models) == 1):
            return matching_models[0].path
        else:
            raise Exception(f"No models are matching your arguments: {kwargs}")