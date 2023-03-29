from pathlib import Path

from oslo_config import cfg


slack_opts = [
    cfg.PortOpt(
            "slack_web_port",
            default=3000,
            help="Port to use for incomming connections from slack",
        ),
]

def register_opts(config):
    config.register_opts(slack_opts)


def list_opts():
    return {
        "DEFAULT": (slack_opts),
    }
