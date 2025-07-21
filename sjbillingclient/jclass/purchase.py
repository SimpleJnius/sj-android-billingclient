from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaMethod, JavaStaticField

__all__ = ("PendingPurchasesParams", "PendingPurchasesParamsBuilder", "Purchase", "PurchaseState", "PendingPurchaseUpdate")


class PendingPurchasesParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/PendingPurchasesParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")


class PendingPurchasesParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/PendingPurchasesParams$Builder"

    build = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams;")
    enableOneTimeProducts = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")
    enablePrepaidPlans = JavaMethod("()Lcom/android/billingclient/api/PendingPurchasesParams$Builder;")


class Purchase(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/Purchase"

    getAccountIdentifiers = JavaMethod("()Lcom/android/billingclient/api/AccountIdentifiers;")
    getDeveloperPayload = JavaMethod("()Ljava/lang/String;")
    getOrderId = JavaMethod("()Ljava/lang/String;")
    getOriginalJson = JavaMethod("()Ljava/lang/String;")
    getPackageName = JavaMethod("()Ljava/lang/String;")
    getPendingPurchaseUpdate = JavaMethod("()Lcom/android/billingclient/api/Purchase$PendingPurchaseUpdate;")
    getProducts = JavaMethod("()Ljava/util/List;")
    getPurchaseState = JavaMethod("()I")
    getPurchaseTime = JavaMethod("()J")
    getPurchaseToken = JavaMethod("()Ljava/lang/String;")
    getQuantity = JavaMethod("()I")
    getSignature = JavaMethod("()Ljava/lang/String;")
    hashCode = JavaMethod("()I")
    isAcknowledged = JavaMethod("()Z")
    isAutoRenewing = JavaMethod("()Z")
    toString = JavaMethod("()Ljava/lang/String;")


class PurchaseState(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/Purchase$PurchaseState"

    # Purchase state constants
    PENDING = JavaStaticField("I")
    PURCHASED = JavaStaticField("I")
    UNSPECIFIED = JavaStaticField("I")


class PendingPurchaseUpdate(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/Purchase$PendingPurchaseUpdate"

    getProducts = JavaMethod("()Ljava/util/List;")
    getPurchaseToken = JavaMethod("()Ljava/lang/String;")

