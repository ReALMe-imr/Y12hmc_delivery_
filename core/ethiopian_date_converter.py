class EthiopianDateConverter:
    _ETHIOPIAN_MONTHS = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 5]
    _JD_EPOCH_OFFSET_AMETE_MIHRET = 1723856
    
    @classmethod
    def _is_leap(cls, year):
        """Check if Ethiopian year is leap year."""
        return year % 4 == 3 or year % 4 == -1

    @classmethod
    def to_gregorian(cls, year, month, day):
        """Convert Ethiopian date to Gregorian date."""
        # Ethiopian year difference from Gregorian
        year_diff = 8

        # Convert Ethiopian year to Gregorian year
        gregorian_year = year + year_diff

        # Calculate the Gregorian month and day
        if month <= 4:
            # For Ethiopian months 1-4, add 8 months to get Gregorian month
            gregorian_month = month + 8
            gregorian_year -= 1  # Previous Gregorian year
        elif month <= 12:
            # For Ethiopian months 5-12, subtract 4 months to get Gregorian month
            gregorian_month = month - 4
        else:  # month 13
            gregorian_month = 9  # September
            
        # Adjust for the different number of days in Ethiopian months
        if month != 13:
            gregorian_day = day + 8
            # Adjust for month length
            days_in_month = [31, 28 + (gregorian_year % 4 == 0 and (gregorian_year % 100 != 0 or gregorian_year % 400 == 0)),
                           31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if gregorian_day > days_in_month[gregorian_month - 1]:
                gregorian_day -= days_in_month[gregorian_month - 1]
                gregorian_month += 1
                if gregorian_month > 12:
                    gregorian_month = 1
                    gregorian_year += 1
        else:
            # Special handling for Ethiopian month 13 (Pagume)
            gregorian_day = day + 5
            gregorian_month = 9  # September
            if gregorian_day > 30:
                gregorian_day -= 30
                gregorian_month = 10  # October

        return gregorian_year, gregorian_month, gregorian_day

    @classmethod
    def convert_date(cls, ethiopian_date_str):
        """Convert Ethiopian date string to Gregorian date."""
        try:
            day, month, year = map(int, ethiopian_date_str.split('/'))
            
            if not (1 <= month <= 13):
                raise ValueError("Invalid month")
            
            max_days = cls._ETHIOPIAN_MONTHS[month - 1]
            if month == 13 and cls._is_leap(year):
                max_days = 6
                
            if not (1 <= day <= max_days):
                raise ValueError("Invalid day")
                
            greg_year, greg_month, greg_day = cls.to_gregorian(year, month, day)
            return f"{greg_year}-{greg_month:02d}-{greg_day:02d}"
            
        except (ValueError, IndexError) as e:
            raise ValueError("Invalid Ethiopian date format. Use DD/MM/YYYY")

    @staticmethod
    def is_valid_date(date_str):
        try:
            day, month, year = map(int, date_str.split('/'))
            if month < 1 or month > 13:
                return False
            max_days = EthiopianDateConverter._ETHIOPIAN_MONTHS[month - 1]
            if month == 13 and EthiopianDateConverter._is_leap(year):
                max_days = 6
            if day < 1 or day > max_days:
                return False
            return True
        except (ValueError, IndexError):
            return False