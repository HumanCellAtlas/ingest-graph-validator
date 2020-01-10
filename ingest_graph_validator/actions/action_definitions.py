# -*- coding: utf-8 -*-

"""Action modules for the ingest-graph-validator."""

import click

from .test_action import TestAction


def get_actions():
    return [test]


@click.command()
@click.option("-f", "--fail", is_flag=True, help="Immediately finish with an error status when a test fails.",
              default=False, show_default=True)
@click.pass_context
@click.argument("test_path", type=click.Path(exists=True))
def test(ctx, test_path, fail):
    """Runs graph validation tests in the specified folder."""

    TestAction(ctx.obj.graph, test_path, fail).run()
