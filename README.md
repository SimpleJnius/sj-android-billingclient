# SJBillingClient (Google Play Billing SDK for Python)

<!-- GitAds-Verify: 71CCWMQSMVD67LS4WF4N44EXISSL2UTQ -->
## GitAds Sponsored
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=simplejnius/sj-android-billingclient@github)](https://gitads.dev/v1/ad-track?source=simplejnius/sj-android-billingclient@github)

## Overview

SJBillingClient is a Python wrapper for the Google Play Billing Library that facilitates in-app purchases and subscriptions in Android applications. It provides a high-level, Pythonic interface to interact with Google Play's billing system, making it easier to implement and manage in-app purchases in Python-based Android apps (like those built with Kivy/Python-for-Android).

### Key Features

- **Simplified Billing Integration**: Easy-to-use Python API for Google Play Billing
- **Asynchronous Operations**: Non-blocking billing operations
- **Comprehensive Purchase Management**: Support for querying, purchasing, consuming, and acknowledging products
- **Product Types Support**: Handles both one-time purchases (INAPP) and subscriptions (SUBS)
- **Detailed Product Information**: Access to formatted prices, currency codes, and other product details

## Requirements

- Python 3.9+
- pyjnius 1.6.1+
- Android application with Google Play Billing Library (version 8.0.0 recommended)

## Installation

```shell
# Using pip
pip install sjbillingclient

# In Buildozer (add to buildozer.spec)
requirements = sjbillingclient
android.gradle_dependencies = com.android.billingclient:billing:8.0.0
```

## Quick Start

Here's a basic example of how to initialize the billing client and start a connection:

```python
from sjbillingclient.tools import BillingClient
from sjbillingclient.jclass.billing import ProductType, BillingResponseCode

# Define callback for purchase updates
def on_purchases_updated(billing_result, is_null, purchases):
    if billing_result.getResponseCode() == BillingResponseCode.OK:
        if not is_null:
            for purchase in purchases:
                print(f"Purchase: {purchase.getProducts().get(0)}")
                # Handle purchase here

# Create billing client
client = BillingClient(on_purchases_updated)

# Start connection
client.start_connection(
    on_billing_setup_finished=lambda result: print(f"Billing setup complete: {result.getResponseCode()}"),
    on_billing_service_disconnected=lambda: print("Billing service disconnected")
)
```

## Usage Examples

### Querying Product Details

```python
from sjbillingclient.tools import BillingClient
from sjbillingclient.jclass.billing import ProductType, BillingResponseCode

def on_product_details_response(billing_result, product_details_list):
    if billing_result.getResponseCode() == BillingResponseCode.OK:
        if product_details_list and not product_details_list.isEmpty():
            # Process product details
            for i in range(product_details_list.size()):
                product_detail = product_details_list.get(i)
                print(f"Product: {product_detail.getProductId()}")

                # Get formatted details
                details = client.get_product_details(product_detail, ProductType.INAPP)
                for detail in details:
                    print(f"Price: {detail['formatted_price']}")

# Query product details
client.query_product_details_async(
    product_type=ProductType.INAPP,
    products_ids=["product_id_1", "product_id_2"],
    on_product_details_response=on_product_details_response
)
```

### Launching a Purchase Flow

```python
from sjbillingclient.tools import BillingClient
from sjbillingclient.jclass.billing import ProductType, BillingResponseCode

def on_product_details_response(billing_result, product_details_list):
    if billing_result.getResponseCode() == BillingResponseCode.OK:
        if product_details_list and not product_details_list.isEmpty():
            # Launch billing flow with the first product
            product_detail = product_details_list.get(0)
            result = client.launch_billing_flow([product_detail])
            print(f"Launch billing flow result: {result.getResponseCode()}")

# Query product details and then launch purchase
client.query_product_details_async(
    product_type=ProductType.INAPP,
    products_ids=["product_id"],
    on_product_details_response=on_product_details_response
)
```

### Consuming a Purchase

```python
from sjbillingclient.tools import BillingClient
from sjbillingclient.jclass.billing import BillingResponseCode

def on_consume_response(billing_result, purchase_token):
    print(f"Consume result: {billing_result.getResponseCode()}")
    if billing_result.getResponseCode() == BillingResponseCode.OK:
        print(f"Successfully consumed: {purchase_token}")

# Consume a purchase
client.consume_async(purchase, on_consume_response)
```

### Acknowledging a Purchase

```python
from sjbillingclient.tools import BillingClient
from sjbillingclient.jclass.billing import BillingResponseCode

def on_acknowledge_purchase_response(billing_result):
    print(f"Acknowledge result: {billing_result.getResponseCode()}")
    if billing_result.getResponseCode() == BillingResponseCode.OK:
        print("Successfully acknowledged purchase")

# Acknowledge a purchase
client.acknowledge_purchase(purchase.getPurchaseToken(), on_acknowledge_purchase_response)
```

### Kivy Integration Example

Here's a complete example of integrating SJBillingClient with a Kivy application:

#### Python Code (main.py)

```python
from os.path import join, dirname, basename
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from sjbillingclient.jclass.billing import BillingResponseCode, ProductType
from sjbillingclient.tools import BillingClient

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class HomeScreen(Screen):
    """
    A screen that demonstrates Google Play Billing integration with Kivy.

    This screen provides functionality to make in-app purchases and subscriptions
    using the Google Play Billing Library through the SJBillingClient wrapper.

    Attributes:
        billing_client (BillingClient): The client used to interact with Google Play Billing.
    """
    billing_client = None

    def support(self):
        """
        Initializes the billing client and starts a connection to the Google Play Billing service.

        This method is called when the user wants to make a purchase or subscription.
        If a billing client already exists, it ends the connection before creating a new one.
        """
        if self.billing_client:
            self.billing_client.end_connection()

        self.billing_client = BillingClient(on_purchases_updated=self.on_purchases_updated)
        self.billing_client.start_connection(
            on_billing_setup_finished=self.on_billing_setup_finished,
            on_billing_service_disconnected=lambda: print("disconnected")
        )

    def on_purchases_updated(self, billing_result, null, purchases):
        """
        Callback method that is called when purchases are updated.

        This method handles the result of a purchase flow, either acknowledging
        a subscription or consuming a one-time purchase.

        Args:
            billing_result: The result of the billing operation.
            null: Boolean indicating if the purchases list is null.
            purchases: List of purchases that were updated.
        """
        if billing_result.getResponseCode() == BillingResponseCode.OK and not null:
            for purchase in purchases:
                if self.ids.subscribe.active:
                    self.billing_client.acknowledge_purchase(
                        purchase_token=purchase.getPurchaseToken(),
                        on_acknowledge_purchase_response=self.on_acknowledge_purchase_response
                    )
                else:
                    self.billing_client.consume_async(purchase, self.on_consume_response)
        print(billing_result.getResponseCode(), billing_result.getDebugMessage())

    def on_acknowledge_purchase_response(self, billing_result):
        """
        Callback method that is called when a purchase acknowledgement is complete.

        Args:
            billing_result: The result of the acknowledgement operation.
        """
        print(billing_result.getDebugMessage())
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.toast("Thank you for subscribing to buy us a cup of coffee! monthly")

    def on_consume_response(self, billing_result):
        """
        Callback method that is called when a purchase consumption is complete.

        Args:
            billing_result: The result of the consumption operation.
        """
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.toast("Thank you for buying us a cup of coffee!")

    def on_product_details_response(self, billing_result, product_details_result):
        """
        Callback method that is called when product details are retrieved.

        This method processes the product details and launches the billing flow.

        Args:
            billing_result: The result of the product details query.
            product_details_result: The result containing product details and unfetched products.
        """
        product_details_list = product_details_result.getProductDetailsList()
        unfetched_product_list = product_details_result.getUnfetchedProductList()

        if billing_result.getResponseCode() == BillingResponseCode.OK:
            for product_details in product_details_list:
                self.billing_client.get_product_details(
                    product_details,
                    ProductType.SUBS if self.ids.subscribe.active else ProductType.INAPP)
            for unfetched_product in unfetched_product_list:
                print(self.billing_client.get_unfetched_product(unfetched_product))
            self.billing_client.launch_billing_flow(product_details=product_details_list)

    def on_billing_setup_finished(self, billing_result):
        """
        Callback method that is called when the billing setup is complete.

        This method queries product details if the billing setup was successful.

        Args:
            billing_result: The result of the billing setup operation.
        """
        product_id = self.ids.btn.product_id
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.billing_client.query_product_details_async(
                product_type=ProductType.SUBS if self.ids.subscribe.active else ProductType.INAPP,
                products_ids=[product_id],
                on_product_details_response=self.on_product_details_response,
            )

    def toast(self, message):
        """
        Display a toast message.

        This is a simple implementation that just prints the message.
        In a real app, you would use platform-specific toast functionality.

        Args:
            message: The message to display.
        """
        # Implementation of toast message (platform specific)
        print(message)


class BillingApp(App):
    """
    Main application class for the SJBillingClient demo.

    This class sets up the application and creates the screen manager
    with the HomeScreen.
    """
    def build(self):
        """
        Build the application UI.

        Returns:
            ScreenManager: The root widget of the application.
        """
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    BillingApp().run()
```

#### Kivy Layout File (main.kv)

```kivy
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '20dp'
        spacing: '10dp'

        Label:
            text: 'SJBillingClient Demo'
            font_size: '24sp'
            size_hint_y: None
            height: '50dp'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: '50dp'

            Label:
                text: 'Subscribe'
                size_hint_x: 0.5

            CheckBox:
                id: subscribe
                size_hint_x: 0.5
                active: False

        Button:
            id: btn
            text: 'Buy Coffee'
            product_id: 'coffee_product_id'
            size_hint_y: None
            height: '60dp'
            on_release: root.support()

        Widget:
            # Spacer
```

This example demonstrates:

1. A `HomeScreen` class that extends `Screen` and handles all billing operations
2. A `BillingApp` class that sets up the Kivy application and screen manager
3. A Kivy layout file that defines the UI with:
   - A checkbox to toggle between one-time purchase and subscription
   - A button to initiate the purchase flow

The `support` method is called when the button is pressed, which initializes the billing client and starts the connection. The various callback methods handle different stages of the billing process, including:
- Handling purchase updates with `on_purchases_updated`
- Acknowledging subscription purchases with `acknowledge_purchase`
- Consuming one-time purchases with `consume_async`
- Processing product details with `on_product_details_response`, including handling unfetched products
- Querying product details with `query_product_details_async`

This example is designed to be copy-and-paste runnable, with no need for the user to add or remove anything to test it.

## API Reference

### BillingClient

The main class for interacting with Google Play Billing.

#### Constructor

- `__init__(on_purchases_updated, enable_one_time_products=True, enable_prepaid_plans=False)`: 
  - Initializes a new BillingClient instance
  - `on_purchases_updated`: Callback function that will be triggered when purchases are updated
  - `enable_one_time_products`: Boolean to enable one-time products (default: True)
  - `enable_prepaid_plans`: Boolean to enable prepaid plans (default: False)

#### Connection Methods

- `start_connection(on_billing_setup_finished, on_billing_service_disconnected)`: 
  - Starts a connection with the billing client
  - `on_billing_setup_finished`: Callback when billing setup is complete
  - `on_billing_service_disconnected`: Callback when billing service is disconnected

- `end_connection()`: 
  - Ends the connection with the billing client

#### Product Details Methods

- `query_product_details_async(product_type, products_ids, on_product_details_response)`: 
  - Queries product details asynchronously
  - `product_type`: Type of products (INAPP or SUBS)
  - `products_ids`: List of product IDs to query
  - `on_product_details_response`: Callback for product details response

- `get_product_details(product_details, product_type)`: 
  - Gets formatted product details
  - `product_details`: Product details object
  - `product_type`: Type of product (INAPP or SUBS)
  - Returns a list of dictionaries with product details

- `get_unfetched_product(unfetched_product)`: 
  - Gets details about an unfetched product
  - `unfetched_product`: Unfetched product object
  - Returns a dictionary with product ID, type, and status code

#### Purchase Methods

- `launch_billing_flow(product_details, offer_token=None)`: 
  - Launches the billing flow for purchase
  - `product_details`: List of product details objects
  - `offer_token`: Optional token for subscription offers

- `consume_async(purchase, on_consume_response)`: 
  - Consumes a purchase asynchronously
  - `purchase`: Purchase object to consume
  - `on_consume_response`: Callback for consume response

- `acknowledge_purchase(purchase_token, on_acknowledge_purchase_response)`: 
  - Acknowledges a purchase
  - `purchase_token`: Token of the purchase to acknowledge
  - `on_acknowledge_purchase_response`: Callback for acknowledge response

### PendingPurchasesParams

Parameters for handling pending purchases.

#### Methods

- `newBuilder()`: Creates a new builder for PendingPurchasesParams
- `build()`: Builds the PendingPurchasesParams object
- `enableOneTimeProducts()`: Enables one-time products
- `enablePrepaidPlans()`: Enables prepaid plans

### QueryProductDetailsParams

Parameters for querying product details.

#### Methods

- `newBuilder()`: Creates a new builder for QueryProductDetailsParams
- `setProductList(product_list)`: Sets the list of products to query
- `build()`: Builds the QueryProductDetailsParams object

### QueryProductDetailsResult

Result of a product details query.

#### Methods

- `getProductDetailsList()`: Gets the list of product details
- `getUnfetchedProductList()`: Gets the list of unfetched products

### ProductType

Constants for product types:

- `ProductType.INAPP`: One-time purchases
- `ProductType.SUBS`: Subscriptions

### BillingResponseCode

Constants for billing response codes:

- `BillingResponseCode.OK`: Success (0)
- `BillingResponseCode.USER_CANCELED`: User canceled (1)
- `BillingResponseCode.SERVICE_UNAVAILABLE`: Service unavailable (2)
- `BillingResponseCode.BILLING_UNAVAILABLE`: Billing unavailable (3)
- `BillingResponseCode.ITEM_UNAVAILABLE`: Item unavailable (4)
- `BillingResponseCode.DEVELOPER_ERROR`: Developer error (5)
- `BillingResponseCode.ERROR`: General error (6)
- `BillingResponseCode.ITEM_ALREADY_OWNED`: Item already owned (7)
- `BillingResponseCode.ITEM_NOT_OWNED`: Item not owned (8)
- `BillingResponseCode.SERVICE_DISCONNECTED`: Service disconnected (10)
- `BillingResponseCode.FEATURE_NOT_SUPPORTED`: Feature not supported (12)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Kenechukwu Akubue <kengoon19@gmail.com>
