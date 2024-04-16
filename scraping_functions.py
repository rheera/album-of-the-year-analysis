def check_must_hear(album_cover_classes):
    if "mustHear" in album_cover_classes:
        if "both" in album_cover_classes:
            return "both"
        elif "user" in album_cover_classes:
            return "user"
        else:
            return "critic"
    else:
        return "no"


def get_album_info(album_element, list_year):
    """
    Get an album's information.

    Parameters
    ----------
    album_element : bs4 element Tag
        An album's div tag
    list_year: int
        The year of the list that the album is on eg. 1958

    Returns
    -------
    A Dict with all the album's information
    """
    import re

    rank = (
        int(float(album_element.find(class_="albumListRank").text))
        if album_element.find(class_="albumListRank")
        else -1
    )
    title = (
        album_element.find(class_="albumListTitle").text
        if album_element.find(class_="albumListTitle")
        else ""
    )
    artist_name = re.search(r"[\d]+[\.](.*)-", title).group(1).strip() if title else ""
    album_name = re.search(r"[\d]+[\.].+-(.*)", title).group(1).strip() if title else ""
    release_date = album_element.find(class_="albumListDate").text
    genres = (
        album_element.find(class_="albumListGenre").text.split(", ")
        if album_element.find(class_="albumListGenre")
        else ""
    )
    user_score = (
        int(album_element.find(class_="scoreValue").text)
        if album_element.find(class_="scoreValue")
        else -1
    )
    user_score_float = (
        float(album_element.find(class_="scoreValueContainer").attrs["title"])
        if album_element.find(class_="scoreValueContainer")
        else -1
    )
    number_of_ratings = (
        int(album_element.find(class_="scoreText").text.split(" ")[0].replace(",", ""))
        if album_element.find(class_="scoreText")
        else -1
    )
    link_to_album = (
        album_element.find("a", itemprop="url").attrs["href"]
        if album_element.find("a", itemprop="url")
        else ""
    )
    must_hear = check_must_hear(
        album_element.find(class_="albumListCover").attrs["class"]
        if album_element.find(class_="albumListCover")
        else ""
    )
    album_artwork_link = (
        album_element.find(class_="albumListCover").find("img").attrs["data-src"]
        if (
            album_element.find(class_="albumListCover")
            and album_element.find(class_="albumListCover").find("img")
        )
        else ""
    )
    return {
        "rank": rank,
        "artist_name": artist_name,
        "album_name": album_name,
        "release_date": release_date,
        "genres": genres,
        "user_score": user_score,
        "user_score_float": user_score_float,
        "number_of_ratings": number_of_ratings,
        "link_to_album": link_to_album,
        "must_hear": must_hear,
        "album_artwork_link": album_artwork_link,
        "list_year": list_year,
    }


def get_years_top_albums(base_url, year_url):
    """
    Get the information of the top 100 albums of a given year

    Parameters
    ----------
    base_url : string
        The base url of Album of the year's rating page
    year_url: string
        The year of the list you want. As a url parameter eg. 1958/

    Returns
    -------
    An array of Dicts, each with an album's information
    """

    import random
    import time

    import requests
    from bs4 import BeautifulSoup

    num_of_pages = 99
    years_album_list = []
    for page_number in range(1, 5):
        # if the year doesn't have the full 100 songs break out of the loop
        if num_of_pages < page_number:
            break
        time.sleep(random.randint(10, 30))
        page_url = str(page_number) + "/"
        if page_number == 1:
            page_url = ""
        r = requests.get(base_url + year_url + page_url)
        # if the page doesn't load or if it redirects to another page then don't scrape
        # sometimes if a page doesn't exist it'll redirect to the latest years list so this avoids scanning that
        if (
            r.status_code != requests.codes.ok
            or r.url != base_url + year_url + page_url
        ):
            with open("log.csv", "a") as logFile:
                logFile.write(f"{base_url + year_url + page_url},{r.status_code}\n")
            continue
        soup = BeautifulSoup(r.text, features="html.parser")
        # on the first page see how many pages there are
        if page_number == 1:
            num_of_pages = len(soup.find_all(class_="pageSelectSmall"))
        album_list = soup.find_all(class_="albumListRow")
        for album in album_list:
            years_album_list.append(get_album_info(album, int(year_url[0:4])))
    return years_album_list


def get_range_top_albums(start_year, end_year, base_url):
    """
    Get the information of the top 100 albums of a range of given years.

    Parameters
    ----------
    start_year : int
        start of the range inclusive
    end_year : int
        end of the range exclusive
    base_url: string
        The base url of Album of the year's rating page

    Returns
    -------
    An array of Dicts, each with an album's information
    """
    full_albums_list = []
    for year_number in range(start_year, end_year):
        year_url = str(year_number) + "/"
        full_albums_list = full_albums_list + get_years_top_albums(base_url, year_url)
    return full_albums_list
