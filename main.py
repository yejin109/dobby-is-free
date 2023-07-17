import yaml
from bot import SlackBot
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--channel', default='test')
parser.add_argument('--text', default='테스트 입니다.')

credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)

if __name__ == '__main__':
    args = parser.parse_args()

    slack_bot = SlackBot(credentials['slack'])

    channel_id = slack_bot.get_channel_id(args.channel)

    slack_bot.post_message(args.text)
