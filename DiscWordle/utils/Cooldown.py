import typing
import discord
from discord.ext import commands


class Cooldown:
    """
    Bot command cooldown
    """
    def __init__(self):
        self._cd = commands.CooldownMapping.from_cooldown(1 * 1000, 6, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def check(self, message):
        # Getting the ratelimit left
        ratelimit = self.get_ratelimit(message)
        print(ratelimit)
        return ratelimit is None
