# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from datetime import datetime

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    def __init__(self, text_analytics_client):
        super().__init__()
        self._text_analytics_client = text_analytics_client

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello and welcome! Type 'help' to see what I can do."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        # Get the user message text in a simple, safe way
        user_text = turn_context.activity.text or ""
        normalized = user_text.strip().lower()

        # HELP: list capabilities
        if normalized == "help":
            reply_text = (
                "I am a simple chatbot connected to Azure AI Language.\n"
                "- Type 'hello' for a greeting.\n"
                "- Type 'time' to see the current server time.\n"
                "- Type anything else and I will echo it back and show sentiment.\n"
            )

        # HELLO: greeting
        elif normalized in ("hi", "hello", "hey"):
            reply_text = "Hello! I am your EchoBot with sentiment analysis."

        # TIME: show current time
        elif normalized == "time":
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reply_text = f"The current server time is: {now}"

        # FALLBACK: unknown input → echo + sentiment analysis
        else:
            sentiment_info = ""
            try:
                documents = [user_text]
                result = self._text_analytics_client.analyze_sentiment(
                    documents=documents
                )[0]
                sentiment_info = (
                    f"\n\n[Sentiment: {result.sentiment} "
                    f"(pos={result.confidence_scores.positive:.2f}, "
                    f"neu={result.confidence_scores.neutral:.2f}, "
                    f"neg={result.confidence_scores.negative:.2f})]"
                )
            except Exception as ex:
                sentiment_info = f"\n\n[Sentiment analysis error: {ex}]"

            reply_text = (
                "I did not fully understand that as a command, "
                "but here is your text and its sentiment:\n"
                f"Echo: {user_text}{sentiment_info}"
            )

        return await turn_context.send_activity(MessageFactory.text(reply_text))
