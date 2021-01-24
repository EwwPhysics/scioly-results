from bs4 import BeautifulSoup
import requests


def get_scores(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    events = []
    top_row = soup.find_all("th")
    for event in top_row:
        event = event.text.strip()
        if event not in {"School/Team", "Place", "Total"}:
            events.append(event)

    data = {}
    schools = soup.find("tbody")
    for school in schools.find_all('tr')[:-1]:
        placements = {}
        school = school.find_all('td')
        for i in range(3, len(events) + 3):
            placements[events[i - 3]] = int(school[i].text.strip())
        data[school[0].text.strip()] = placements

    return data


def superscore(data):
    combined_results = {}
    for school in data:
        if "," in school:
            school_name = school[:school.find(',')]
            if school_name not in combined_results:
                combined_results[school_name] = data[school]
            else:
                for event in combined_results[school_name]:
                    if data[school][event] < combined_results[school_name][event]:
                        combined_results[school_name][event] = data[school][event]
    return combined_results


if __name__ == "__main__":
    s = get_scores("https://scilympiad.com/ut-invite/Info/Results/255a4158-7761-44e6-b653-059a1928c259")
    print(superscore(s))
