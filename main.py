#!/usr/bin/env python3
# A basic calculator which helps to actualize the needed Bitcoin collateral for a loan at Nexo.io .
# Don't forget! Not your keys, not your coins! Use loans responsibly!
from btc import data
from nexo import getInfo

btc_actual_string = data["bpi"]["USD"]["rate"]
btc_actual_usd = float(btc_actual_string.replace(",", ""))  # The actual price of Bitcoin in USD

loan_amount = float(input("Add the loan amount (USD): "))       # The already taken loan amount in USD
total_btc = float(input("Add the total amount of BTC in your Nexo wallet: "))
credit_wallet = float(input("Add the total amount of BTC in your Nexo credit line wallet: "))

nexo = input("Do you have Nexo coins (True/False)? ")


credit_usd = btc_actual_usd * credit_wallet     # The worth of collateral in USD
collateral_need = loan_amount / btc_actual_usd  # The loan amount in Bitcoin


def zero_apr_credit():

    zero_apr_collateral = round((collateral_need * 5), 8)   # The needed Bitcoin collateral for 0% APR loan
    print("The currently needed collateral for a 0% APR loan: ", zero_apr_collateral, " BTC")
    fine_tune = round((credit_wallet - zero_apr_collateral), 8)     # More or less BTC needed for 0% APR loan limit
    if fine_tune < 0:       # Basic test if the loan is either already margin called or at least one input is wrong.
        print("You're below the 0% APR limit. To upgrade back you need to add", fine_tune, " BTC to the Credit wallet. ")
    else:
        print("You're over or under collateralized with: ", fine_tune, " BTC")
        over_collateralized_percent = loan_amount / (credit_usd / 5)    # The over collateralized percentage
        margin_call = btc_actual_usd * over_collateralized_percent      # The lowest Bitcoin price for 0% APR loan
        print("You're still on 0% APR loan until Bitcoin price drops to: ", round(margin_call, 2), " USD")


def normal_credit():

    normal_collateral = round((collateral_need * 2), 8)     # The needed Bitcoin collateral for 50% APR loan
    print("The currently needed minimum collateral (50% LTV): ", round((collateral_need * 2), 8), " BTC")
    norm_fine_tune = round((credit_wallet - normal_collateral), 8)      # More or less BTC needed for 50% APR loan limit
    if norm_fine_tune < 0:      # Basic test if the loan is either already margin called or at least one input is wrong.
        print("You're loan either already margin called or some data is wrong! Start again!")
    else:
        print("You're over collateralized with: ", norm_fine_tune, " BTC")
        overcoll_norm_percent = loan_amount / (credit_usd / 2)      # The over collateralized percentage
        norm_margin_call = btc_actual_usd * overcoll_norm_percent   # The Bitcoin price for margin call of the loan
        print("You're above margin call until Bitcoin price drops to: ", round(norm_margin_call, 2), " USD")


if nexo.lower() == "true":      # If you have Nexo coins
    nexo_coins = float(input("Add the amount of Nexo you have in the Savings wallet: "))
    nexo_current = getInfo()        # Nexo live price feed from Coinmarketcap API (limited to daily 333)

    def nexo_loyalty():
        nexo_worth = ((nexo_coins * nexo_current) / (btc_actual_usd * total_btc)) * 100
        # The percentage amount the Nexo coins in the Savings wallet worth
        if nexo_worth <= 1:
            return "Base"
        if 1 < nexo_worth <= 5:
            return "Silver"
        if 5 < nexo_worth <= 10:
            return "Gold"
        if 10 < nexo_worth:
            return "Platinum"
    if nexo_loyalty() == "Platinum":
        no_interest = input("Do you want to calculate for a 0% APR loan (True/False)? ")
        # At Nexo Platinum package you're eligible to take 0% APR loans.
        if no_interest.lower() == "true":       # If you want 0% APR loans
            print("\n")
            zero_apr_credit()
        else:
            print("\n")
            normal_credit()
    else:
        print("\n")
        normal_credit()
        needed_nexo = round(((btc_actual_usd * total_btc) * 0.1), 8) - nexo_coins
        # The amount of Nexo coins needed to be able to get 0% APR loans
        print("\n")
        print("Right now to be able to get 0% APR loan you need to buy at least:", needed_nexo, "Nexo coins")

else:
    print("\n")
    normal_credit()


