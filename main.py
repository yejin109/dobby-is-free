import yaml
import argparse
from datetime import datetime

from slack import SlackBot, encode_papers
from crawl import get_papers


parser = argparse.ArgumentParser()
parser.add_argument('--date', default=datetime.today().strftime(f"%a, %d %b %Y"))

credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)
arxivs = yaml.load(open('./arxiv.yml'), Loader=yaml.FullLoader)


def to_slack(arxiv_name, _contents):
    channel_name = arxivs[arxiv_name]['slack_channel']
    # slack interface
    slack_bot = SlackBot(credentials['slack'])
    channel_id = slack_bot.get_channel_id(channel_name)
    slack_bot.post_message(channel_id, _contents)


def get_paper_list(_subject, date):
    arxiv_url = arxivs[_subject]['arxiv_link_all']
    _papers = get_papers(arxiv_url, date)
    return _papers


if __name__ == '__main__':
    args = parser.parse_args()
    exceptions = ['AI', 'IT']
    # exceptions = ['AI', "IT", 'CV', 'ML']
    # Arxiv post
    for subject in arxivs.keys():
        if subject in exceptions:
            continue
        try:
            papers = get_paper_list(subject, args.date)
            contents = encode_papers(papers, args.date)
            to_slack(subject, contents)
            print(f"{subject} Arxiv DONE")
        except AssertionError as e:
            print(f"Error occurs at {subject}, Err: {e}")
            continue
