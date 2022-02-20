""" portfoliocommands """
import click
from beautifultable import BeautifulTable, ALIGN_LEFT
from pprint import pprint

import kytrade.ps.portfolio as ps
from kytrade.cli.ps.tx import tx
from kytrade.cli.ps.strat import strat


def _get_ps_table(portfolios: list):
    """Print a list of portfolios"""
    table = BeautifulTable(maxwidth=120)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    headers = [
        "Name",
        "Start",
        "End",
        "Positions"
    ]
    table.columns.header = headers
    for portfolio in portfolios:
        sp = portfolio.data["stock_positions"]
        positions = ",".join([f"{key}={sp[key]}" for key in sp.keys() ])
        row = [
            portfolio.name,
            portfolio.data["date_opened"],
            str(portfolio.date),
            positions,
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
    ps.create_portfolio(name, date)
    portfolio = ps.get_portfolio(name)
    table = _get_ps_table([portfolio])
    click.echo(table)


@click.command(name="list")
def _list():
    """list instances"""
    portfolios = ps.list_portfolios()
    table = _get_ps_table(portfolios)
    click.echo(table)


@click.argument("name")
@click.command()
def describe(name):
    """Print a detailed overview of a portfolio instance"""
    portfolio = ps.get_portfolio(name)
    click.echo(f"date: {portfolio.date}")
    pprint(portfolio.data)
    return
    # TODO: re-implement this with the new data structure
    table = BeautifulTable(maxwidth=120, default_alignment=ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_COMPACT)
    table.rows.append(["ID", portfolio.id])
    table.rows.append(["Name", portfolio.name])
    table.rows.append(
        ["Compound Anual Growth Rate", f"{portfolio.compound_anual_growth_rate:.2f}%"]
    )
    table.rows.append(["Start Date", str(portfolio.date_opened)])
    table.rows.append(["Simulation Date", str(portfolio.date)])
    table.rows.append(["Days Open", f"{portfolio.days_opened:,}"])
    table.rows.append(["Years Open", f"{portfolio.years_opened:.2f}"])
    table.rows.append(["Book Value", f"${portfolio.total_deposited:,.2f}"])
    table.rows.append(["Market Value", f"${portfolio.value_at_close:,.2f}"])
    table.rows.append(["Total Profit", f"${portfolio.profit:,.2f}"])
    table.rows.append(["Return on Investment", f"{portfolio.return_on_investment:.2f}%"])
    table.rows.append(
        [
            "All-Time Low",
            f"${portfolio.all_time_daily_low.total_usd:,.2f} at {portfolio.all_time_daily_low.date}",
        ]
    )
    table.rows.append(
        [
            "All-Time High",
            f"${portfolio.all_time_daily_high.total_usd:,.2f} at {portfolio.all_time_daily_high.date}",
        ]
    )
    click.echo(table)


@click.argument("name")
@click.command()
def delete(name):
    """Delete a portfolio"""
    ps.delete_portfolio(name)



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
portfolio_simulator.add_command(strat)
portfolio_simulator.add_command(value_history)
