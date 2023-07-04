import requests
import sys
import time
import pandas as pd
from random import choice

# add you desktop agent here. for this go to: https://www.whatismybrowser.com/detect/what-is-my-user-agent/
# and copy your agent here
# Example ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36']
desktop_agents = [""]


def random_headers():
    return {
        "User-Agent": choice(desktop_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }


def call_api(doi):
    search_url = (
        "http://api.semanticscholar.org/v1/paper/"
        + doi
        + "?include_unknown_references=true"
    )

    resp = requests.get(search_url, headers=random_headers())
    content = resp.json()
    return content


if __name__ == "__main__":
    df = pd.read_csv("../data/" + sys.argv[1])
    filename = sys.argv[2]

    print(len(df))
    df = df[df.doi != "No Doi"]
    print(len(df))
    list_doi = list(df["doi"])
    list_abstracts = []
    list_topics = []
    i = 0
    for doi in list_doi:
        i = i + 1
        print(i)
        try:
            content = call_api(doi)
            list_abstracts.append(content["abstract"])
            list_topics.append(content["topics"])
        except Exception as e:
            print(e)
            list_abstracts.append("None")
            list_topics.append("None")
        time.sleep(2)
    df["abstract"] = list_abstracts
    df["topics"] = list_topics
    df.to_csv("../data/abstracts_" + filename + ".csv", index=None)
