import discord
import aiohttp
import asyncio

client = discord.Client(self_bot=True)

CHANNEL_WEBHOOK_MAP = {
    427560506832715796: "https://discord.com/api/webhooks/1352983805417361408/cMk1Afw60NKB5CEbTISTZprqD1T_5O5kTVCCCnPddzXsYu40QPW2_XaBf7mijUGxDH8w",
    866704036237148180: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1285968642369917043: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    888831833230434364: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1217319820681281638: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
    1223753648564080690: "https://discord.com/api/webhooks/1352984410416353351/fqqpYbJyt44ttZXCYvt6psIuowwnawRPkZTP9Aot6aDysOUss8UPRy_VO3qHXxyiA1m9",
}

print("Starting script...")

async def main():
    print("Entering main function...")
    session = aiohttp.ClientSession()
    try:
        @client.event
        async def on_ready():
            print(f"Connected to {client.user.name} (ID: {client.user.id})")

            # Verify source channels
            for channel_id in CHANNEL_WEBHOOK_MAP.keys():
                channel = client.get_channel(channel_id)
                if channel:
                    print(f"Found source channel: {channel} (ID: {channel_id})")
                    if hasattr(channel, 'guild'):
                        print(f"Channel {channel_id} belongs to guild: {channel.guild.name} (ID: {channel.guild.id})")
                else:
                    print(f"Error: Could not find source channel with ID {channel_id}")

        @client.event
        async def on_message(message):
            print(f"on_message triggered for message ID: {message.id}")
            if message.author.id == client.user.id:
                print("Ignoring message from selfbot user")
                return

            print(f"Message received: {message.content} from {message.author} in channel {message.channel.id}")
            if message.channel.id in CHANNEL_WEBHOOK_MAP:
                webhook_url = CHANNEL_WEBHOOK_MAP[message.channel.id]
                print(f"Message matches source channel {message.channel.id}! Sending via webhook {webhook_url}...")

                payload = {
                    "content": message.content,
                    "username": str(message.author.name),
                    "avatar_url": message.author.avatar.url if message.author.avatar else None
                }
                print(f"Webhook payload: {payload}")

                try:
                    async with session.post(webhook_url, json=payload) as response:
                        print(f"Webhook response status: {response.status}")
                        if response.status == 204:
                            print(f"Message sent successfully via webhook for channel {message.channel.id}!")
                        else:
                            response_text = await response.text()
                            print(f"Webhook error: Status {response.status}, Response: {response_text}")
                except Exception as e:
                    print(f"Error sending message via webhook for channel {message.channel.id}: {e}")

        print("Starting client...")
        await client.start("MTI0NTM4ODUzNTEwNDY3MTc0NQ.GocMC_.LP7PAi9KVnjkr1LHjSnJTUEy0q1LqheW7URZ8U")

    except Exception as e:
        print(f"Error during login or runtime: {e}")
    finally:
        print("Closing session...")
        await session.close()

if __name__ == "__main__":
    print("Running asyncio.run(main())...")
    asyncio.run(main())
