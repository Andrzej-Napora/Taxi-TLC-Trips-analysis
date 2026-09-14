from datetime import date

from dateutil.relativedelta import relativedelta


def generate_date_range(start_date_str,end_date_str):
    """
    Generate a list of year-month strings between start and end dates.
    
    Args:
        start_date_str: Start date in YYYY-MM format
        end_date_str: End date in YYYY-MM format
    
    Returns:
        List of date strings in YYYY-MM format
    """
    start = date.fromisoformat(f"{start_date_str}-01")
    end = date.fromisoformat(f"{end_date_str}-01")
    
    dates = []
    current = start
    while current <= end:
        dates.append(current.strftime("%Y-%m"))
        current += relativedelta(months=1)
    
    return dates