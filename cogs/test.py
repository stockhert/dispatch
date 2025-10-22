from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server_count(self, ctx):
        await ctx.send(f'{self.bot.user} is in {len(self.bot.guilds)} servers')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def sum_of_two(self, ctx, a: int, b: int):
        await ctx.send(f'Hello world!!! :333')


async def setup(bot):
    await bot.add_cog(Test(bot))
