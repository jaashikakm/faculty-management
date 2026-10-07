from datetime import date
from decimal import Decimal
from django.db.models import Sum
from .models import LeaveApplication, LeaveStatus, LeaveType

# Institutional rule used in this project:
# Leave year = June 1 through May 31 of the following year.
ANNUAL_LIMITS = {
    LeaveType.EL: Decimal("12"),
    LeaveType.ML: Decimal("6"),
}
MONTHLY_LIMITS = {
    LeaveType.CL: Decimal("1"),
    LeaveType.PERMISSION: Decimal("2"),  # permission units, measured in hours
}

def leave_year_bounds(day=None):
    day = day or date.today()
    if day.month >= 6:
        return date(day.year, 6, 1), date(day.year + 1, 5, 31)
    return date(day.year - 1, 6, 1), date(day.year, 5, 31)

def overlap_days(start1, end1, start2, end2):
    start = max(start1, start2)
    end = min(end1, end2)
    return max(0, (end - start).days + 1)

def annual_used(faculty, leave_type, as_of):
    year_start, year_end = leave_year_bounds(as_of)
    total = Decimal("0")
    qs = LeaveApplication.objects.filter(
        faculty=faculty,
        leave_type=leave_type,
        status__in=[LeaveStatus.PENDING, LeaveStatus.APPROVED],
        from_date__lte=year_end,
        to_date__gte=year_start,
    )
    for leave in qs:
        if leave_type == LeaveType.PERMISSION:
            total += leave.permission_hours
        else:
            total += Decimal(str(overlap_days(
                leave.from_date, leave.to_date, year_start, year_end
            )))
    return total

def monthly_used(faculty, leave_type, year, month):
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1)
    else:
        month_end = date(year, month + 1, 1)
    qs = LeaveApplication.objects.filter(
        faculty=faculty,
        leave_type=leave_type,
        status__in=[LeaveStatus.PENDING, LeaveStatus.APPROVED],
        from_date__lt=month_end,
        to_date__gte=month_start,
    )
    total = Decimal("0")
    for leave in qs:
        if leave_type == LeaveType.PERMISSION:
            total += leave.permission_hours
        else:
            total += Decimal(str(overlap_days(
                leave.from_date, leave.to_date,
                month_start, month_end - __import__("datetime").timedelta(days=1)
            )))
    return total

def leave_balance(faculty, leave_type, as_of=None):
    as_of = as_of or date.today()
    if leave_type == LeaveType.CL:
        used = monthly_used(faculty, leave_type, as_of.year, as_of.month)
        return MONTHLY_LIMITS[leave_type] - used
    if leave_type == LeaveType.PERMISSION:
        used = monthly_used(faculty, leave_type, as_of.year, as_of.month)
        return MONTHLY_LIMITS[leave_type] - used
    used = annual_used(faculty, leave_type, as_of)
    return ANNUAL_LIMITS[leave_type] - used

def validate_leave_request(faculty, leave_type, start, end, permission_hours=Decimal("0")):
    if end < start:
        return False, "To date cannot be before From date."

    if leave_type == LeaveType.PERMISSION:
        if start != end:
            return False, "Permission must be requested for one date."
        if permission_hours <= 0 or permission_hours > 1:
            return False, "Permission must be up to 1 hour per request."
        balance = leave_balance(faculty, leave_type, start)
        if permission_hours > balance:
            return False, f"Permission limit exceeded. Remaining this month: {balance} hour(s)."
        return True, "Valid"

    days = Decimal((end - start).days + 1)

    # CL must remain within one calendar month because the entitlement is 1 per month.
    if leave_type == LeaveType.CL:
        if start.month != end.month or start.year != end.year:
            return False, "CL cannot span multiple months."
        balance = leave_balance(faculty, leave_type, start)
        if days > balance:
            return False, f"CL limit exceeded. Remaining this month: {balance} day(s)."
        return True, "Valid"

    if leave_type in [LeaveType.EL, LeaveType.ML]:
        year_start, year_end = leave_year_bounds(start)
        if start < year_start or end > year_end:
            return False, "Leave must fall within the current June-to-May leave year."
        balance = leave_balance(faculty, leave_type, start)
        if days > balance:
            return False, f"{leave_type} limit exceeded. Remaining: {balance} day(s)."
        return True, "Valid"

    return False, "Invalid leave type."
