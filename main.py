import yaml
import argparse
from datetime import datetime

from slack import SlackBot, encode_papers
from crawl import get_arxiv, get_icml


parser = argparse.ArgumentParser()
parser.add_argument('--target_arxiv',
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--arxiv_date',
                    # default=datetime.today().strftime(f"%a, %d %b %Y"),
                    default="Mon, 17 Jul 2023",
                    help='format : %a, %d %b %Y such as Mon, 17 Jul 2023'
                    )

parser.add_argument('--target_conf',
                    action=argparse.BooleanOptionalAction)
parser.add_argument('--conf_year',
                    default=2022)
parser.add_argument('--conf_keyword',
                    default="shot")


credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)

arxivs = yaml.load(open('./arxiv.yml'), Loader=yaml.FullLoader)
conferences = yaml.load(open('./conference.yml'), Loader=yaml.FullLoader)


def to_slack(channel_name, _contents):
    # slack interface
    slack_bot = SlackBot(credentials['slack'])
    channel_id = slack_bot.get_channel_id(channel_name)

    # post할 thread만들기
    slack_response = slack_bot.post_message(channel_id, _contents[0])

    # post할 thread 찾기
    # thread_id = slack_bot.get_thread_id(channel_id, _contents[0]['text']['text'])
    # slack_bot.post_message(channel_id, _contents)
    slack_bot.post_thread_message(channel_id, slack_response.data['ts'], _contents[1:])


def get_arxiv_paper_list(_subject, date):
    arxiv_url = arxivs[_subject]['arxiv_link_all']
    _papers = get_arxiv(arxiv_url, date)
    return _papers


def get_conference_paper_list(_conf, _year, _keyword):
    if _conf == 'ICML':
        _papers = get_icml(conferences[_conf]['url'], _year, _keyword)
    else:
        assert False

    return _papers


if __name__ == '__main__':
    args = parser.parse_args()
    # Arxiv post
    if args.target_arxiv:
        print("Arxiv start")
        # arxiv_exceptions = []
        arxiv_exceptions = ['AI', "IT", 'CV', 'ML']
        for subject in arxivs.keys():
            if subject in arxiv_exceptions:
                continue
            try:
                papers = get_arxiv_paper_list(subject, args._arxiv_date)
                contents = encode_papers(papers, args.date)
                channel_name = arxivs[subject]['slack_channel']
                to_slack(channel_name, contents)
                print(f"{subject} Arxiv DONE")
            except AssertionError as e:
                print(f"Error occurs at {subject}, Err: {e}")
                continue

    # Conference
    if args.target_conf:
        print("Conf start")
        conference_exceptions = []
        for conference in conferences.keys():
            if conference in conference_exceptions:
                continue
            try:
                papers = get_conference_paper_list(conference, args.conf_year, args.conf_keyword)
                contents = encode_papers(papers, f"{args.conf_year}- Keyword {args.conf_keyword}.")
                channel_name = conferences[conference]['slack_channel']
                to_slack(channel_name, contents)
                print(f"{conference} Conference DONE")
            except AssertionError as e:
                print(f"Error occurs at {conference}, Err: {e}")
                continue
