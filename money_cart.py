from yoomoney import Quickpay


def change_sum(x):
    quickpay = Quickpay(
                receiver="4100117394518969",
                quickpay_form="shop",
                targets="Покупка на месяц Авито бота",
                paymentType="SB",
                sum=x,
                )
    print(quickpay.base_url)
    print(quickpay.redirected_url)
    return quickpay.redirected_url

def get_sum(tg_id):
    quickpay = Quickpay(
                receiver="4100117394518969",
                quickpay_form="shop",
                targets="Покупка на месяц Авито бота",
                paymentType="SB",
                sum=5,
                label=tg_id
                )
    return quickpay.redirected_url