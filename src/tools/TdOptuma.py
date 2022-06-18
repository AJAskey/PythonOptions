import time

from src.Utils import build_list
from src.tdameritrade import td_api_key
from src.tdameritrade.Statistics import Statistics
from src.tdameritrade.TDA_Interface import call_tda
from src.tdameritrade.TdProcess import get_avg_iv2, process_putcall_data

totalPuts = 0
totalCalls = 0
valuePuts = 0.0
valueCalls = 0.0

if __name__ == '__main__':

    codes0 = ['JNK', 'SPLK', 'HLF']

    codes1 = build_list("D:/dev/MarketTools - dev/lists/BreadthETFs.csv")
    # codes1.sort()

    codes2 = build_list("D:/dev/MarketTools - dev/lists/shortlist.csv")
    # codes2.sort()

    codes3 = build_list("D:/dev/MarketTools - dev/lists/watchlist.csv")
    # codes3.sort()

    allc = codes0 + codes1 + codes2 + codes3
    # allc = ['SPY', 'QQQ']
    # allc = codes0 + codes1

    allc.sort()

    tmp_codes = set(allc)
    all_codes = list(tmp_codes)
    all_codes.sort()

    url = r"https://api.tdameritrade.com/v1/marketdata/chains"

    statlist = []

    totputiv = 0.0
    totcalliv = 0.0
    tot_codes = 0
    knt = 0
    for code in all_codes:

        if (len(code)) > 0:
            knt += 1
            if knt > 10:
                time.sleep(3.33)
                knt = 0

            p = dict(apikey=td_api_key, symbol=code)
            content = call_tda(url, p)
            try:
                if content['status'] == "SUCCESS":
                    print("Processing : ", code)

                    ul = float(content['underlyingPrice'])

                    stats = Statistics(code)

                    process_putcall_data(content['callExpDateMap'], stats, ul)
                    process_putcall_data(content['putExpDateMap'], stats, ul)

                    stats.calliv = get_avg_iv2(content['callExpDateMap'], ul, False)
                    stats.putiv = get_avg_iv2(content['putExpDateMap'], ul, False)
                    totcalliv += stats.calliv
                    totputiv += stats.putiv
                    tot_codes += 1
                    # try:
                    #     stats.realvol = get_realvol(code, 22)
                    # except:
                    stats.realvol = 0.0
                    stats.premium = 0.0
                    if stats.realvol > 0.0:
                        stats.premium = ((stats.calliv / stats.realvol) - 1.0) * 100.0
                        # print(code, stats.calliv, stats.realvol, stats.premium)

                    stats.calc()
                    statlist.append(stats)

                else:
                    print("Bad code : ", code)
                    time.sleep(0.33)
            except:
                print("Exception code : ", code)
                time.sleep(15.0)
                knt = 0

    with open("D:/Dev/MarketTools - dev/lists/OptionVol.csv", 'w') as fp:
        fp.write("CODE,Puts,Calls,PC,Put$,Call$,PC$,PutsOI,CallsOI,PCOI,Put$OI,Call$OI,PC$OI,")
        fp.write("PutIV,CallIV,hVol,Prem,Skew\n")
        for stats in statlist:
            fp.write("{},{:d},{:d},{:.2f},{:d},{:d},{:.2f},".format(
                stats.code,
                stats.totalPutsVol, stats.totalCallsVol, stats.putcall,
                int(stats.dollarPutsVol * 100.0), int(stats.dollarCallsVol * 100.0), stats.dollarputcall))
            fp.write("{:d},{:d},{:.2f},{:d},{:d},{:.2f},".format(
                stats.totalPutsOi, stats.totalCallsOi, stats.putcallio,
                int(stats.dollarPutsOi * 100.0), int(stats.dollarCallsOi * 100.0), stats.dollarputcalloi))
            fp.write(
                "{:.2f},{:.2f},{:.2f},{:.2f},{:d}\n".format(stats.putiv, stats.calliv, float(0.0), stats.premium,
                                                            round(stats.skew)))
