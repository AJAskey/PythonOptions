from TDAmeritrade import td_api_key
from TDAmeritrade.TDA_Interface import call_tda, get_tda_list
from Utilities import datetime_to_str


def printit(dd, ulie):
    dt = datetime_to_str(dd.expiration)
    cst = float(dd.strike * dd.oi)
    cst2 = float(dd.bid * dd.oi)
    str = "{} {} {} {} oi:{} vol:{} dte:{}\tiv:{:.1f}\tprem:{:.2f}%\task:{:.2f} cost:{:.1f} cost2:{:.1f}\n". \
        format(dd.code,
               dd.type,
               dt,
               dd.strike,
               dd.oi,
               dd.volume,
               dd.daysToExpiration,
               dd.volatility,
               # dd.bid,
               dd.ask,
               # dd.mark,
               # dd.last,
               # dd.intrinsicValue,
               dd.premium,
               cst, cst2)

    return str


def orgit(dd, ulie):
    pass


if __name__ == '__main__':

    url = r"https://api.tdameritrade.com/v1/marketdata/chains"
    p = dict(apikey=td_api_key, symbol='SPY', toDate='2022-06-17')
    content = call_tda(url, p)

    p = dict(apikey=td_api_key, symbol='SPY')
    ul, vol, daList = get_tda_list(url=url, params=p, min_dte=1, max_dte=25, min_oi=1,
                                   min_vol=0, min_price=0.10, max_iv=400.0, opt_type='CALL')

    print("{:.2f} {:.2f}".format(ul, vol))

    with open("out/maxpain.txt", 'w') as fp:
        for d in daList:
            s = printit(d, ul)
            fp.write(s)

    orgit(daList, ul)
