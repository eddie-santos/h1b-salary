import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import BOOLEAN, FLOAT, INTEGER, TEXT, TIMESTAMP

db_url = 'postgresql+psycopg2://localhost:5432/postgres'

dtype = {
    'agent_attorney_city': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'agent_attorney_name': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'agent_attorney_state': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'agent_representing_employer': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'amended_petition': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'case_number': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'case_status': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'case_submitted': {
        'python': 'datetime64[ns]',
        'sqlalchemy': TIMESTAMP
    },
    'change_employer': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'change_previous_employment': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'continued_employment': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'decision_date': {
        'python': 'datetime64[ns]',
        'sqlalchemy': TIMESTAMP
    },
    'employer_address': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_business_dba': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_city': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_country': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_name': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_phone': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_phone_ext': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_postal_code': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_province': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employer_state': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'employment_end_date': {
        'python': 'datetime64[ns]',
        'sqlalchemy': TIMESTAMP
    },
    'employment_start_date': {
        'python': 'datetime64[ns]',
        'sqlalchemy': TIMESTAMP
    },
    'full_time_position': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'h1b_dependent': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'job_title': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'labor_con_agree': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'naics_code': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'new_concurrent_employment': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'new_employment': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'original_cert_date': {
        'python': 'datetime64[ns]',
        'sqlalchemy': TIMESTAMP
    },
    'prevailing_wage': {
        'python': 'float64',
        'sqlalchemy': FLOAT
    },
    'public_disclosure_location': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'pw_source': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'pw_source_other': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'pw_source_year': {
        'python': 'float64',
        'sqlalchemy': FLOAT
    },
    'pw_unit_of_pay': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'pw_wage_level': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'soc_code': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'soc_name': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'source_file': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'support_h1b': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'total_workers': {
        'python': 'int64',
        'sqlalchemy': INTEGER
    },
    'visa_class': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'wage_rate_of_pay_from': {
        'python': 'float64',
        'sqlalchemy': FLOAT
    },
    'wage_rate_of_pay_to': {
        'python': 'float64',
        'sqlalchemy': FLOAT
    },
    'wage_unit_of_pay': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'willful_violator': {
        'python': 'bool',
        'sqlalchemy': BOOLEAN
    },
    'worksite_city': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'worksite_county': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'worksite_postal_code': {
        'python': 'object',
        'sqlalchemy': TEXT
    },
    'worksite_state': {
        'python': 'object',
        'sqlalchemy': TEXT
    }
}

bool_cols = [k for k, v in dtype.items() if v['python'] == 'bool']
file_dir = '/Users/Eddie/projects/h1b-salary/data/'

def parse_date(date):
    month, day, year = date.split('/')
    return year + '-' + month + '-' + day

if __name__ == '__main__':
    engine = create_engine(db_url)
    
    files = ['h1b_2018.xlsx', 'h1b_2017.xlsx', 'h1b_2016.xlsx', 'h1b_2015.xlsx']
    
    for file in files:
        print('loading file: {}'.format(file))
        df = pd.read_excel(file_dir + file)
        print('file loaded, processing')
        df.columns = df.columns.map(lambda x: x.lower().replace('-',''))
        df['source_file'] = [file.split('.')[0]]*df.shape[0]
        db_cols = list(dtype.keys())

        if 'naic_code' in df:
            df['naics_code'] = df['naic_code']
            del df['naic_code']

        for col in db_cols:
            if col not in df:
                df[col] = [None]*df.shape[0]
            if col in bool_cols:
                df[col] = df[col].apply(lambda x: True if x in (1, 'Y', True) else False)

            try:
                df[col] = df[col].astype(dtype[col]['python'])
            except ValueError:
                if dtype[col] == 'datetime64[ns]':
                    df[col] = df[col].apply(parse_date)
                df[col] = df[col].astype(dtype[col]['python'])

        print('writing to database')
        df[db_cols].to_sql('h1b_salary', engine, if_exists='append', index=False, chunksize=5000, dtype={k:v['sqlalchemy'] for k, v in dtype.items()})
        print('file {} complete!'.format(file))
