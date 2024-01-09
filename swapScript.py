from collections import OrderedDict
from terra_sdk.client.lcd import LCDClient
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.client.lcd.api.tx import CreateTxOptions
from terra_sdk.core.fee import Fee
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core.fee import Fee
from terra_sdk.core.coins import Coins

import time
import datetime

mk = MnemonicKey("once sphere again usage trip weird stage sadness direct inmate fork snow climb gospel decorate swap pluck nominee ensure marine walk grocery gorilla sketch")
account = mk.acc_address
wallet = LCDClient.wallet()

period = 0
od = OrderedDict()
terra = LCDClient(chain_id="pisco-1", url="https://phoenix-lcd.terra.dev")
total = 0
avg = 0
count = 1

#Block count variable
#count = 0

def lower_bound_chk():
    if od[latest_block] <= avg * 0.99:
        return True
    return False

#Query luna to axl-USDC
def query_price():
    #query message that offers 1 luna
    query = {
        "simulation": {
            "offer_asset": {
                "info": {
                    "native_token": {
                        "denom": "uluna"
                    }
                },
                "amount": "1000000"
            }
        }
    }

    #Address for luna to axlUSDC
    contract_address = "terra1fd68ah02gr2y8ze7tm9te7m70zlmc7vjyyhs6xlhsdmqqcjud4dql4wpxr"
    #Result of querying luna to axlUSDC
    result = terra.wasm.contract_query(contract_address, query)
    return int(result["return_amount"]) - int(result["commission_amount"])

def query_price1():
    #query message
    query = {
            "simulate_swap_operations": {
                "offer_amount": str(query_price()),
                "operations": [
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "token": {
                        "contract_addr": "terra1qx284aak0wl7vrvlsc6cwcsn6xwajragkh6cjqj87m9p34hx5l2s22p3cp"
                        }
                    },
                    "offer_asset_info": {
                        "native_token": {
                        "denom": "ibc/B3504E092456BA618CC28AC671A71FB08C6CA0FD0BE7C8A5B5A3E2DD933CC9E4"
                        }
                    }
                    }
                },
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "native_token": {
                        "denom": "uluna"
                        }
                    },
                    "offer_asset_info": {
                        "token": {
                        "contract_addr": "terra1qx284aak0wl7vrvlsc6cwcsn6xwajragkh6cjqj87m9p34hx5l2s22p3cp"
                        }
                    }
                    }
                }
                ]
            }
        }

    #Address for axlUSDC to luna
    contract_address = "terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a"
    #Result of querying axlUSDC to luna
    result = terra.wasm.contract_query(contract_address, query)
    return int(result["amount"])

#swap from luna to axlUSDC
def swap():
    #Contract address for luna-axlUSDC
    contract_addr = "terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a"
    #Swap Operations for luna-axlUSDC
    swap = {
            "execute_swap_operations": {
                "minimum_receive": "79824",
                "operations": [
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "token": {
                        "contract_addr": "terra1d4j9lsl453mkvtlg4ctw8y52rdkhafsaefug0hq0z06phczuvvvs7uq0vg"
                        }
                    },
                    "offer_asset_info": {
                        "native_token": {
                        "denom": "uluna"
                        }
                    }
                    }
                },
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "token": {
                        "contract_addr": "terra1ry9f6alqyf9dpj04u9ymq5u4whjndu485agh6gusn89dmqse3ggsnzducj"
                        }
                    },
                    "offer_asset_info": {
                        "token": {
                        "contract_addr": "terra1d4j9lsl453mkvtlg4ctw8y52rdkhafsaefug0hq0z06phczuvvvs7uq0vg"
                        }
                    }
                    }
                },
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "native_token": {
                        "denom": "ibc/B3504E092456BA618CC28AC671A71FB08C6CA0FD0BE7C8A5B5A3E2DD933CC9E4"
                        }
                    },
                    "offer_asset_info": {
                        "token": {
                        "contract_addr": "terra1ry9f6alqyf9dpj04u9ymq5u4whjndu485agh6gusn89dmqse3ggsnzducj"
                        }
                    }
                    }
                }
                ]
            }
        }

    #Execute msg input fields
    execute = MsgExecuteContract(
        mk.acc_address,
        contract_addr,
        swap,
        {"uluna": 1000000},
    )

    #Tx amount
    execute_tx = wallet.wallets.create_and_sign_tx(
        CreateTxOptions(msgs=[execute], fee=Fee(1000000, Coins(uluna=1000000)))
    )

    #Execute/Result
    execute_tx_result = terra.tx.broadcast(execute_tx)
    print(execute_tx_result)

#swap from axlUSDC to luna
def swap1():
    #Contract address for axlUSDC-luna
    contract_addr = "terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a"
    #Swap Operations for axlUSDC-luna
    swap = {
            "execute_swap_operations": {
                "minimum_receive": "39282",
                "operations": [
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "token": {
                        "contract_addr": "terra1qx284aak0wl7vrvlsc6cwcsn6xwajragkh6cjqj87m9p34hx5l2s22p3cp"
                        }
                    },
                    "offer_asset_info": {
                        "native_token": {
                        "denom": "ibc/B3504E092456BA618CC28AC671A71FB08C6CA0FD0BE7C8A5B5A3E2DD933CC9E4"
                        }
                    }
                    }
                },
                {
                    "astro_swap": {
                    "ask_asset_info": {
                        "native_token": {
                        "denom": "uluna"
                        }
                    },
                    "offer_asset_info": {
                        "token": {
                        "contract_addr": "terra1qx284aak0wl7vrvlsc6cwcsn6xwajragkh6cjqj87m9p34hx5l2s22p3cp"
                        }
                    }
                    }
                }
                ]
            }
        }

    '''
        {
            "send": {
                "contract": "terra1j8hayvehh3yy02c2vtw5fdhz9f4drhtee8p5n5rguvg3nyd6m83qd2y90a",
                "amount": "10000000",
                "msg": "ewogICJleGVjdXRlX3N3YXBfb3BlcmF0aW9ucyI6IHsKICAgICJvcGVyYXRpb25zIjogWwogICAgIHsKICAgICAgICAiYXN0cm9fc3dhcCI6IHsKICAgICAgICAgICJvZmZlcl9hc3NldF9pbmZvIjogewogICAgICAgICAgICAidG9rZW4iOiB7CiAgICAgICAgICAgICAgICAiY29udHJhY3RfYWRkciI6ICJ0ZXJyYTE2N2RzcWtoMmFsdXJ4OTk3d215Y3c5eWRreXU1NGd5c3dlM3lnbXJzNGx3dW1lM3Ztd2tzOHJ1cW52IgogICAgICAgICAgICAgIH0KICAgICAgICAgIH0sCiAgICAgICAgICAiYXNrX2Fzc2V0X2luZm8iOiB7CiAgICAgICAgICAgICJuYXRpdmVfdG9rZW4iOiB7CiAgICAgICAgICAgICAgICAiZGVub20iOiAidWx1bmEiCiAgICAgICAgICAgICAgfQogICAgICAgICAgfQogICAgICAgIH0KICAgICAgfQogICAgXQogIH0KfQ=="
            }
        }
    '''

    #Execute msg input fields
    execute = MsgExecuteContract(
        mk.acc_address,
        contract_addr,
        swap,
        {"uluna": 1000000},
    )

    #Tx amount
    execute_tx = wallet.wallets.create_and_sign_tx(
        CreateTxOptions(msgs=[execute], fee=Fee(1000000, Coins(uluna=1000000)))
    )

    #Execute/Result
    execute_tx_result = terra.tx.broadcast(execute_tx)
    print(execute_tx_result)


while True:
    if period == 0:
        #Always returns latest block
        latest_block = int(terra.tendermint.block_info()['block']['header']['height'])
        #If latest block exists in set reset count otherwise check for swap opportunity
        if latest_block in od:
            period = 3.25
        else:
            if len(od) > 499:
                #Re-calculate total so first block is no longer reflected in average price
                total -= od[latest_block-500]
                #Delete first block
                del od[latest_block-500]

            #Create new block and re-calculate average
            od[latest_block] = query_price()
            total += od[latest_block]
            newAvg = total/500

            #If new block deviates from average price perform appropriate swap
            if (od[latest_block] <= avg * 0.99 or od[latest_block] >= avg * 1.01) and len(od) == 500:
                if lower_bound_chk():
                    swap()
                else:
                    swap1()
            
            #Re-calculate new average
            avg = newAvg


            #Provides block count
            if len(od) < 500:
                count += 1
                print("Block Count: " + str(count))
                print(od[latest_block])
    else: 
        #Sets timer to current period
        timer = datetime.timedelta(seconds = period)
        #Waits .25 seconds and subtracts from time
        time.sleep(0.25)
        period -= 0.25

