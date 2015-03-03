import os
import numpy as np
from pandas import DataFrame

from django.conf import settings


class PensionCalculator(object):
    """
    Initial Pension Calculator Class

    FIXME: Consider changing all column indices to ints instead of strings.
    """

    def __init__(self, retirement_age=65, discount_rate=0.775, calculate_through_year=2115):
        # FIXME: Eventually, this will transition to a Database rather than file systems.
        csv_folder = os.path.join(settings.BASE_DIR, 'apps', 'calculator',
            'onetime_scripts', 'csv_data')

        activemembers_file = os.path.join(csv_folder, 'ILPR_1.0_activemembers.csv') # Constant over time; varies by age
        annuitants_file = os.path.join(csv_folder, 'ILPR_1.0_annuitants.csv') # Constant over time; varies by age
        income_file = os.path.join(csv_folder, 'ILPR_1.0_income.csv') # Varies over time; constant by age
        payment_file = os.path.join(csv_folder, 'ILPR_1.0_payment.csv') # Varies over time; constant by age
        servicetable_file = os.path.join(csv_folder, 'ILPR_1.0_servicetable.csv') # Varies by years of service
        yearsofservice_file = os.path.join(csv_folder, 'ILPR_1.0_yearsofservice.csv') # Constant over time; varies by age

        self.activemembers_df = DataFrame.from_csv(activemembers_file)
        self.annuitants_df = DataFrame.from_csv(annuitants_file)
        self.income_df = DataFrame.from_csv(income_file)
        self.payment_df = DataFrame.from_csv(payment_file)
        self.servicetable_df = DataFrame.from_csv(servicetable_file)
        self.yearsofservice_df = DataFrame.from_csv(yearsofservice_file)

        self.base_year = 2014
        self.life_expectancy = 85
        self.life_expectancy_after_retirement = self.life_expectancy - retirement_age
        self.percentage_of_final_salary = 0.0167
        self.discount_rate = discount_rate
        self.inflation_rate = .03
        self.calculate_through_year = calculate_through_year


    def _copy_df_values_to_future(self, df):
        for i in xrange(self.base_year + 1, self.calculate_through_year + 1):
            df[str(i)] = df[str(self.base_year)]
        return df

    def _build_cumulative_growth_df(self, growth_rate):
        """
        Given a `growth_rate` (float), return a df that looks as follows:

        (Assume a 0.03 value for growth_rate)
        Age     2014    2015    2016 ...    2115
        0       1.0     1.03    1.0609      19.759
        1       1.0     1.03    1.0609      19.759
        2       1.0     1.03    1.0609      19.759
        ...
        85      1.0     1.03    1.0609      19.759

        Where each row contains (1 + growth_rate)^n where n is the number
        of years that have passed between 2014 and the column in which the
        cell resides.
        """
        ages = range(0, self.life_expectancy + 1)
        # Create dataframe dict from one year in the future to the end of our time.
        columns = xrange(self.base_year + 1, self.calculate_through_year + 1)
        data = {str(col): [1 + growth_rate] * len(ages) for col in columns}
        data.update({str(self.base_year): np.float64(1)})
        raw_growth_rate_df = DataFrame(data=data, index=ages)
        # This takes the annual growth rates for each year
        # and multiples them together to get the cumulative
        # growth rates. The "T" is the transpose operator, and we
        # need to do this because our standard index is age, not time.
        growth_df = raw_growth_rate_df.T.cumprod().T

        return growth_df.reindex_axis(sorted(growth_df.columns), axis=1)

    def activemembers_build_future(self, **kwargs):
        """
        Takes the 2014 actual activemembers numbers by age and
        builds a reasonable future based on **kwargs
        """
        self.activemembers_df = self._copy_df_values_to_future(self.activemembers_df)
        return self.activemembers_df

    def annuitants_build_future(self, **kwargs):
        """
        Takes the 2014 actual annuitants numbers by age and
        builds a reasonable future based on **kwargs
        """
        self.annuitants_df = self._copy_df_values_to_future(self.annuitants_df)
        return self.annuitants_df

    def income_build_future(self, inflation_rate):
        """
        Takes the 2014 actual income numbers by age and
        builds a reasonable future based on the assumed
        inflation rate.
        """
        # Get cumulative inflation over time
        inflation_df = self._build_cumulative_growth_df(growth_rate=inflation_rate)
        # Build out future income from present (in present present value dollars)
        temp_income_df = self._copy_df_values_to_future(self.income_df)
        # Adjust to future-value dollars
        self.income_df = temp_income_df * inflation_df
        return self.income_df

    def payment_build_future(self, cola):
        """
        Takes the 2014 actual payment numbers by age and
        builds a reasonable future based on the assumed
        cola, which can vary over time.
        """
        # Get cumulative cola over time
        cola_df = self._build_cumulative_growth_df(growth_rate=cola)
        # Build out future payments from present (in present present value dollars)
        temp_income_df = self._copy_df_values_to_future(self.payment_df)
        # Adjust to future-value dollars
        self.payment_df = temp_income_df * cola_df
        return self.payment_df

    def yearsofservice_build_future(self, **kwargs):
        """
        Takes the 2014 actual yearsofservice numbers by age and
        builds a reasonable future based on the assumed kwargs.
        """
        self.yearsofservice_df = self._copy_df_values_to_future(self.yearsofservice_df)
        return self.yearsofservice_df