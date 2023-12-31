from datetime import datetime
from slack_sdk import WebClient


class SlackBot:
    def __init__(self, token) -> None:
        self.client = WebClient(token)

    def get_channel_id(self, channel_name: str):
        """
        슬랙 채널ID 조회
        """
        channel_name = channel_name.replace(' ', '-')
        # conversations_list() 메서드 호출
        result = self.client.conversations_list()
        # 채널 정보 딕셔너리 리스트
        channels = result.data['channels']

        # 채널 명이 'test'인 채널 딕셔너리 쿼리
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        # 채널ID 파싱
        channel_id = channel["id"]
        return channel_id

    def get_thread_id(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        # conversations_history() 메서드 호출
        result = self.client.conversations_history(channel=channel_id)
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data['messages']
        # 채널 내 메세지가 query와 일치하는 메세지 딕셔너리 쿼리
        message = list(filter(lambda m: query in m["text"], messages))[0]
        # 해당 메세지ts 파싱
        message_ts = message["ts"]
        return message_ts

    def post_thread_message(self, channel_id, thread_id, contents, post_type='blocks'):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        if post_type == 'blocks':
            if not isinstance(contents, list):
                contents = [contents]
            if len(contents) >= 50:
                contents = contents[:50]
            result = self.client.chat_postMessage(
                channel=channel_id,
                blocks=contents,
                thread_ts=thread_id
            )
        elif post_type == 'text':
            result = self.client.chat_postMessage(
                channel=channel_id,
                text=contents,
                thread_ts=thread_id
            )
        else:
            assert False, 'NOT SUPPORTING POST TYPE'
        return result

        # result = self.client.chat_postMessage(
        #     channel=channel_id,
        #     text = text,
        #     thread_ts = message_ts
        # )
        # return result

    def post_message(self, channel_id, contents, post_type='blocks'):
        """
        슬랙 채널에 메세지 보내기
        """
        # chat_postMessage() 메서드 호출
        if post_type == 'blocks':
            if not isinstance(contents, list):
                contents = [contents]
            for i in range(0, len(contents), 50):
                blocks = contents[i:i + 50]
                result = self.client.chat_postMessage(
                    channel=channel_id,
                    blocks=blocks
                )
                print(f"{i+1}th chunk DONE")
        elif post_type == 'text':
            result = self.client.chat_postMessage(
                channel=channel_id,
                text=contents
            )
        else:
            assert False, 'NOT SUPPORTING POST TYPE'
        return result


def encode_papers(papers, title):
	header = {
		"type": "header",
		"text": {"type": "plain_text", "text": f"{title} New Papers!"}
	}
	encoded = [header]
	for i, paper in enumerate(papers):
		block = get_paper_text(paper)
		encoded.append(block)

	return encoded


def get_paper_text(paper):
	return {
		"type": "section",
		"fields": [
			{
				"type": "mrkdwn",
				"text": f"*Title:* \n{paper['title']}"
			},
			{
				"type": "mrkdwn",
				"text": f"*link:* {paper['link']}"
			}
		]
	}