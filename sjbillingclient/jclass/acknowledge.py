from jnius import JavaClass, MetaJavaClass, JavaStaticMethod

__all__ = ("AcknowledgePurchaseParams",)


class AcknowledgePurchaseParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/AcknowledgePurchaseParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/AcknowledgePurchaseParams$Builder;")
