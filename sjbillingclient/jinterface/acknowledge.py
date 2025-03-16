from jnius import PythonJavaClass, java_method

__all__ = ("AcknowledgePurchaseResponseListener", )


class AcknowledgePurchaseResponseListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/AcknowledgePurchaseResponseListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;)V")
    def onAcknowledgePurchaseResponse(self, billing_result):
        self.callback(billing_result)
