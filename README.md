## De-Identification - Diaz Solution

##Instructions
- Install the following dependencies
    Python 3.7.3
    SQLLite3 v3.2.1, 
    Flask v 1.1.1
    pytest v5.1.0
- Create SqlLite db.
    I used the build-in SQLLite CSV importer and included the db file for convenience. 
- Run application,
    run 'python deidentify_controller.py'

## Testing
To run the tests, run the appropriate command below
'pytest test_deidentify_utils.py'

##Assumptions/Next Steps
- For the notes cleanup, I am assuming that all email address, US social security numbers, or telephone numbers are correct. My code assumes that ssn always contains dashes. My code is assuming that it is not an international number or a letter grouping such as (1-877-Kars4Kids). I am assuming that the numbers will be in year-month-day order. If given more time I would adjust the code to handle these cases.
-  I did not add validation beyond the zipcode due to time and its priority for risk of sql injection. I would add more informative error messages if given more time. 
