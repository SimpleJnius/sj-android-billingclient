from jnius import JavaClass, MetaJavaClass, JavaStaticMethod

__all__ = ("QueryProductDetailsParams", "QueryProductDetailsParamsProduct")


class QueryProductDetailsParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/QueryProductDetailsParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;")


class QueryProductDetailsParamsProduct(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/QueryProductDetailsParams$Product"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;")
