"""
Siz Merchant API dan foydalanishiz uchun https://test.paycom.uz/ ning test laridan muvaffaqiyatlik o'tishiz kerak.
Har doim KEY almashganda yoki TEST qilish oldidan python manage.py create_paycom_user komandasini ishlating.
"""


from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from order.models import Order


from rest_framework.response import Response
from rest_framework.decorators import api_view

from decimal import Decimal




class CheckOrder(Paycom):
    """Order ni tekshiramiz."""
    def check_order(self, amount, account, **kwargs):
        order_id = int(account['order_id'])
        order = Order.objects.filter(id=order_id).first()
        if order is not None:
            if Decimal(amount) != Decimal(order.amount_for_payme):
                return self.INVALID_AMOUNT
            return self.ORDER_FOUND
        else:
            return self.ORDER_NOT_FOND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        order_id = int(transaction.order_key)
        order = Order.objects.filter(id=order_id).first()
        order.is_payed = True
        order.save()

        print(order)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        order_id = int(transaction.order_key)
        order = Order.objects.filter(id=order_id).first()
        order.is_payed = False
        order.save()


class PaymentView(MerchantAPIView):
    """Bu yerda biz validate qilamiz."""
    VALIDATE_CLASS = CheckOrder


@api_view(['POST'])
def checkout_view(request):
    """Tekshirib korish uchun."""
    data = request.data
    if 'id' in data and 'amount' in data:
        order_id = data['id']
        amount = Decimal(data['amount'])
        if 'return_url' in data:
            return_url = data['return_url']
        else:
            return_url = 'https://example.com/'
        paycom = Paycom()
        data['url'] = paycom.create_initialization(amount=amount, order_id=order_id, return_url=return_url)
    return Response(data)