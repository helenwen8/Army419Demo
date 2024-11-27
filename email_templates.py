def item_stringify(item):
    s = f"Name: {item.get('Name')}"

    if item.get('NSN') or item.get('Serial_Num'):
        s += f" (NSN: {item.get('NSN')}, Serial: {item.get('Serial_Num')})"

    return s


def loan_reminder_template(name, items):
    template = f"""\
Subject: Your Items are Due Soon!


Dear {name},

This is a reminder that the following items will be due soon:
"""

    for item in items:
        template += f"\t- {item_stringify(item)} - Due {item.get('Due_Date')}\n"


    return template