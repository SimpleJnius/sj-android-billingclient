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
- Android application with Google Play Billing Library (version 7.1.1 recommended)

## Installation

```shell
# Using pip
pip install sjbillingclient

# In Buildozer (add to buildozer.spec)
requirements = sjbillingclient
android.gradle_dependencies = com.android.billingclient:billing:7.1.1
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

# Load the KV file
Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class HomeScreen(Screen):
    billing_client = None

    def purchase_or_subscribe(self):
        if self.billing_client:
            self.billing_client.end_connection()

        self.billing_client = BillingClient(on_purchases_updated=self.on_purchases_updated)
        self.billing_client.start_connection(
            on_billing_setup_finished=self.on_billing_setup_finished,
            on_billing_service_disconnected=lambda: print("disconnected")
        )

    def on_purchases_updated(self, billing_result, null, purchases):
        if billing_result.getResponseCode() == BillingResponseCode.OK and not null:
            for purchase in purchases:
                if self.ids.subscribe.active:
                    self.billing_client.acknowledge_purchase(
                        purchase_token=purchase.getPurchaseToken(),
                        on_acknowledge_purchase_response=self.on_acknowledge_purchase_response
                    )
                else:
                    self.billing_client.consume_async(purchase, self.on_consume_response)

    def on_acknowledge_purchase_response(self, billing_result):
        print(billing_result.getDebugMessage())
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.toast("Thank you for subscribing to buy us a cup of coffee! monthly")

    def on_consume_response(self, billing_result):
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.toast("Thank you for buying us a cup of coffee!")

    def on_product_details_response(self, billing_result, product_details_list):
        for product_details in product_details_list:
            self.billing_client.get_product_details(
                product_details,
                ProductType.SUBS if self.ids.subscribe.active else ProductType.INAPP)
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.billing_client.launch_billing_flow(product_details=product_details_list)

    def on_billing_setup_finished(self, billing_result):
        product_id = self.ids.btn.product_id
        if billing_result.getResponseCode() == BillingResponseCode.OK:
            self.billing_client.query_product_details_async(
                product_type=ProductType.SUBS if self.ids.subscribe.active else ProductType.INAPP,
                products_ids=[product_id],
                on_product_details_response=self.on_product_details_response,
            )

    def toast(self, message):
        # Implementation of toast message (platform specific)
        print(message)


class BillingApp(App):
    def build(self):
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
            on_release: root.purchase_or_subscribe()

        Widget:
            # Spacer
```

This example demonstrates:

1. A `HomeScreen` class that handles all billing operations
2. A `BillingApp` class that sets up the Kivy application and screen manager
3. A Kivy layout file that defines the UI with:
   - A checkbox to toggle between one-time purchase and subscription
   - A button to initiate the purchase flow

The `purchase_or_subscribe` method is called when the button is pressed, which initializes the billing client and starts the connection. The various callback methods handle different stages of the billing process, including acknowledging purchases and consuming one-time purchases.

## API Reference

### BillingClient

The main class for interacting with Google Play Billing.

#### Methods

- `__init__(on_purchases_updated)`: Initialize with a callback for purchase updates
- `start_connection(on_billing_setup_finished, on_billing_service_disconnected)`: Start billing connection
- `end_connection()`: End billing connection
- `query_product_details_async(product_type, products_ids, on_product_details_response)`: Query product details
- `get_product_details(product_details, product_type)`: Get formatted product details
- `launch_billing_flow(product_details, offer_token=None)`: Launch purchase flow
- `consume_async(purchase, on_consume_response)`: Consume a purchase
- `acknowledge_purchase(purchase_token, on_acknowledge_purchase_response)`: Acknowledge a purchase

### ProductType

Constants for product types:

- `ProductType.INAPP`: One-time purchases
- `ProductType.SUBS`: Subscriptions

### BillingResponseCode

Constants for billing response codes:

- `BillingResponseCode.OK`: Success
- `BillingResponseCode.USER_CANCELED`: User canceled
- `BillingResponseCode.SERVICE_UNAVAILABLE`: Service unavailable
- And many others

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Kenechukwu Akubue <kengoon19@gmail.com>
