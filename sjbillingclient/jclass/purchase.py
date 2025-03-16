from jnius import JavaClass, MetaJavaClass, JavaStaticMethod

__all__ = ("PendingPurchasesParams",)


class PendingPurchasesParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/PendingPurchasesParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")
