""" portfoliocommands """
import click
from beautifultable import BeautifulTable, ALIGN_LEFT

import kytrade.portfolio_simulator as ps
from kytrade.cli.ps.tx import tx


def _get_ps_table(portfolios: list):
    """Print a list of portfolios"""
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = [
        "ID",
        "Name",
        "Start",
        "End",
        "Positions",
        "CAGR",
        "ROI",
    ]
    table.columns.header = headers
    for portfolio in portfolios:
        positions = ", ".join([f"{pos.ticker}({pos.qty})" for pos in portfolio.stock_positions])
        row = [
            portfolio.id,
            portfolio.name,
            str(portfolio.date_opened),
            str(portfolio.date),
            positions,
            f"{portfolio.compound_anual_growth_rate:,.2f}%",
            f"{portfolio.return_on_investment:.2f}%",
        ]
        table.rows.append(row)
    return table


@click.group(name="ps")
def portfolio_simulator():
    """Portfolio Simulator"""


@click.option("--date", "-d", required=True, help="Start date  YYYY-MM-DD")
@click.argument("name")
@click.command()
def create(name, date):
    """Create a simulated portfolio instance"""
    portfolio = ps.Portfolio(name, date)
    portfolio.save()
    table = _get_ps_table([portfolio])
    click.echo(table)


@click.command(name="list")
def _list():
    """list instances"""
    portfolios = ps.list_portfolios()
    table = _get_ps_table(portfolios)
    click.echo(table)


@click.argument("id")
@click.command()
def describe(id):
    """Print a detailed overview of a portfolio instance"""
    portfolio = ps.Portfolio.load(id)
    table = BeautifulTable(maxwidth=120, default_alignment=ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.rows.append(["ID", portfolio.id])
    table.rows.append(["Name", portfolio.name])
    table.rows.append(["Compound Anual Growth Rate", f"{portfolio.compound_anual_growth_rate:.2f}%"])
    table.rows.append(["Start Date", str(portfolio.date_opened)])
    table.rows.append(["Simulation Date", str(portfolio.date)])
    table.rows.append(["Days Open", f"{portfolio.days_opened:,}"])
    table.rows.append(["Years Open", f"{portfolio.years_opened:.2f}"])
    table.rows.append(["Book Value", f"${portfolio.total_deposited:,.2f}"])
    table.rows.append(["Market Value", f"${portfolio.value_at_close:,.2f}"])
    table.rows.append(["Total Profit", f"${portfolio.profit:,.2f}"])
    table.rows.append(["Return on Investment", f"{portfolio.return_on_investment:.2f}%"])
    table.rows.append(["All-Time Low", f"${portfolio.all_time_daily_low.total_usd:,.2f} at {portfolio.all_time_daily_low.date}"])
    table.rows.append(["All-Time High", f"${portfolio.all_time_daily_high.total_usd:,.2f} at {portfolio.all_time_daily_high.date}"])
    click.echo(table)


@click.argument("id")
@click.command()
def delete(id):
    """Delete a portfolio"""
    ps.Portfolio.load(id).delete()
    click.echo(f"Done")


@click.option("--print-status/--no-print-status", default=True, help="Print sim status")
@click.option("--to-date", "-d", required=False, default=None, help="Advance to date YYYY-MM-DD")
@click.argument("id")
@click.command()
def advance(id, to_date, print_status):
    """Advance the ps 1 day or to --to-date"""
    portfolio = ps.Portfolio.load(id)
    if to_date:
        click.echo(f"Simulating daily activities to {to_date}...")
        portfolio.advance_to_date(to_date, print_status=print_status)
        click.echo("")
    else:
        portfolio.advance_one_day()
    click.echo("Saving....")
    portfolio.save()


@click.option("--table/--csv", default=True, help="Use --csv to print a CSV")
@click.argument("id")
@click.command()
def value_history(id, table):
    """Print the balance history"""
    portfolio = ps.Portfolio.load(id)
    if table:
        table = BeautifulTable(maxwidth=80)
        table.set_style(BeautifulTable.STYLE_MARKDOWN)
        headers = ["date", "mkt_val", "profit"]
        table.columns.header = headers
        for entry in portfolio.value_history:
            row = [str(entry.date), entry.total_usd, entry.profit_usd]
            table.rows.append(row)
        click.echo(table)
    else:
        click.echo("date,mkt_val,profit")
        for entry in portfolio.value_history:
            click.echo(f"{entry.date},{entry.total_usd},{entry.profit_usd}")


portfolio_simulator.add_command(create)
portfolio_simulator.add_command(_list)
portfolio_simulator.add_command(describe)
portfolio_simulator.add_command(delete)
portfolio_simulator.add_command(advance)
portfolio_simulator.add_command(tx)
portfolio_simulator.add_command(value_history)
