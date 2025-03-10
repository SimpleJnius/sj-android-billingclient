from jnius import JavaClass, MetaJavaClass, JavaStaticMethod

__all__ = ("BillingClient", "BillingFlowParams")


class BillingClient(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/BillingClient"
    newBuilder = JavaStaticMethod("(Landroid/content/Context;)Lcom/android/billingclient/api/BillingClient$Builder;")


class BillingFlowParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/BillingFlowParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/BillingFlowParams$Builder;")


class GetBillingConfigParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/GetBillingConfigParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/GetBillingConfigParams$Builder;")
