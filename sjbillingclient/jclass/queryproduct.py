from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaMethod

__all__ = ("QueryProductDetailsParams", "QueryProductDetailsParamsProduct", "QueryProductDetailsParamsBuilder", "QueryProductDetailsParamsProductBuilder")


class QueryProductDetailsParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryProductDetailsParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;")


class QueryProductDetailsParamsProduct(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryProductDetailsParams$Product"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;")


class QueryProductDetailsParamsProductBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryProductDetailsParams$Product$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams$Product;")
    setProductId = JavaMethod("(Ljava/lang/String;)"
                              "Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;")
    setProductType = JavaMethod("(Ljava/lang/String;)"
                                "Lcom/android/billingclient/api/QueryProductDetailsParams$Product$Builder;")


class QueryProductDetailsParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryProductDetailsParams$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/QueryProductDetailsParams;")
    setProductList = JavaMethod("(Ljava/util/List;)Lcom/android/billingclient/api/QueryProductDetailsParams$Builder;")


class QueryProductDetailsResult(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/QueryProductDetailsResult"
    create = JavaStaticMethod("(Ljava/util/List;Ljava/util/List;)"
                              "Lcom/android/billingclient/api/QueryProductDetailsResult;")
    getProductDetailsList = JavaMethod("()Ljava/util/List;")
    getUnfetchedProductList = JavaMethod("()Ljava/util/List;")
