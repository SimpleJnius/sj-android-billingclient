from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaMethod

__all__ = ("QueryProductDetailsParams", "QueryProductDetailsParamsProduct")


class QueryProductDetailsParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/QueryProductDetailsParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;")


class QueryProductDetailsParamsProduct(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/QueryProductDetailsParams$Product"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;")


class QueryProductDetailsResult(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = f"com/android/billingclient/api/QueryProductDetailsResult"
    create = JavaStaticMethod("(Ljava/util/List;Ljava/util/List;)"
                              "Lcom/android/billingclient/api/QueryProductDetailsResult;")
    getProductDetailsList = JavaMethod("()Ljava/util/List;")
    getUnfetchedProductList = JavaMethod("()Ljava/util/List;")
