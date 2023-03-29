from oslo_config import cfg

DEFAULT_MAGIC_WORD = "CHANGEME!!!"

rpc_group = cfg.OptGroup(
    name="rpc_settings",
    title="RPC Settings for admin <--> web",
)

common_opts = [
    cfg.BoolOpt(
            "trace_enabled",
            default=False,
            help="Enable code tracing",
        ),
]

rpc_opts = [
    cfg.BoolOpt(
        "enabled",
        default=True,
        help="Enable RPC calls",
    ),
    cfg.StrOpt(
        "ip",
        default="localhost",
        help="The ip address to listen on",
    ),
    cfg.PortOpt(
        "port",
        default=18861,
        help="The port to listen on",
    ),
    cfg.StrOpt(
        "magic_word",
        default=DEFAULT_MAGIC_WORD,
        help="Magic word to authenticate requests between client/server",
    ),
]

def register_opts(config):
    config.register_opts(common_opts)
    config.register_group(rpc_group)
    config.register_opts(rpc_opts, group=rpc_group)


def list_opts():
    return {
        "DEFAULT": (common_opts),
        rpc_group.name: rpc_opts,
    }
