"""
A Python wrapper for the Google Play Billing Library that facilitates in-app purchases and subscriptions.

This module provides a high-level interface to interact with Google Play's billing system through
the BillingClient class. It handles various billing operations including:

- Establishing and managing billing service connections
- Querying product details for in-app purchases and subscriptions
- Processing purchase flows
- Handling consumption of purchased items
- Managing purchase acknowledgments

Key Features:
- Asynchronous billing operations
- Support for both one-time purchases (INAPP) and subscriptions (SUBS)
- Product details querying with price formatting
- Purchase flow management
- Consumption and acknowledgment handling

Example:
    ```python
    def on_purchases_updated(billing_result, purchases):
        # Handle purchase updates
        pass

    client = BillingClient(on_purchases_updated)
    client.start_connection(
        on_billing_setup_finished=lambda result: print("Billing setup complete"),
        on_billing_service_disconnected=lambda: print("Billing service disconnected")
    )
    ```

Dependencies:
    - jnius: For Java/Android interop
    - android.activity: For access to the Android activity context
"""

from typing import List, Dict, Optional
from jnius import autoclass, JavaException
from sjbillingclient.jclass.acknowledge import AcknowledgePurchaseParams
from sjbillingclient.jclass.billing import BillingClient as SJBillingClient, ProductType, ProductDetailsParams, \
    BillingFlowParams
from android.activity import _activity as activity  # noqa
from sjbillingclient.jclass.consume import ConsumeParams
from sjbillingclient.jclass.purchase import PendingPurchasesParams
from sjbillingclient.jclass.queryproduct import QueryProductDetailsParams, QueryProductDetailsParamsProduct
from sjbillingclient.jclass.querypurchases import QueryPurchasesParams
from sjbillingclient.jinterface.acknowledge import AcknowledgePurchaseResponseListener
from sjbillingclient.jinterface.billing import BillingClientStateListener
from sjbillingclient.jinterface.consume import ConsumeResponseListener
from sjbillingclient.jinterface.product import ProductDetailsResponseListener
from sjbillingclient.jinterface.purchases import PurchasesUpdatedListener, PurchasesResponseListener

ERROR_NO_BASE_PLAN = "You don't have a base plan"
ERROR_NO_BASE_PLAN_ID = "You don't have a base plan id"
ERROR_INVALID_PRODUCT_TYPE = "product_type not supported. Must be one of `ProductType.SUBS`, `ProductType.INAPP`"


class BillingClient:
    """
    Provides methods and functionality to manage billing operations, including starting and terminating
    billing connections, querying product details, launching billing flows, consuming purchases, and
    acknowledging purchases.

    This class acts as a wrapper around the Google Play Billing Library, simplifying the process of in-app
    purchases and subscriptions by integrating higher-level methods for essential billing features.

    :ivar __billing_client: The main billing client that interacts with the Google Play Billing Library.
    :type __billing_client: SJBillingClient
    :ivar __purchase_update_listener: Listener for purchase updates and processing purchase-related events.
    :type __purchase_update_listener: PurchasesUpdatedListener
    :ivar __billing_client_state_listener: Listener for tracking the state of the billing client connection.
    :type __billing_client_state_listener: BillingClientStateListener | None
    :ivar __product_details_response_listener: Listener that handles the response for product details queries.
    :type __product_details_response_listener: ProductDetailsResponseListener | None
    :ivar __consume_response_listener: Listener handling responses for consumption requests.
    :type __consume_response_listener: ConsumeResponseListener | None
    :ivar __acknowledge_purchase_response_listener: Listener handling responses for acknowledging purchases.
    :type __acknowledge_purchase_response_listener: AcknowledgePurchaseResponseListener | None
    :type __purchases_response_listener: PurchasesResponseListener | None handling responses for purchase queries.
    """

    def __init__(
            self,
            on_purchases_updated,
            enable_auto_service_reconnection: bool = True,
            enable_one_time_products: bool = True,
            enable_prepaid_plans: bool = False,
            enable_external_offer: bool = False,
    ) -> None:
        """
        Initializes an instance of the class with the given purchase update callback.

        :param on_purchases_updated: A callback function that will be triggered when purchases
            are updated. This function typically handles updates to purchases such as
            processing the results or actions related to the purchases.
        :type on_purchases_updated: callable
        """
        self.__billing_client_state_listener = None
        self.__product_details_response_listener = None
        self.__consume_response_listener = None
        self.__acknowledge_purchase_response_listener = None
        self.__purchases_response_listener = None

        self.__purchase_update_listener = PurchasesUpdatedListener(on_purchases_updated)
        pending_purchase_params = PendingPurchasesParams.newBuilder()
        if enable_one_time_products:
            pending_purchase_params.enableOneTimeProducts()
        if enable_prepaid_plans:
            pending_purchase_params.enablePrepaidPlans()

        billing_client = SJBillingClient.newBuilder(activity.context)
        if enable_external_offer:
            billing_client.enableExternalOffer()
        if enable_auto_service_reconnection:
            billing_client.enableAutoServiceReconnection()
        self.__billing_client = billing_client \
            .setListener(self.__purchase_update_listener) \
            .enablePendingPurchases(pending_purchase_params.build()) \
            .build()

    def start_connection(self, on_billing_setup_finished, on_billing_service_disconnected=lambda: None) -> None:
        """
        Starts a connection with the billing client and initializes the billing
        client state listener. This method sets up a listener to handle billing
        setup finished and billing service disconnection callbacks.

        :param on_billing_setup_finished: A callable that will be invoked when
            the billing setup has finished.
        :param on_billing_service_disconnected: A callable that will be invoked
            when the billing service gets disconnected.
        :return: None
        """
        self.__billing_client_state_listener = BillingClientStateListener(
            on_billing_setup_finished,
            on_billing_service_disconnected
        )
        self.__billing_client.startConnection(self.__billing_client_state_listener)

    def end_connection(self) -> None:
        """
        Ends the connection with the billing client.

        This method terminates the active connection with the billing client
        by calling its `endConnection` method. It ensures proper cleanup of
        resources related to the billing client.

        :return: None
        """
        self.__billing_client.endConnection()

    def query_purchase_async(self, product_type: str, on_query_purchases_response) -> None:
        """
        Queries purchases asynchronously for a given product type.

        This function utilizes the provided purchases response callback to handle the
        resulting response from the query.

        :param product_type: The type of the products to query purchases for (e.g., "inapp" or "subs").
        :param on_query_purchases_response: A callback function that is triggered when the
                                           purchases query is complete.
        :return: None
        """

        params = (QueryPurchasesParams.newBuilder()
                  .setProductType(product_type)
                  .build())

        self.__purchases_response_listener = PurchasesResponseListener(on_query_purchases_response)
        self.__billing_client.queryPurchasesAsync(params, self.__purchases_response_listener)

    def query_product_details_async(self, product_type: str, products_ids: List[str],
                                    on_product_details_response) -> None:
        """
        Queries product details asynchronously for a given list of product IDs and product type.

        This function utilizes the provided product details response callback to handle the
        resulting response from the query.

        :param product_type: The type of the products to be queried (e.g., "inapp" or "subs").
        :param products_ids: A list of product IDs to query details for.
        :param on_product_details_response: A callback function that is triggered when the
                                             product details query is complete.
        :return: None
        """
        JavaList = autoclass("java.util.List")
        product_list = [
            self._build_product_params(product_id, product_type)
            for product_id in products_ids
        ]

        params = (QueryProductDetailsParams.newBuilder()
                  .setProductList(JavaList.of(*product_list))
                  .build())

        self.__product_details_response_listener = ProductDetailsResponseListener(on_product_details_response)
        self.__billing_client.queryProductDetailsAsync(params, self.__product_details_response_listener)

    @staticmethod
    def _build_product_params(product_id: str, product_type: str):
        """
        Builds product parameters using the provided product ID and product type.

        This is a static helper method designed to construct and return an object
        representing the parameters for querying product details. It uses a builder
        pattern for constructing the product details object.

        :param product_id: The unique identifier of the product.
        :type product_id: str
        :param product_type: The type/category of the product (e.g., consumable, subscription).
        :type product_type: str
        :return: A constructed product details parameter object.
        :rtype: QueryProductDetailsParamsProduct
        """
        return (QueryProductDetailsParamsProduct.newBuilder()
                .setProductId(product_id)
                .setProductType(product_type)
                .build())

    @staticmethod
    def get_purchase(purchase) -> Dict:
        """
        Retrieves detailed information from a purchase object.

        This function extracts important details from a purchase object, such as
        product IDs, purchase token, purchase state, and other relevant information.
        The extracted details are then returned as a dictionary.

        :param purchase: The purchase object to extract information from.
        :type purchase: Purchase
        :return: A dictionary containing detailed information about the purchase.
        :rtype: Dict
        """
        account_identifiers = purchase.getAccountIdentifiers()
        pending_purchase_update = purchase.getPendingPurchaseUpdate()

        return {
            "products": list(purchase.getProducts()),
            "purchase_token": purchase.getPurchaseToken(),
            "purchase_state": purchase.getPurchaseState(),
            "purchase_time": purchase.getPurchaseTime(),
            "order_id": purchase.getOrderId(),
            "quantity": purchase.getQuantity(),
            "is_acknowledged": purchase.isAcknowledged(),
            "is_auto_renewing": purchase.isAutoRenewing(),
            "original_json": purchase.getOriginalJson(),
            "signature": purchase.getSignature(),
            "package_name": purchase.getPackageName(),
            "developer_payload": purchase.getDeveloperPayload(),
            "account_identifiers": {
                "obfuscated_account_id": account_identifiers.getObfuscatedAccountId(),
                "obfuscated_profile_id": account_identifiers.getObfuscatedProfileId(),
            },
            "pending_purchase_update": {
                "products": list(pending_purchase_update.getProducts() or []),
                "purchase_token": pending_purchase_update.getPurchaseToken(),
            } if pending_purchase_update else None
        }

    @staticmethod
    def get_unfetched_product(unfetched_product) -> Dict:
        """
        Retrieves detailed product information for an unfetched product.

        This function takes an object representing an unfetched product and extracts
        important details such as the product ID, product type, and status code.
        The extracted details are then returned as a dictionary.

        :param unfetched_product: The product object that has not yet been fetched.
            Must provide methods to retrieve product ID, type, and status code.
        :type unfetched_product: Any
        :return: A dictionary containing detailed information about the unfetched
            product, including its ID, type, and status code.
        :rtype: Dict
        """
        return {
            "product_id": unfetched_product.getProductId(),
            "product_type": unfetched_product.getProductType(),
            "status_code": unfetched_product.getStatusCode(),
        }

    def get_product_details(self, product_details, product_type: str) -> List[Dict]:
        """
        Retrieves the details of a product based on the provided product type. The function processes
        different types of products, such as subscriptions and in-app purchases, and returns the corresponding
        details.

        If the product type is not recognized, an exception is raised.

        :param product_details: The details of the product to process.
        :param product_type: The type of the product. It can either be 'SUBS' for subscriptions or 'INAPP' for in-app purchases.
        :return: A list of dictionaries containing the processed product details.
        :rtype: List[Dict]
        :raises Exception: If the specified product type is invalid.
        """
        if product_type == ProductType.SUBS:
            return self._get_subscription_details(product_details)
        elif product_type == ProductType.INAPP:
            return self._get_inapp_purchase_details(product_details)
        raise Exception(ERROR_INVALID_PRODUCT_TYPE)

    def _get_subscription_details(self, product_details) -> List[Dict]:
        """
        Retrieves subscription details from the provided product details by parsing its
        subscription offer details and related pricing phases. The extracted details
        include product ID, formatted price, price amount in micros, and the currency code.

        :param product_details: Contains information about the product including
            subscription offers and pricing.
        :type product_details: Any
        :return: List of dictionaries, each containing subscription details such as
            product ID, formatted price, price amount in micros, and currency code.
        :rtype: List[Dict]
        """
        details = []
        offer_details = product_details.getSubscriptionOfferDetails()
        for offer in offer_details:
            pricing_phase = offer.getPricingPhases().getPricingPhaseList().get(0)
            details.append(self._create_product_detail_dict(
                product_details.getProductId(),
                pricing_phase.getFormattedPrice(),
                pricing_phase.getPriceAmountMicros,
                pricing_phase.getPriceCurrencyCode()
            ))
        return details

    def _get_inapp_purchase_details(self, product_details) -> List[Dict]:
        """
        Retrieve and construct in-app purchase product details.

        This function takes product details from an in-app purchase API response and
        constructs a list of dictionaries containing formatted product details. Each
        dictionary includes details such as product ID, formatted price, raw price
        amount, and currency code. Only one-time purchase offer details are supported.

        :param product_details: Product details object containing information about
            an in-app purchase product.
        :type product_details: Any
        :return: A list of dictionaries representing constructed product details
            based on the provided product information.
        :rtype: List[Dict]
        """
        offer_details = product_details.getOneTimePurchaseOfferDetails()
        return [self._create_product_detail_dict(
            product_details.getProductId(),
            offer_details.getFormattedPrice(),
            offer_details.getPriceAmountMicros,
            offer_details.getPriceCurrencyCode()
        )]

    @staticmethod
    def _create_product_detail_dict(product_id: str, formatted_price: str,
                                    price_amount_micros, price_currency_code: str) -> Dict:
        """
        Creates a dictionary containing product details.

        This method generates and returns a dictionary that encapsulates product
        details such as the product identifier, formatted price, price in micros,
        and the price currency code.

        :param product_id: The unique identifier for the product.
        :type product_id: str
        :param formatted_price: The human-readable price of the product.
        :type formatted_price: str
        :param price_amount_micros: The price of the product in micro-units.
        :type price_amount_micros: int
        :param price_currency_code: The currency code associated with the product price.
        :type price_currency_code: str
        :return: A dictionary holding the product details.
        :rtype: Dict
        """
        return {
            "product_id": product_id,
            "formatted_price": formatted_price,
            "price_amount_micros": price_amount_micros,
            "price_currency_code": price_currency_code,
        }

    def launch_billing_flow(self, product_details: List, offer_token: Optional[str] = None):
        """
        Initiates the in-app billing flow for the specified product details and an optional
        offer token. The method constructs billing flow parameters using the provided product
        details and triggers the billing process.

        :param product_details: A list of product detail objects representing the items
                                available for purchase through the billing flow.
        :param offer_token: Optional string representing a unique token to identify
                            specific offers for the product being purchased.
        :return: An integer identifier returned by the billing client representing the
                 result of the billing flow launch attempt.
        """
        JavaList = autoclass("java.util.List")
        product_params_list = [
            self._create_product_params(product_detail, offer_token)
            for product_detail in product_details
        ]

        billing_flow_params = (BillingFlowParams.newBuilder()
                               .setProductDetailsParamsList(JavaList.of(*product_params_list))
                               .build())

        return self.__billing_client.launchBillingFlow(activity, billing_flow_params)

    def _create_product_params(self, product_detail, offer_token: Optional[str]):
        """
        Creates and builds product parameters for a given product detail and optional offer token.

        This method initializes the `ProductDetailsParams` through its builder,
        populates it with the provided product detail, and conditionally sets the
        offer token if the product type is a subscription (SUBS). Once all
        necessary values are set, it builds and returns the params.

        :param product_detail: The product details used for generating the params.
        :type product_detail: ProductDetails

        :param offer_token: Optional token specific to the offer for the subscription
            product. Will be resolved internally if not provided and the product type
            is a subscription.
        :type offer_token: Optional[str]

        :return: A fully constructed `ProductDetailsParams` object populated
            with the input product data and offer token, if applicable.
        :rtype: ProductDetailsParams
        """
        params = ProductDetailsParams.newBuilder()
        params.setProductDetails(product_detail)

        if product_detail.getProductType() == ProductType.SUBS:
            offer_token = self._resolve_offer_token(product_detail, offer_token)
            params.setOfferToken(offer_token)

        return params.build()

    @staticmethod
    def _resolve_offer_token(product_detail, offer_token: Optional[str]) -> str:
        """
        Resolves the offer token for a given product detail. If the provided offer token is
        not `None`, it returns the same. Otherwise, it determines the offer token using
        the subscription offer details from the product detail. Raises exceptions if the
        required information is missing.

        :param product_detail: The product detail object containing subscription offer
            details.
        :type product_detail: Any
        :param offer_token: A string value representing the offer token if provided,
            or None to attempt resolving it from the product detail.
        :type offer_token: Optional[str]
        :return: The resolved offer token as a string.
        :rtype: str
        :raises JavaException: When no base plan or base plan ID is found in the
            subscription offer details.
        """
        if offer_token:
            return offer_token

        offer_list = product_detail.getSubscriptionOfferDetails()
        if not offer_list or offer_list.isEmpty():
            raise JavaException(ERROR_NO_BASE_PLAN)

        base_plan_id = offer_list.get(0).getBasePlanId()
        if not base_plan_id:
            raise JavaException(ERROR_NO_BASE_PLAN_ID)

        return offer_list.get(0).getOfferToken()

    def consume_async(self, purchase, on_consume_response):
        """
        Consumes a given purchase asynchronously using the billing client. The method takes
        a purchase object and a callback function that is triggered upon the consumption's
        completion. This process involves creating appropriate consume parameters and invoking
        the consume operation on the billing client.

        :param purchase: The purchase object to consume.
        :type purchase: Purchase
        :param on_consume_response: The callback to execute upon completion of the consumption
            process. This should handle the result of the consumption.
        :type on_consume_response: Callable
        :return: None
        """
        consume_params = (
            ConsumeParams.newBuilder()
            .setPurchaseToken(purchase.getPurchaseToken())
            .build()
        )
        self.__consume_response_listener = ConsumeResponseListener(on_consume_response)
        self.__billing_client.consumeAsync(consume_params, self.__consume_response_listener)

    def acknowledge_purchase(self, purchase_token, on_acknowledge_purchase_response):
        """
        Acknowledges a purchase using the provided purchase token. This method communicates
        with the billing client to confirm the completion of a purchase, ensuring its validity
        and acknowledgment. A callback function is triggered once the acknowledgment process
        is complete.

        :param purchase_token: The token representing the purchase to be acknowledged.
        :type purchase_token: str
        :param on_acknowledge_purchase_response: A callback function to handle the
            response of the acknowledgment process. It is triggered upon completion.
        :type on_acknowledge_purchase_response: Callable[[AcknowledgePurchaseResponse], None]

        :return: None
        """
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
