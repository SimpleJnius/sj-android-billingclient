from jnius import PythonJavaClass, java_method

__all__ = ("ProductDetailsResponseListener", )


class ProductDetailsResponseListener(PythonJavaClass):
    __javainterfaces__ = ["com/android/billingclient/api/ProductDetailsResponseListener"]
    __javacontext__ = "app"

    def __init__(self, callback):
        self.callback = callback

    @java_method("(Lcom/android/billingclient/api/BillingResult;"
                 "Lcom/android/billingclient/api/QueryProductDetailsResult;)V")
    def onProductDetailsResponse(self, billing_result, product_details_result):
        self.callback(billing_result, product_details_result)
