import random

HI_LIST = [
    "( ･ω･)ﾉ",
    "( ^_^)／",
    "(^o^)/",
    "( ´ ▽ ` )ﾉ",
    "(=ﾟωﾟ)ﾉ",
    "( ・_・)ノ",
    "(。･∀･)ﾉ",
    "(*ﾟ͠ ∀ ͠)ﾉ",
    "(♦亝д 亝)ﾉ",
    "( *՞ਊ՞*)ﾉ",
    "(｡Ő▽Ő｡)ﾉﾞ",
    "(ஐ╹◡╹)ノ",
    "(✧∇✧)╯",
    "(^▽^)/ ʸᵉᔆᵎ",
    "(。･д･)ﾉﾞ",
    "(◍˃̶ᗜ˂̶◍)ﾉ”",
    "(*´･д･)ﾉ",
    "|。･ω･|ﾉ",
    "(ه’́⌣’̀ه )／",
    "ヽ(´･ω･`)､",
    "ヘ(°￢°)ノ",
    "＼(-_- )",
    "(¬_¬)ﾉ",
    "(;-_-)ノ",
    "(^-^*)/",
    "＼( ･_･)",
    "ヾ(-_-;)",
    "|ʘ‿ʘ)╯"
]

# Map the .tf <command> to a function
COMMAND_MAPPING = {
    "help": "_help",

    "hi": "_hello",
    "hello": "_hello",

    "battle": "_battle",
    "b": "_battle",

    "covfefe": "_covfefe",
    "c": "_covfefe",

    "dude": "_dude",
    "d": "_dude",

    "fat": "_fat",
    "f": "_fat",

    "finger": "_finger",
    "g": "_finger",

    "hercules": "_hercules",
    "h": "_hercules",

    "jedi": "_jedi",
    "j": "_jedi",

    "magic": "_magic",
    "m": "_magic",

    "rage": "_rage",
    "r": "_rage",

    "table": "_table",
    "t": "_table",

    "bear": "_bear",
    "z": "_bear",
}


def _help(nick, text):
    #flip = formatting.color("(╯°□°)╯︵ ┻━┻ ", formatting.colors.RED)
    msg = (
        "```\n"
        "Welcome to Table flipping bot.  (╯°□°)╯︵ ┻━┻ \n"
        "Type /tf <command>\n"
        "Commands\n"
        "help                 - This help\n"
        "hi                   - Hello Table Flip!\n"
        "covfefe (c)          - Covfefe table flip\n"
        "fat (f)              - Fat table flip\n"
        "finger (g)           - The finger table flip\n"
        "jedi (j)             - Jedi table flip.\n"
        "hercules (h)         - Herculese table flip\n"
        "magic (m)            - Magic table flip\n"
        "rage (r)             - Rage table flip\n"
        "table (t)            - Standard table flip\n"
        "bear (b)             - Bear table flip\n"
        "```"

    )
    #bot.say(flip)
    #bot.say("@!           - Hello.")
    #bot.say("@!b <nick>   - Battle another nick table flip.")
    ##bot.say("@!c          - Covfefe table flip.")
    #bot.say("@!d <nick>   - Battle win another nick table flip.")
    #bot.say("@!f          - Fat table flip.")
    #bot.say("@!g          - The Finger table flip.")
    #bot.say("@!h          - Hercules table flip.")
    #bot.say("@!j          - Jedi table flip.")
    #bot.say("@!m          - Magic table flip.")
    #bot.say("@!r          - Rage table flip.")
    #bot.say("@!t          - Standard table flip.")
    #bot.say("@!z          - Bear table flip.")

    return msg


#def _prep_colors(nick, flip):
#    return (formatting.color(nick, formatting.colors.BLUE),
#            formatting.color(flip, formatting.colors.RED))


def _build_msg(nick, flip, replace_str=None):
    #nick, flip = _prep_colors(trigger.nick, flip)
    msg = "%s   *%s*" % (nick, flip)
    #if replace_str and trigger:
    #    other = str(trigger).replace(replace_str, '')
    #    return msg + other
    #else:
    return msg


def _hello(nick, text):
    index = random.randint(0, len(HI_LIST) - 1)
    # flip = hi_list[index].decode("utf-8")
    flip = HI_LIST[index]
    msg = _build_msg(nick, flip)
    return msg


def hello(nick, text):
    return _hello(nick, text)


def _covfefe(nick, text):
    flip = "༼ノಠل͟ಠ༽ノ ︵ ┻━┻"
    return _build_msg(nick, flip)


def _fat(nick, text):
    flip = "(ノ ゜Д゜)ノ ︵ ┻━┻"
    return _build_msg(nick, flip)


def _finger(nick, text):
    flip = "╭∩╮◕ل͜◕)╭∩╮  ︵┻┻"
    return _build_msg(nick, flip)


def _hercules(nick, text):
    flip = "(/ .□.) ︵╰(゜Д゜)╯︵ /(.□. )"
    return _build_msg(nick, flip)


def _jedi(nick, text):
    flip = "(._.) ~ ︵ ┻━┻"
    return _build_msg(nick, flip)


def _magic(nick, text):
    flip = "༼∩ຈل͜ຈ༽つ━☆ﾟ.*･｡ﾟ ︵ ┻━┻"
    return _build_msg(nick, flip)


def _rage(nick, text):
    flip = "(ノಠ益ಠ)ノ彡┻━┻"
    return _build_msg(nick, flip)


def _table(nick, text):
    flip = "(╯°□°)╯︵ ┻━┻ "
    return _build_msg(nick, flip)

def _bear(nick, text):
    flip = "ʕノ•ᴥ•ʔノ ︵ ┻━┻"
    return _build_msg(nick, flip)


def tf(nick, text):
    """Send a table flip to a channel."""

    try:
        func = COMMAND_MAPPING[text]
    except Exception as e:
        msg = "I don't know what you want me to do"
        msg = "{}\n {}".format(msg,
                               _help(nick, text))
    else:
        msg = globals()[func](nick, text)

    return msg
