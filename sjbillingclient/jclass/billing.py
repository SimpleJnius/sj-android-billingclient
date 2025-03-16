from jnius import JavaClass, MetaJavaClass, JavaStaticMethod, JavaStaticField, JavaMethod, JavaMultipleMethod

__all__ = ("BillingClient", "BillingFlowParams", "ProductType", "GetBillingConfigParams",
           "ProductDetailsParams")


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
    queryPurchaseHistoryAsync = JavaMultipleMethod([
        ("(Lcom/android/billingclient/api/QueryPurchaseHistoryParams;"
         "Lcom/android/billingclient/api/PurchaseHistoryResponseListener;)V",
         False, False),
        ("(Ljava/lang/String;Lcom/android/billingclient/api/PurchaseHistoryResponseListener;)V,",
         False, False),
    ])
    queryPurchasesAsync = JavaMultipleMethod([
        ("(Lcom/android/billingclient/api/QueryPurchasesParams;"
         "Lcom/android/billingclient/api/PurchasesResponseListener;)V", False, False),
        ("(Ljava/lang/String;Lcom/android/billingclient/api/PurchasesResponseListener;)V",
         False, False),
    ])
    querySkuDetailsAsync = JavaMethod(
        "(Lcom/android/billingclient/api/SkuDetailsParams;"
        "Lcom/android/billingclient/api/SkuDetailsResponseListener;)V"
    )
    startConnection = JavaMethod("(Lcom/android/billingclient/api/BillingClientStateListener;)V")
    isReady = JavaMethod("()Z")


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


class GetBillingConfigParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/GetBillingConfigParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/GetBillingConfigParams$Builder;")


class ProductDetailsParams(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = "com/android/billingclient/api/BillingFlowParams$ProductDetailsParams"
    newBuilder = JavaStaticMethod("()Lcom/android/billingclient/api/BillingFlowParams$ProductDetailsParams$Builder;")
