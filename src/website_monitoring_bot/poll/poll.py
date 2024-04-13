from bs4 import BeautifulSoup
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl
from requests import get


class Poll(BaseModel):
    url: AnyHttpUrl
    element: str

    def poll(self) -> str:
        page = get(url=str(self.url))
        soup = BeautifulSoup(markup=page.text, features="html.parser")
        element = soup.find(id=self.element)
        return element.text if element else ""
