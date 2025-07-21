from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaMethod

__all__ = ("QueryPurchasesParams", "QueryPurchasesParamsBuilder")


class QueryPurchasesParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryPurchasesParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryPurchasesParams$Builder;")


class QueryPurchasesParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryPurchasesParams$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/QueryPurchasesParams;")
    setProductType = JavaMethod("(Ljava/lang/String;)Lcom/android/billingclient/api/QueryPurchasesParams$Builder;")
