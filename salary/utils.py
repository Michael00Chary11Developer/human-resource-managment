from decimal import Decimal


def calculate_gross_salary(
    base_salary,
    housing_allowance,
    child_allowance,
    food_allowance,
    number_of_child,
    marital_status: str,
):
    """
    Calculate the gross salary based on various allowances and marital status.

    Args:
        base_salary (Decimal): The basic salary of the personnel.
        housing_allowance (Decimal): The allowance for housing.
        child_allowance (Decimal): The allowance for each child.
        food_allowance (Decimal): The allowance for food.
        number_of_child (int or None): The number of children the personnel has.
        marital_status (str): The marital status of the personnel ('single' or 'married').

    Returns:
        Decimal: The total gross salary calculated.

    Notes:
        If the marital status is 'single' or if the personnel is 'married' but has no children
        (i.e., number_of_child is 0 or None), the child allowance is not included in the calculation.
    """

    if marital_status != "married" or (
        marital_status == "married" and number_of_child in [0, None]
    ):
        return base_salary + housing_allowance + food_allowance

    child_allowance = child_allowance if child_allowance is not None else Decimal(0)

    return (
        base_salary
        + housing_allowance
        + (number_of_child * child_allowance)
        + food_allowance
    )


def calculate_net_salary(gross_salary, tax_rate=Decimal("0.1")):
    """
    Calculate the net salary after applying a tax rate.

    Args:
        gross_salary (Decimal): The total gross salary.
        tax_rate (Decimal, optional): The tax rate to be applied. Default is 10%.

    Returns:
        Decimal: The net salary after tax deduction.
    """

    return gross_salary * (Decimal(1) - tax_rate)
