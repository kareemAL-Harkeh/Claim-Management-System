from celery import Celery
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Claim 

app1 = Celery('Cliams')


app1.conf.broker_url = "redis://localhost:6379/0"

app1.conf.result_backend = "redis://localhost:6379/0"

app1.conf.task_ignore_result = False


DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app1.task
def generate_claim_report():
    db = SessionLocal()
    claims = db.query(Claim).all()

    report_data = {}
    for claim in claims:
        if claim.status not in report_data:
            report_data[claim.status] = 0
        report_data[claim.status] += claim.claim_amount

    df = pd.DataFrame(report_data.items(), columns=['Status', 'Total Amount'])
    
    csv_file_path = 'claims_report.csv'
    df.to_csv(csv_file_path, index=False)

    db.close()
    return csv_file_path

if __name__ == '__main__':
    app1.start()
