from tracemalloc import start
import boto3,json
from datetime import datetime, timedelta
from dateutil import relativedelta
import os

dollar_exchange_rate = float(1)


def getMonthBill():
    client = boto3.client('ce')

    today = datetime.today()
    start_date = datetime.strftime(
        today + relativedelta.relativedelta(day=1), '%Y-%m-%d')

    end_date = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
    print("start_date " + start_date)
    print("end_date " + end_date)
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=[
            'UnblendedCost'
        ],
        GroupBy=[{
            'Type': 'DIMENSION',
            'Key': 'LEGAL_ENTITY_NAME'
        }
        ]
    )


    month_to_date_bill = round(float(
        response["ResultsByTime"][0]['Groups'][0]["Metrics"]["UnblendedCost"]["Amount"]) * dollar_exchange_rate)
    return month_to_date_bill
    # return response

def getYesterdayBill():
    client = boto3.client('ce')

    start_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    end_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

    print("start_date " + start_date)
    print("end_date " + end_date)

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=[
            'UnblendedCost'
        ],
        GroupBy=[{
            'Type': 'DIMENSION',
            'Key': 'LEGAL_ENTITY_NAME'
        }
        ]
    )

    yesterdays_bill = round(float(
        response["ResultsByTime"][0]["Groups"][0]['Metrics']["UnblendedCost"]["Amount"]))*dollar_exchange_rate
    return yesterdays_bill
    # return response

def predictedBill():
    client = boto3.client('ce')

    client = boto3.client('ce')
    start_date = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')

    today = datetime.today()

    #start_date = datetime.strftime( today + relativedelta.relativedelta(day=1) , '%Y-%m-%d')
    end_date = datetime.strftime(
        today + relativedelta.relativedelta(months=1, day=1), '%Y-%m-%d')
    print("start_date " + start_date)
    print("end_date " + end_date)
    response = client.get_cost_forecast(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Metric='UNBLENDED_COST',
        Granularity='MONTHLY'
    )

    return round(float(response['Total']['Amount']) * dollar_exchange_rate)
    # return response

print(getYesterdayBill())
print(getMonthBill())
print(predictedBill())