import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter
from typing import Dict

router: APIRouter = APIRouter()

headers: dict = {
    "content-type": "text/html; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/27.0.1453.94 "
                    "Safari/537.36"
}


@router.get("/{uid}/stats")
async def stats(uid: int) -> Dict[str, str]:
    result: Dict[str, str] = {}
    res: requests.Response = requests.get(
        "https://www.mcbbs.net/home.php?uid={uid}".format(uid=uid),
        headers=headers
    )
    soup: BeautifulSoup = BeautifulSoup(res.text, "html5lib")
    for i, v in enumerate(soup.find_all("li")[-10::]):
        v_soup: BeautifulSoup = BeautifulSoup(str(v), "html5lib")
        result[v_soup.find("em").text] = v_soup.find("li").contents[1].text
    return result
