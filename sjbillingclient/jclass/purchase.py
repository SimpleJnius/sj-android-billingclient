from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaMethod

__all__ = ("PendingPurchasesParams", "PendingPurchasesParamsBuilder")


class PendingPurchasesParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/PendingPurchasesParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")


class PendingPurchasesParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/PendingPurchasesParams$Builder"

    build = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams;")
    enableOneTimeProducts = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")
    enablePrepaidPlans = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")
