import click

from .xls_hydrator import XlsHydrator


def get_hydrators():
    return [xls]


@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
@click.pass_context
def xls(ctx, xls_filename):
    """Import data from an XLS spreadsheet."""

    ctx.obj.name, ctx.obj.entity_map = XlsHydrator(xls_filename).run()
