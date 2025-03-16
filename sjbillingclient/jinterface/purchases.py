__all__ = ("PurchasesUpdatedListener", )

from jnius import PythonJavaClass, java_method
from sjbillingclient import is_jnull


class PurchasesUpdatedListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/PurchasesUpdatedListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;Ljava/util/List;)V")
    def onPurchasesUpdated(self, billing_result, purchases):
        self.callback(billing_result, is_jnull(purchases), purchases)
