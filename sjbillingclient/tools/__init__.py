from jnius import autoclass, JavaException
from sjbillingclient.jclass.acknowledge import AcknowledgePurchaseParams
from sjbillingclient.jclass.billing import BillingClient as SJBillingClient, ProductType, ProductDetailsParams, \
    BillingFlowParams
from android.activity import _activity as activity  # noqa
from sjbillingclient.jclass.consume import ConsumeParams
from sjbillingclient.jclass.queryproduct import QueryProductDetailsParams, QueryProductDetailsParamsProduct
from sjbillingclient.jinterface.acknowledge import AcknowledgePurchaseResponseListener
from sjbillingclient.jinterface.billing import BillingClientStateListener
from sjbillingclient.jinterface.consume import ConsumeResponseListener
from sjbillingclient.jinterface.product import ProductDetailsResponseListener
from sjbillingclient.jinterface.purchases import PurchasesUpdatedListener


class BillingClient:
    __billing_client = None
    __purchase_update_listener = None
    __billing_client_state_listener = None
    __product_details_response_listener = None
    __consume_response_listener = None
    __acknowledge_purchase_response_listener = None

    def __init__(self, on_purchases_updated):
        self.__purchase_update_listener = PurchasesUpdatedListener(on_purchases_updated)

        self.__billing_client = (
            SJBillingClient.newBuilder(activity.context)
            .setListener(self.__purchase_update_listener)
            .enablePendingPurchases()
            .build()
        )

    def start_connection(self, on_billing_setup_finished, on_billing_service_disconnected):
        self.__billing_client_state_listener = BillingClientStateListener(
            on_billing_setup_finished,
            on_billing_service_disconnected
        )
        self.__billing_client.startConnection(self.__billing_client_state_listener)

    def end_connection(self):
        self.__billing_client.endConnection()

    def query_product_details_async(self, product_type, products_ids: list, on_product_details_response):
        List = autoclass("java.util.List")
        queryProductDetailsParams = (
            QueryProductDetailsParams.newBuilder()
            .setProductList(
                List.of(*[
                    QueryProductDetailsParamsProduct.newBuilder()
                    .setProductId(product_id)
                    .setProductType(product_type)
                    .build()
                    for product_id in products_ids
                ])
            )
            .build()
        )

        self.__product_details_response_listener = ProductDetailsResponseListener(on_product_details_response)

        self.__billing_client.queryProductDetailsAsync(
            queryProductDetailsParams,
            self.__product_details_response_listener
        )

    @staticmethod
    def get_product_details(product_details, product_type):
        details = []
        if product_type == ProductType.SUBS:
            offer_details = product_details.getSubscriptionOfferDetails()
            for offer in offer_details:
                pricing_phase = offer.getPricingPhases().getPricingPhaseList().get(0)
                details.append({
                    "product_id": product_details.getProductId(),
                    "formatted_price": pricing_phase.getFormattedPrice(),
                    "price_amount_micros": pricing_phase.getPriceAmountMicros,
                    "price_currency_code": pricing_phase.getPriceCurrencyCode(),
                })
            return details
        elif product_type == ProductType.INAPP:
            offer_details = product_details.getOneTimePurchaseOfferDetails()
            details.append({
                "product_id": product_details.getProductId(),
                "formatted_price": offer_details.getFormattedPrice(),
                "price_amount_micros": offer_details.getPriceAmountMicros,
                "price_currency_code": offer_details.getPriceCurrencyCode(),
            })
            return details
        raise Exception("product_type not supported. Must be one of `ProductType.SUBS`, `ProductType.INAPP`")

    def launch_billing_flow(self, product_details: list, offer_token: str = None):

        product_details_param_list = []

        for product_detail in product_details:
            params = ProductDetailsParams.newBuilder()
            params.setProductDetails(product_detail)
            if product_detail.getProductType() == ProductType.SUBS:
                if not offer_token:
                    offer_list = product_detail.getSubscriptionOfferDetails()
                    if not offer_list or offer_list.isEmpty():
                        raise JavaException("You don't have a base plan")
                    base_plan_id = offer_list.get(0).getBasePlanId()
                    offer_token = offer_list.get(0).getOfferToken()
                    if not base_plan_id:
                        raise JavaException("You don't have a base plan id")
                    params.setOfferToken(offer_token)
                else:
                    params.setOfferToken(offer_token)
            product_details_param_list.append(params.build())
        List = autoclass("java.util.List")

        billing_flow_params = (
            BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(List.of(*product_details_param_list))
            .build()
        )

        billing_result = self.__billing_client.launchBillingFlow(activity, billing_flow_params)
        return billing_result

    def consume_async(self, purchase, on_consume_response):
        consume_params = (
            ConsumeParams.newBuilder()
            .setPurchaseToken(purchase.getPurchaseToken())
            .build()
        )
        self.__consume_response_listener = ConsumeResponseListener(on_consume_response)
        self.__billing_client.consumeAsync(consume_params, self.__consume_response_listener)

    def acknowledge_purchase(self, purchase_token, on_acknowledge_purchase_response):
        acknowledge_purchase_params = (
            AcknowledgePurchaseParams.newBuilder()
            .setPurchaseToken(purchase_token)
            .build()
        )

        self.__acknowledge_purchase_response_listener = AcknowledgePurchaseResponseListener(
            on_acknowledge_purchase_response
        )
        self.__billing_client.acknowledgePurchase(
            acknowledge_purchase_params,
            self.__acknowledge_purchase_response_listener
        )
