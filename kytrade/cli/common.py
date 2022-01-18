"""Common CLI functions"""
from beautifultable import BeautifulTable


def get_table(data: list):
    """Get a nicely formatted table from a list of ORM objects"""
    if not data:
        return ""
    print(data[0])
    headers = ["id"] + [key for key in data[0].__dict__.keys() if not key.startswith("_")]
    table = BeautifulTable(maxwidth=100)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.columns.header = headers
    for element in data:
        row = []
        for header in headers:
            row.append(str(getattr(element, header)))
        table.rows.append(row)
    return table
