import click
import importlib.metadata as imp
from importlib.metadata import version as metadata_version
import logging
import sys

from oslo_config import cfg, generator

import slackbot_bs

LOG = logging.getLogger(__name__)
CONF = cfg.CONF

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    pass

def main():
    # First import all the possible commands for the CLI
    # The commands themselves live in the cmds directory
    from .cmds import (  # noqa
        slack,
    )
    cli()


@cli.command()
@click.pass_context
def sample_config(ctx):
    """Generate a sample Config file from aprsd and all installed plugins."""

    def get_namespaces():
        args = []

        all = imp.entry_points()
        selected = []
        if "oslo.config.opts" in all:
            for x in all["oslo.config.opts"]:
                if x.group == "oslo.config.opts":
                    selected.append(x)
        for entry in selected:
            if "slackbot_bs" in entry.name:
                args.append("--namespace")
                args.append(entry.name)

        return args

    args = get_namespaces()
    config_version = metadata_version("oslo.config")
    logging.basicConfig(level=logging.WARN)
    conf = cfg.ConfigOpts()
    generator.register_cli_opts(conf)
    try:
        conf(args, version=config_version)
    except cfg.RequiredOptError:
        conf.print_help()
        if not sys.argv[1:]:
            raise SystemExit
        raise
    generator.generate(conf)


@cli.command()
@click.pass_context
def version(ctx):
    """Show the APRSD version."""
    click.echo(click.style("APRSD slackbot Version : ", fg="white"), nl=False)
    click.secho(f"{slackbot_bs.__version__}", fg="yellow", bold=True)


if __name__ == "__main__":
    main()  # pragma: no cover
