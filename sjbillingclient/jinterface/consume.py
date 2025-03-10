from jnius import PythonJavaClass, java_method

__all__ = ("ConsumeResponseListener", )


class ConsumeResponseListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/ConsumeResponseListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;Ljava/lang/String;)V")
    def onConsumeResponse(self, billing_result, purchase_token):
        self.callback(billing_result, purchase_token)
