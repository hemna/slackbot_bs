import logging
import random
import tabulate


LOG = logging.getLogger(__name__)

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

dynamic_map = {
    "hello": {
        "short": "hi",
        "flip": HI_LIST,
        "desc": "Hellow TF!",
    },

    "battle": {
        "short": None,
        "flip": "(╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)",
        "desc": "Time to battle!"
    },

    "covfefe": {
        "short": "c",
        "flip": "༼ノಠل͟ಠ༽ノ ︵ ┻━┻",
        "desc": "Trump covfefe TF!"
    },

    "dude": {
        "short": "d",
        "flip": "(╯°Д°）╯︵ /(.□ . )",
        "desc": "Dude....."
    },

    "fat": {
        "short": None,
        "flip": "(ノ ゜Д゜)ノ ︵ ┻━┻",
        "desc": "Fat MF'ing TF!"
    },

    "finger": {
        "short": "f",
        "flip": "╭∩╮◕ل͜◕)╭∩╮  ︵┻┻",
        "desc": "Give em the finger!",
    },

    "hercules": {
        "short": "h",
        "flip": "(/ .□.) ︵╰(゜Д゜)╯︵ /(.□. )",
        "desc": "Super herculean TF",
    },
    "jedi": {
        "short": "j",
        "flip": "(._.) ~ ︵ ┻━┻",
        "desc": "Use the force Luke!"
    },

    "magic": {
        "short": "m",
        "flip": "༼∩ຈل͜ຈ༽つ━☆ﾟ.*･｡ﾟ ︵ ┻━┻",
        "desc": "Magic TF!"
    },

    "rage": {
        "short": "r",
        "flip": "(ノಠ益ಠ)ノ彡┻━┻",
        "desc": "Super pissed TF!"
    },
    "table": {
        "short": "t",
        "flip": "(╯°□°)╯︵ ┻━┻",
        "desc": "Flip the standard table"
    },

    "bear": {
        "short": "b",
        "flip": "ʕノ•ᴥ•ʔノ ︵ ┻━┻",
        "desc": "Awe, a cute cuddle TF"
    },

}


def _help(nick, text):

    help_list = []
    for flip in sorted(dynamic_map.keys()):
        flip_type = type(dynamic_map[flip]['flip'])
        if flip_type is str:
            flip_str = dynamic_map[flip]['flip']
        elif flip_type is list:
            dynamic_map[flip]['flip'][0]

        help_list.append(
            [flip, dynamic_map[flip]['short'],
             dynamic_map[flip]['desc'], flip_str]
        )

    flip_table = tabulate.tabulate(
        help_list, headers=['Name', 'Short', 'Description', 'flip'])

    msg = (
        "```\n"
        "Welcome to Table flipping bot.  (╯°□°)╯︵ ┻━┻ \n"
        "Type /tf <command>\n"
        "Commands\n"
        "{}\n"
        "```".format(flip_table)
    )

    return msg


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


def get_flip(key):
    try:
        flip = dynamic_map[key]
        return flip
    except Exception as e:
        # see if there is a shorthand
        for f in dynamic_map:
            if dynamic_map[f]['short'] == key:
                return dynamic_map[f]
        raise e


def tf(nick, text):
    """Send a table flip to a channel."""

    try:
        flip = get_flip(text)
    except Exception as e:
        LOG.exception(e)
        msg = "I don't know what you want me to do"
        msg = "{}\n {}".format(msg,
                               _help(nick, text))
    else:
        flipit = flip['flip']
        flip_type = type(flipit)
        if flip_type is list:
            flipit = flipit[random.randint(0, len(flipit)-1)]
        msg = _build_msg(nick,flipit)

    return msg
