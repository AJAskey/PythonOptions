"""
This is a doc string.
"""
from datetime import datetime

from src import OUTDIR
from src.Utils import is_success
from src.tdameritrade import td_api_key
from src.tdameritrade.Statistics import Statistics
from src.tdameritrade.TDA_Interface import call_tda
from src.tdameritrade.TdProcess import process_putcall_data, get_avg_iv2, get_realvol

totalPuts = 0
totalCalls = 0
valuePuts = 0.0
valueCalls = 0.0


def process_code(cod):
    p = dict(apikey=td_api_key, symbol=cod)
    content = call_tda(url, p)

    if is_success(content):
        print("Processing : ", cod)

        ul = float(content['underlyingPrice'])

        sts = Statistics(cod)

        process_putcall_data(content['callExpDateMap'], sts, ul)
        process_putcall_data(content['putExpDateMap'], sts, ul)

        sts.calliv = get_avg_iv2(content['callExpDateMap'], ul, False)
        sts.putiv = get_avg_iv2(content['putExpDateMap'], ul, False)
        sts.realvol = get_realvol(cod, 22)

        if sts.realvol > 0.0:
            sts.putpremium = ((sts.putiv / sts.realvol) - 1.0) * 100.0
            sts.callpremium = ((sts.calliv / sts.realvol) - 1.0) * 100.0

        totstats.code += " " + cod

        totstats.totalPutsVol += sts.totalPutsVol
        totstats.totalCallsVol += sts.totalCallsVol
        totstats.totalPutsOi += sts.totalPutsOi
        totstats.totalCallsOi += sts.totalCallsOi

        totstats.dollarPutsVol += sts.dollarPutsVol
        totstats.dollarCallsVol += sts.dollarCallsVol
        totstats.dollarPutsOi += sts.dollarPutsOi
        totstats.dollarCallsOi += sts.dollarCallsOi

        sts.calc()
        statlist.append(sts)
        return sts

    else:
        print("Bad code : ", cod)


if __name__ == '__main__':

    main_codes = ['XLB', 'XLC', 'XLE', 'XLF', 'KRE', 'XLI', 'XLK', 'IGV', 'XLP', 'XLU', 'XLV', 'XLY', 'XLRE',
                  'IYT', 'XHB', 'XRT', 'IBB', 'SMH', 'IWM', 'DIA', 'QQQ', 'SPY']

    misc_codes = ['TLT', 'SLV', 'GLD']

    test_codes = ['ARKK']

    url = r"https://api.tdameritrade.com/v1/marketdata/chains"

    statlist = []
    totstats = Statistics("Combined")

    for code in main_codes:
        da_sts = process_code(code)

    totstats.calc()
    print(totstats)

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S\n\n")
    print(date_time)

    with open(OUTDIR+"tdstats.txt", 'w') as fp:
        for stats in statlist:
            fp.write("{}"
                     ""
                     "\n".format(stats))
        fp.write("\n{}\n".format(totstats))
        fp.write("\n\n{}".format(date_time))

    strNow = now.strftime("%Y%m%d-%H%M%S")
    filename = OUTDIR+"tdstats-{d}.txt".format(d=strNow)
    with open(filename, 'w') as fp:
        for stats in statlist:
            fp.write("{}"
                     ""
                     "\n".format(stats))
        fp.write("\n{}\n".format(totstats))
