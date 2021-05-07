SPOTIFY = "spotify"
REDDIT = "reddit"
GITHUB = "github"
DISCORD = "discord"
MAIL = "email"
TWITCH = "twitch"
SMS = "sms"

from reaction.mail import mailbox
from reaction.spotify import spotify_parser
from reaction.github import github_parser
from reaction.reddit import reddit_parser
from reaction.discord import discord_parser
from reaction.sms import sms_sender
from reaction.twitch import twitch_parser

MAP_REACTION = {
    SPOTIFY: spotify_parser,
    REDDIT: reddit_parser,
    GITHUB: github_parser,
    DISCORD: discord_parser,
    MAIL: mailbox,
    SMS: sms_sender,
    TWITCH: twitch_parser,
}