def extract_prices(resp, code):
    result = {}
    for period in resp.get(code).get("prices"):
        result[period.get("formatted_date")] = period.get("close")
    return result

def price_returns(price_ordered_dict: dict):
    sorted_price_list = [price_ordered_dict[period] for period in sorted(price_ordered_dict, reverse= True)]
    combined_price = zip(sorted_price_list, sorted_price_list[1:])
    returns = []
    for i in combined_price:
        returns.append((i[0] / i[1]) - 1)
    return returns