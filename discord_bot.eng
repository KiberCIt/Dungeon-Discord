import os
import logging
import discord
from discord.ext import commands
from game.game_session import GameSession

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'PUT_YOUR_DISCORD_BOT_TOKEN_HERE')


def print_help() -> str:
    commands_map = {
        '/start': 'Start the game',
        '/help': 'Show the help menu',
        '/randomhero': 'Create a random hero',
        '/stats': 'Show hero stats',
        '/dungeon': 'Enter the dungeon',
        '/fight': 'Fight the monster',
        '/flee': 'Try to escape',
        '/next': 'Move to the next room',
        '/search': 'Search the current room',
        '/shop': 'Open the shop',
        '/buy <item>': 'Buy an item, for example /buy iron sword',
        '/use <item>': 'Use an item, for example /use healing potion',
        '/achievement_i': 'Show achievement I',
        '/achievement_ii': 'Show achievement II',
        '/achievement_iii': 'Show achievement III',
    }
    return '\n'.join(f'{cmd:18} - {desc}' for cmd, desc in commands_map.items())


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
shared_game = None


def get_game() -> GameSession:
    global shared_game
    if shared_game is None:
        shared_game = GameSession()
    return shared_game


@bot.event
async def on_ready():
    logger.info('Logged in as %s (%s)', bot.user, bot.user.id)


@bot.command(name='start')
async def start(ctx: commands.Context):
    global shared_game
    shared_game = GameSession()
    await ctx.send('Welcome to the game! Use /help for the command list.')


@bot.command(name='help')
async def help_command(ctx: commands.Context):
    await ctx.send(f'```\n{print_help()}\n```')


@bot.command(name='randomhero')
async def randomhero(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('randomhero')
    await ctx.send(response)


@bot.command(name='stats')
async def stats(ctx: commands.Context):
    game = get_game()
    if not getattr(game, 'hero', None):
        await ctx.send('Start the game first with /start and create a hero with /randomhero.')
        return
    if hasattr(game.hero, 'get_stats'):
        response = game.hero.get_stats()
    else:
        response = game.handle_command('stats')
    await ctx.send(response)


@bot.command(name='shop')
async def shop(ctx: commands.Context):
    game = get_game()
    if hasattr(game, 'shop') and hasattr(game.shop, 'show_items'):
        response = game.shop.show_items()
    else:
        response = game.handle_command('shop')
    await ctx.send(response)


@bot.command(name='buy')
async def buy(ctx: commands.Context, *, item_name: str | None = None):
    game = get_game()
    if not getattr(game, 'hero', None):
        await ctx.send('Create a hero first with /randomhero.')
        return
    if not item_name:
        await ctx.send('Specify an item to buy. Example: /buy iron sword')
        return
    normalized = item_name.strip().lower()
    if hasattr(game, 'shop') and hasattr(game.shop, 'buy_item'):
        response = game.shop.buy_item(game.hero, normalized)
    else:
        response = game.handle_command('buy', normalized)
    await ctx.send(response)


@bot.command(name='dungeon')
async def dungeon(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('dungeon')
    await ctx.send(response)


@bot.command(name='fight')
async def fight(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('fight')
    await ctx.send(response)


@bot.command(name='flee')
async def flee(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('flee')
    await ctx.send(response)


@bot.command(name='next')
async def next_room(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('next')
    await ctx.send(response)


@bot.command(name='search')
async def search(ctx: commands.Context):
    game = get_game()
    response = game.handle_command('search')
    await ctx.send(response)


@bot.command(name='use')
async def use(ctx: commands.Context, *, item_name: str | None = None):
    game = get_game()
    if not getattr(game, 'hero', None):
        await ctx.send('Create a hero first with /randomhero.')
        return
    if not item_name:
        await ctx.send('Specify an item to use. Example: /use healing potion')
        return
    normalized = item_name.strip().lower()
    if hasattr(game.hero, 'use_item'):
        response = game.hero.use_item(normalized)
    else:
        response = game.handle_command('use', normalized)
    await ctx.send(response)


@bot.command(name='achievement_i')
async def achievement_i(ctx: commands.Context):
    game = get_game()
    await ctx.send(game.handle_command('/i'))


@bot.command(name='achievement_ii')
async def achievement_ii(ctx: commands.Context):
    game = get_game()
    await ctx.send(game.handle_command('/ii'))


@bot.command(name='achievement_iii')
async def achievement_iii(ctx: commands.Context):
    game = get_game()
    await ctx.send(game.handle_command('/iii'))


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.exception('Discord bot error', exc_info=error)
    await ctx.send(f'An error occurred: {error}')


if __name__ == '__main__':
    if TOKEN == 'PUT_YOUR_DISCORD_BOT_TOKEN_HERE':
        raise RuntimeError('Set DISCORD_BOT_TOKEN in your environment before running the bot.')
    bot.run(TOKEN)
