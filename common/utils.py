from common import models 


def add_debt_client(debt, client):
    client.debt += debt
    client.save()
    return client.debt

def subtract_debt_client(debt, client):
    client.debt -= debt
    client.save()
    return client.debt

