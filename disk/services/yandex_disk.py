import requests
from typing import Any, Dict, List

class YandexDiskService:
    """
    Сервис для взаимодействия с API Яндекс.Диска.
    """
    BASE_URL = "https://cloud-api.yandex.net/v1/disk"

    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def get_file_list(self) -> List[Dict[str, Any]]:
        """
        Метод позволяет выводить список папок/файлов по публичной ссылке

        """
        url = f"{self.BASE_URL}/public/resources"
        params = {
            "public_key": self.public_key,
            "limit": 100
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения данных: {response.text}")
        data = response.json()
        embedded = data.get("_embedded")
        if not embedded:
            raise Exception("Неверный формат ответа от API. Возможно, публичная ссылка некорректна.")
        file_items = embedded.get("items", [])
        return file_items

    def download_file(self, file_path: str) -> bytes:
        """
        Загрузка файла по указанному пути на Яндекс.Диске.

        Сначала получаем временную ссылку для скачивания через эндпоинт /public/resources/download,
        затем выполняем запрос для загрузки содержимого файла.

        """
        url = f"{self.BASE_URL}/public/resources/download"
        params = {
            "public_key": self.public_key,
            "path": file_path
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка получения ссылки для загрузки: {response.text}")
        data = response.json()
        download_url = data.get("href")
        if not download_url:
            raise Exception("Ссылка для загрузки не получена.")

        file_response = requests.get(download_url)
        if file_response.status_code != 200:
            raise Exception(f"Ошибка загрузки файла: {file_response.text}")
        return file_response.content
