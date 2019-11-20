import re
from datetime import datetime, date
import sqlite3
import csv 



def calculate_age(birthDate):
    formated_date = datetime.strptime(birthDate, '%Y-%m-%d')
    today = date.today()
    age = today.year - formated_date.year - ((today.month, today.day) < (formated_date.month, formated_date.day)) 
    if age > 89:
        return "90+" 
    return str(age) 

def csv_reader(zipcode):
    with open('population_by_zcta_2010.csv', newline='') as f:
        reader = csv_reader(f)
        for row in reader:
            print(row)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def zipcode_mask(zipcode):
    return zipcode[:3] 
    
def zipcode_clean(zipcode):
    if len(zipcode) != 5 or not zipcode.isnumeric(): 
        raise ValueError('Incorrect Zipcode')
    conn = sqlite3.connect('population_zip.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    trunc_zipcode = zipcode_mask(zipcode)
    query = "SELECT SUM(population) AS population_sum FROM population_zip WHERE zipcode LIKE \'" + trunc_zipcode + "%\';"
    result = cur.execute(query).fetchall()
    population_sum = result[0]['population_sum'] 
    if population_sum < 20000:
        return "00000"
    else :
        return trunc_zipcode + "00"

def extract_year(date) :
    year = datetime.strptime(date,'%Y-%m-%d').year
    return str(year)  

def replace_date(matches, notes):
    clean_notes = notes
    matches_list = []
    for m in matches:
        start = m.span()[0]
        end = m.span()[1]
        year = extract_year(m.group())
        matches_list.append((year, start, end))
    #process matches list in reverse so replacesments do not
    # affect start indexes later in the string  
    for entry in reversed(matches_list):
        clean_notes = clean_notes[:entry[1]] + str(entry[0]) + clean_notes[entry[2]:]
    return clean_notes
    

def notes_cleanup(notes):
    ssn_pattern = r'\d{3}-\d{2}-\d{4}'
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    phone_pattern = r'(?:\+ *)?\d[\d\- ]{7,}\d'
    year_pattern = r'%Y-%m-%d'
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    #RegEx pattern as raw string to avoid escaped Unicode character depreciation warnings 
    #and syntaxErrors from python 3.7+

    matches = re.finditer(date_pattern, notes)
    cleaned_notes = replace_date(matches, notes)
    ssn_cleaned = re.sub(ssn_pattern, 'XXX-XX-XXXX', cleaned_notes)
    email_cleaned = re.sub(email_pattern, '@email', ssn_cleaned)
    phone_cleaned = re.sub(phone_pattern, '(XXX)-XXX-XXXX', email_cleaned)
    return phone_cleaned