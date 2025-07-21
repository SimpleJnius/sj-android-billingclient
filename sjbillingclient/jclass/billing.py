from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaStaticField, JavaMethod, JavaMultipleMethod

__all__ = ("BillingClient", "BillingFlowParams", "BillingFlowParamsBuilder", "ProductType", "GetBillingConfigParams",
           "ProductDetailsParams", "BillingResponseCode", "SubscriptionUpdateParams", "SubscriptionUpdateParamsBuilder",
           "ReplacementMode")


class BillingClient(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingClient"
    newBuilder = JavaStaticMethod("(Landroid/content/Context;)Lcom/android/billingclient/api/BillingClient$Builder;")
    isFeatureSupported = JavaMethod("(Ljava/lang/String;)Lcom/android/billingclient/api/BillingResult;")
    launchBillingFlow = JavaMethod(
        "(Landroid/app/Activity;Lcom/android/billingclient/api/BillingFlowParams;)"
        "Lcom/android/billingclient/api/BillingResult;"
    )
    showAlternativeBillingOnlyInformationDialog = JavaMethod(
        "(Landroid/app/Activity;Lcom/android/billingclient/api/AlternativeBillingOnlyInformationDialogListener;)"
        "Lcom/android/billingclient/api/BillingResult;"
    )
    showExternalOfferInformationDialog = JavaMethod(
        "(Landroid/app/Activity;Lcom/android/billingclient/api/ExternalOfferInformationDialogListener;)"
        "Lcom/android/billingclient/api/BillingResult;"
    )
    showInAppMessages = JavaMethod(
        "(Landroid/app/Activity;Lcom/android/billingclient/api/InAppMessageParams;"
        "Lcom/android/billingclient/api/InAppMessageResponseListener;)"
        "Lcom/android/billingclient/api/BillingResult;"
    )
    acknowledgePurchase = JavaMethod(
        "(Lcom/android/billingclient/api/AcknowledgePurchaseParams;"
        "Lcom/android/billingclient/api/AcknowledgePurchaseResponseListener;)V"
    )
    consumeAsync = JavaMethod(
        "(Lcom/android/billingclient/api/ConsumeParams;"
        "Lcom/android/billingclient/api/ConsumeResponseListener;)V"
    )
    createAlternativeBillingOnlyReportingDetailsAsync = JavaMethod(
        "(Lcom/android/billingclient/api/AlternativeBillingOnlyReportingDetailsListener;)V"
    )
    createExternalOfferReportingDetailsAsync = JavaMethod(
        "(Lcom/android/billingclient/api/ExternalOfferReportingDetailsListener;)V"
    )
    endConnection = JavaMethod("()V")
    getBillingConfigAsync = JavaMethod(
        "(Lcom/android/billingclient/api/GetBillingConfigParams;"
        "Lcom/android/billingclient/api/BillingConfigResponseListener;)V"
    )
    isAlternativeBillingOnlyAvailableAsync = JavaMethod(
        "(Lcom/android/billingclient/api/AlternativeBillingOnlyAvailabilityListener;)V"
    )
    isExternalOfferAvailableAsync = JavaMethod(
        "(Lcom/android/billingclient/api/ExternalOfferAvailabilityListener;)V"
    )
    queryProductDetailsAsync = JavaMethod(
        "(Lcom/android/billingclient/api/QueryProductDetailsParams;"
        "Lcom/android/billingclient/api/ProductDetailsResponseListener;)V"
    )
    queryPurchasesAsync = JavaMethod(
        "(Lcom/android/billingclient/api/QueryPurchasesParams;"
        "Lcom/android/billingclient/api/PurchasesResponseListener;)V"
    )
    startConnection = JavaMethod("(Lcom/android/billingclient/api/BillingClientStateListener;)V")
    isReady = JavaMethod("()Z")


class BillingClientBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingClient$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/BillingClient;")
    enableAlternativeBillingOnly = JavaMethod("()Lcom/android/billingclient/api/BillingClient$Builder;")
    enableAutoServiceReconnection = JavaMethod("()Lcom/android/billingclient/api/BillingClient$Builder;")
    enableExternalOffer = JavaMethod("()Lcom/android/billingclient/api/BillingClient$Builder;")
    enablePendingPurchases = JavaMethod("(Lcom/android/billingclient/api/PendingPurchasesParams;)"
                                        "Lcom/android/billingclient/api/BillingClient$Builder;")
    enableUserChoiceBilling = JavaMethod("(Lcom/android/billingclient/api/UserChoiceBillingListener;)"
                                         "Lcom/android/billingclient/api/BillingClient$Builder;")
    setListener = JavaMethod("(Lcom/android/billingclient/api/PurchasesUpdatedListener;)"
                             "Lcom/android/billingclient/api/BillingClient$Builder;")


class ProductType(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingClient$ProductType"
    INAPP = JavaStaticField("Ljava/lang/String;")
    SUBS = JavaStaticField("Ljava/lang/String;")


class BillingResponseCode(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingClient$BillingResponseCode"
    BILLING_UNAVAILABLE = JavaStaticField("I")
    DEVELOPER_ERROR = JavaStaticField("I")
    ERROR = JavaStaticField("I")
    FEATURE_NOT_SUPPORTED = JavaStaticField("I")
    ITEM_ALREADY_OWNED = JavaStaticField("I")
    ITEM_NOT_OWNED = JavaStaticField("I")
    ITEM_UNAVAILABLE = JavaStaticField("I")
    NETWORK_ERROR = JavaStaticField("I")
    OK = JavaStaticField("I")
    SERVICE_DISCONNECTED = JavaStaticField("I")
    SERVICE_UNAVAILABLE = JavaStaticField("I")
    USER_CANCELED = JavaStaticField("I")


class BillingFlowParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/BillingFlowParams$Builder;")


class BillingFlowParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/BillingFlowParams;")
    setIsOfferPersonalized = JavaMethod("(Z)Lcom/android/billingclient/api/BillingFlowParams$Builder;")
    setObfuscatedAccountId = JavaMethod("(Ljava/lang/String;)Lcom/android/billingclient/api/BillingFlowParams$Builder;")
    setObfuscatedProfileId = JavaMethod("(Ljava/lang/String;)Lcom/android/billingclient/api/BillingFlowParams$Builder;")
    setProductDetailsParamsList = JavaMethod("(Ljava/util/List;)Lcom/android/billingclient/api"
                                             "/BillingFlowParams$Builder;")
    setSubscriptionUpdateParams = JavaMethod("(Lcom/android/billingclient/api"
                                             "/BillingFlowParams$SubscriptionUpdateParams;)Lcom/android/billingclient"
                                             "/api/BillingFlowParams$Builder;")


class GetBillingConfigParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/GetBillingConfigParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/GetBillingConfigParams$Builder;")


class ProductDetailsParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$ProductDetailsParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/BillingFlowParams$ProductDetailsParams$Builder;")


class SubscriptionUpdateParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$SubscriptionUpdateParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/BillingFlowParams"
                                  "$SubscriptionUpdateParams$Builder;")


class SubscriptionUpdateParamsBuilder(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$SubscriptionUpdateParams$Builder"
    build = JavaMethod("()Lcom/android/billingclient/api/BillingFlowParams$SubscriptionUpdateParams;")
    setOldPurchaseToken = JavaMethod("(Ljava/lang/String;)Lcom/android/billingclient/api"
                                     "/BillingFlowParams$SubscriptionUpdateParams$Builder;")
    setSubscriptionReplacementMode = JavaMethod("(I)Lcom/android/billingclient/api"
                                                "/BillingFlowParams$SubscriptionUpdateParams$Builder;")


class ReplacementMode(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$SubscriptionUpdateParams$ReplacementMode"
    CHARGE_FULL_PRICE = JavaStaticField("I")
    CHARGE_PRORATED_PRICE = JavaStaticField("I")
    DEFERRED = JavaStaticField("I")
    UNKNOWN_REPLACEMENT_MODE = JavaStaticField("I")
    WITHOUT_PRORATION = JavaStaticField("I")
    WITH_TIME_PRORATION = JavaStaticField("I")
