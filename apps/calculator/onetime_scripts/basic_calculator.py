import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pensioncalc.settings')

# Shows how to use the basic calculator.

# Import the calculator class
from apps.calculator.executor.basic_calculator import PensionCalculator

# Instantiate a calculator
calculator = PensionCalculator()

# Build the future
calculator.activemembers_build_future()
calculator.annuitants_build_future()
calculator.income_build_future()
calculator.payment_build_future()
calculator.yearsofservice_build_future()

# Check that the future exists
print calculator.activemembers_df
print calculator.annuitants_df
print calculator.income_df
print calculator.payment_df
print calculator.yearsofservice_df

# Next steps - create some cool calculations for net contributions, etc.