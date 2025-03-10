from jnius import PythonJavaClass, java_method

__all__ = ("BillingClientStateListener", )


class BillingClientStateListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/BillingClientStateListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;)V")
    def onBillingSetupFinished(self, billing_result):
        self.callback(billing_result)


class BillingConfigResponseListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/BillingConfigResponseListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;Lcom/android/billingclient/api/BillingConfig;)V")
    def onBillingConfigResponse(self, billing_result, billing_config):
        self.callback(billing_result, billing_config)
