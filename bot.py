# main_bot.py (hosted on GitHub)
import discord
import aiohttp
import asyncio
import logging
import os
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

try:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    client = discord.Client(self_bot=True, intents=intents)
except AttributeError:
    logger.warning("Intents not supported. Proceeding without intents...")
    client = discord.Client(self_bot=True)

CHANNEL_WEBHOOK_MAP = {
    427560506832715796: "https://discord.com/api/webhooks/1352983805417361408/cMk1Afw60NKB5CEbTISTZprqD1T_5O5kTVCCCnPddzXsYu40QPW2_XaBf7mijUGxDH8w",
    866704036237148180: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1285968642369917043: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    888831833230434364: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1217319820681281638: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1223753648564080690: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
}

async def main():
    session = aiohttp.ClientSession()
    try:
        @client.event
        async def on_ready():
            logger.info(f"Connected to {client.user.name} (ID: {client.user.id})")
            for channel_id in CHANNEL_WEBHOOK_MAP.keys():
                channel = client.get_channel(channel_id)
                if channel:
                    logger.info(f"Found source channel: {channel} (ID: {channel_id})")
                else:
                    logger.warning(f"Could not find source channel with ID {channel_id}")

        @client.event
        async def on_message(message):
            if message.author.id == client.user.id:
                return
            logger.info(f"Message received: {message.content} from {message.author} in channel {message.channel.id}")
            if message.channel.id in CHANNEL_WEBHOOK_MAP:
                webhook_url = CHANNEL_WEBHOOK_MAP[message.channel.id]
                logger.info(f"Message matches source channel {message.channel.id}! Sending via webhook {webhook_url}...")
                
                # Prepare content with original message and attachment URLs
                content = message.content
                if message.attachments:
                    attachment_urls = [attachment.url for attachment in message.attachments]
                    content += "\n" + "\n".join(attachment_urls) if content else "\n".join(attachment_urls)
                
                payload = {
                    "content": content,
                    "username": str(message.author.name),
                    "avatar_url": message.author.avatar.url if message.author.avatar else None
                }
                try:
                    async with session.post(webhook_url, json=payload) as response:
                        if response.status == 204:
                            logger.info(f"Message sent successfully via webhook for channel {message.channel.id}!")
                        else:
                            logger.error(f"Webhook error: Status {response.status}, Response: {await response.text()}")
                except Exception as e:
                    logger.error(f"Error sending message via webhook for channel {message.channel.id}: {e}")

        while True:
            try:
                logger.info("Starting client...")
                token = os.getenv("DISCORD_TOKEN")
                if not token:
                    raise ValueError("DISCORD_TOKEN environment variable not set")
                await client.start(token)
            except Exception as e:
                logger.error(f"Failed to start client: {e}. Retrying in 60 seconds...")
                await asyncio.sleep(60)
    finally:
        await session.close()

if __name__ == "__main__":
    logger.info("Running asyncio.run(main())...")
    asyncio.run(main())
