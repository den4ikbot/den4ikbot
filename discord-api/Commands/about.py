# Microbot Discord bot
# Repo: https://github.com/tinelix/microbot
# Licensed under Apache License 2.0 & GNU Affero General Public License v3.0 and higher

import cpuinfo # for install 'pip install py-cpuinfo'
import psutil
import os
import sys
import platform
import sqlite3

async def generateEmbed(ctx, bot, config, links, language, disnake, translator, python_version):
    msg_embed = disnake.Embed(
        description=translator.translate('embed_description', 'please_wait', language),
        colour=config['accent_def'],
    )
    msg_embed.set_author(name=str(translator.translate('embed_title', 'about', language)))
    return msg_embed

async def editEmbed(ctx, bot, config, links, language, disnake, translator, python_version, uptime):
    try:
        dev = bot.get_user(config['dev_id'])
    except Exception as e:
        print(e)
        dev = None

    try:
        codev = bot.get_user(config['codev_id'])
    except Exception as e:
        print(e)
        codev = None

    plt_system = platform.system()
    plt_version = platform.version()

    if(plt_system == 'Windows'):
        if plt_version.startswith('10.0') and int(plt_version.split('.')[2]) >= 22000:
            os_ver = 'Windows 11 ({0})'.format(plt_version)
        elif plt_version.starstwith('10.0') and int(plt_version.split('.')[2]) >= 10240:
            os_ver = 'Windows 10 ({0})'.format(plt_version)
        elif plt_version.startswith('6.3') and int(plt_version.split('.')[2]) >= 9600:
            os_ver = 'Windows 8.1 ({0})'.format(plt_version)
        elif plt_version.startswith('6.2') and int(plt_version.split('.')[2]) >= 9200:
            os_ver = 'Windows 8 ({0})'.format(plt_version)
        elif plt_version.startswith('6.1') and int(plt_version.split('.')[2]) >= 7601:
            os_ver = 'Windows 7 ({0})'.format(plt_version)
        elif plt_version.startswith('6.0') and int(plt_version.split('.')[2]) >= 6000:
            os_ver = 'Windows Vista ({0})'.format(plt_version)
        elif plt_version.startswith('5.2') and int(plt_version.split('.')[2]) >= 3790:
            os_ver = 'Windows XP x64 / Server 2003 ({0})'.format(plt_version)
        elif plt_version.startswith('5.1') and int(plt_version.split('.')[2]) >= 2600:
            os_ver = 'Windows XP ({0})'.format(plt_version)
        else:
            os_ver = 'Windows ({0})'.format(plt_version)
    else:
        os_ver = '{0} {1}'.format(platform.system(), platform.release())

    if psutil.virtual_memory().available < 1024 or psutil.virtual_memory().total < 1024:
        ram = translator.translate('numb_with_unit', 'kilobytes2', language).format(round(psutil.virtual_memory().used / 1024, 2), round(psutil.virtual_memory().total / 1024, 2))
    elif (psutil.virtual_memory().available < 1048576 and psutil.virtual_memory().available >= 1024) or (psutil.virtual_memory().total < 1048576 and psutil.virtual_memory().total >= 1024):
        ram = translator.translate('numb_with_unit', 'megabytes2', language).format(round(psutil.virtual_memory().used / 1024 / 1024, 2), round(psutil.virtual_memory().total / 1024 / 1024, 2))
    else:
        ram = translator.translate('numb_with_unit', 'gigabytes2', language).format(round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 2), round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2))

    msg_embed = disnake.Embed(
        colour=config['accent_def']
    )
    msg_embed.set_author(name=str(translator.translate('embed_title', 'about', language)))
    msg_embed.add_field(
        translator.translate('embed_fields', 'about_versf', language), translator.translate('embed_fields', 'about_versv', language).format(config['version'], config['version_date']), inline=True
    )
    if(dev == None):
        pass
    else:
        if(codev == None):
            msg_embed.add_field(
                translator.translate('embed_fields', 'about_devsf', language), translator.translate('embed_fields', 'about_devsv', language).format(dev.name, dev.discriminator), inline=True
            )
        else:
            msg_embed.add_field(
                translator.translate('embed_fields', 'about_devsf2', language), translator.translate('embed_fields', 'about_devsv2', language).format(dev.name, dev.discriminator, codev.name, codev.discriminator), inline=True
            )
    msg_embed.add_field(
        translator.translate('embed_fields', 'about_regdf', language), translator.translate('embed_fields', 'about_regdv', language).format(translator.formatDate(bot.user.created_at, 'normal', language)), inline=True
    )
    msg_embed.add_field(
        translator.translate('embed_fields', 'about_statsf', language), translator.translate('embed_fields', 'about_statsv', language).format(len(bot.guilds), len(bot.users)), inline=True
    )
    msg_embed.add_field(
        translator.translate('embed_fields', 'about_uptimef', language), translator.translate('embed_fields', 'about_uptimev', language).format(uptime), inline=True
    )
    msg_embed.add_field(
        translator.translate('embed_fields', 'about_basedf', language), translator.translate('embed_fields', 'about_basedv', language).format(python_version(), disnake.__version__, sqlite3.sqlite_version), inline=True
    )

    msg_embed.add_field(
        translator.translate('embed_fields', 'about_hardwf', language), translator.translate('embed_fields', 'about_hardwv', language).format(cpuinfo.get_cpu_info()['brand_raw'], round(cpuinfo.get_cpu_info()['hz_advertised'][0] / 1000000, 2), ram, os_ver), inline=False
    )

    links_str = ''

    if(len(links['invite']) > 0):
        links_str += "{0}\r\n".format(translator.translate('embed_fields', 'about_linksv', language).format(links['invite']))
    if(len(links['website']) > 0):
        links_str += "{0}\r\n".format(translator.translate('embed_fields', 'about_linksv2', language).format(links['website']))
    if(len(links['youtube']) > 0):
        links_str += "{0}\r\n".format(translator.translate('embed_fields', 'about_linksv5', language).format(links['youtube']))
    if(len(links['repo']) > 0):
        links_str += "{0}\r\n".format(translator.translate('embed_fields', 'about_linksv3', language).format(links['repo']))
    if(len(links['support']) > 0):
        links_str += "{0}\r\n".format(translator.translate('embed_fields', 'about_linksv4', language).format(links['support']))
    if(len(links_str) > 0):
        msg_embed.add_field(
            translator.translate('embed_fields', 'about_linksf', language), links_str, inline=True
        )

    msg_embed.set_footer(text='Copyright © 2022 Dmitry Tretyakov (aka. Tinelix) & Den4ik')
    return msg_embed

async def sendSlashMsg(ctx, bot, config, links, language, disnake, translator, python_version, uptime):
    await ctx.response.defer()
    msg_embed = await editEmbed(ctx, bot, config, links, language, disnake, translator, python_version, uptime)
    await ctx.send(embed=msg_embed)

async def sendRegularMsg(ctx, bot, config, links, language, disnake, translator, python_version, uptime):
    msg_embed = await generateEmbed(ctx, bot, config, links, language, disnake, translator, python_version)
    msg = await ctx.reply(embed=msg_embed, mention_author=False)
    msg_embed_2 = await editEmbed(ctx, bot, config, links, language, disnake, translator, python_version, uptime)
    await msg.edit(embed=msg_embed_2)
