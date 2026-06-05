def calculate_bonus(order_total: float, employee_performance: float, rate: float = 0.05) -> float:
    """Calculate employee bonus.
    Args:
        order_total: monetary value of the order.
        employee_performance: a score between 0 and 1 representing performance.
        rate: base bonus rate (default 5%).
    Returns:
        Bonus amount as float, rounded to 2 decimals.
    """
    return round(order_total * rate * employee_performance, 2)
