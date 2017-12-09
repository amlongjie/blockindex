holder = {
    "BTC": 0.51,
    "BCH": 0.07,
    "IOT": 0.07,
    "DASH": 0.07,
    "XMR": 0.07,
    "NEO": 0.07,
    "EOS": 0.07,
    "QTUM": 0.07
}

symbol = ["BTC", "BCH", "IOT", "DASH", "XMR", "NEO", "EOS", "QTUM"]
cap = [274181069463, 25973752413, 14624737573, 5927601279, 4413242454, 2452803611, 2318020646, 934196763]
total = 0
for i in range(0, len(cap)):
    symbol_ = symbol[i]
    cap_ = cap[i]
    if symbol_ in holder:
        print symbol_ + ":" + str(cap_)
        total += cap_ * holder[symbol_]
print total
