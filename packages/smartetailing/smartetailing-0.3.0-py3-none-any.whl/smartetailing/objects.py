from datetime import datetime
from typing import List

from lxml.etree import Element

from smartetailing.__serializer import IXMLSerializer


class WebOrder(IXMLSerializer):
    def __init__(self):
        self.order = Order()
        self.web_comment = ""

    def from_xml(self, source_element: Element) -> 'WebOrder':
        self.order = Order().from_xml(source_element.find('Order'))
        self.web_comment = source_element.find('WebComment').text
        return self

    def to_xml(self) -> Element:
        c = Element('WebComment')
        c.text = self.web_comment
        e = Element('WebOrder')
        e.append(self.order.to_xml())
        return e

    @staticmethod
    def from_xml_collection(source_element: Element) -> List['WebOrder']:
        return [WebOrder().from_xml(order) for order in source_element.findall('WebOrder')]


class Order(IXMLSerializer):
    def __init__(self):
        self.currency = "USD"
        self.id = ""
        self.time = datetime.now()
        self.customer_id = 0
        self.customer_ip = ''

        self.ship_address = AddressInfo()
        self.bill_address = AddressInfo()
        self.affiliate_info = AffiliateInfo()

        self.shipping = Shipping()

        self.payment_info = PaymentInfo()
        self.status = ""
        self.comments = ""

        self.items: List[Item] = []

        self.order_total = OrderTotal()

    def from_xml(self, source_element: Element) -> 'Order':
        self.currency = source_element.find('Currency').text
        self.id = source_element.find('OrderId').text
        self.time = datetime.strptime(source_element.find('Time').text, "%a %b %d %H:%M:%S %Y")
        self.customer_id = int(source_element.find('CustomerId').text)
        self.customer_ip = source_element.find('CustomerIP').text

        self.ship_address = AddressInfo().from_xml(source_element.find('AddressShipTo'))
        self.bill_address = AddressInfo().from_xml(source_element.find('AddressBillTo'))

        self.affiliate_info = AffiliateInfo().from_xml(source_element.find('AffiliateInfo'))
        self.shipping = Shipping().from_xml(source_element.find('Shipping'))
        self.payment_info = PaymentInfo().from_xml(source_element.find('PaymentInfo'))
        self.status = source_element.find('Status').text
        self.comments = source_element.find('Comments').text

        self.items = [Item().from_xml(xml) for xml in source_element.find('Items').findall('Item')]
        self.order_total = OrderTotal().from_xml(source_element.find('OrderTotal'))
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class Shipping(IXMLSerializer):
    def __init__(self):
        self.method = ''
        self.classification = ''
        self.pickup_location = ''

    def from_xml(self, source_element: Element) -> 'Shipping':
        self.method = source_element.find('Method').text
        self.classification = source_element.find('Classification').text
        self.pickup_location = source_element.find('PickupLocation').text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class Item(IXMLSerializer):
    def __init__(self):
        self.id = 0
        self.code = 0
        self.mpn = "0-0"
        self.gtin1 = ""
        self.gtin2 = ""
        self.quantity = 1
        self.unit_price = 0.00
        self.weight = 1.00
        self.description = ""
        self.category = "Catalog > Accessories > Lighting > Headlights"
        self.url = ""
        self.taxable = "YES"
        self.model_year = ""  # TODO - What is this?
        self.option = Option()

    def from_xml(self, source_element: Element) -> 'Item':
        self.id = int(source_element.find('Id').text)
        self.code = int(source_element.find('Code').text or "0")
        self.mpn = source_element.find('Mpn').text or ""
        self.gtin1 = source_element.find('Gtin1').text or ""
        self.gtin2 = source_element.find('Gtin2').text or ""
        self.quantity = int(source_element.find('Quantity').text)
        self.unit_price = float(source_element.find('Unit-Price').text)
        self.weight = float(source_element.find('Weight').text or "0")
        self.description = source_element.find('Description').text or ""
        self.category = source_element.find('Category').text or ""
        self.url = source_element.find('Url').text
        self.taxable = source_element.find('Taxable').text or "YES"
        self.model_year = source_element.find('ModelYear').text or ""
        self.option = Option().from_xml(source_element.find('Option'))

        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class Option(IXMLSerializer):
    def __init__(self):
        self.name = ""
        self.type = ""
        self.value = ""

    def from_xml(self, source_element: Element) -> 'Option':
        if source_element is None:
            # Some items don't have option data, that's okay.
            return self
        self.name = source_element.get('name')
        self.type = source_element.get('type')
        self.value = source_element.text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class OrderTotal(IXMLSerializer):
    def __init__(self):
        self.subtotal = 0.00
        self.discount = 0.00
        self.shipping = 0.00
        self.tax = 0.00
        self.total = 0.00

    def from_xml(self, source_element: Element) -> 'OrderTotal':
        lines = source_element.findall("Line")
        self.subtotal = self.find_element_value(lines, "Subtotal")
        self.discount = self.find_element_value(lines, "Discount")
        self.shipping = self.find_element_value(lines, "Shipping")
        self.tax = self.find_element_value(lines, "Tax")
        self.total = self.find_element_value(lines, "Total")
        return self

    @staticmethod
    def find_element_value(lines: List[Element], line_type: str) -> float:
        return [float(line.text) for line in lines if line.get("type") == line_type][0]

    def to_xml(self) -> Element:
        raise NotImplementedError


class CardAuthInfo(IXMLSerializer):
    def __init__(self):
        self.amount = 0.00
        self.auth_response = ""
        self.avs_response = ""
        self.ccv_response = ""
        self.trans_id = ""

    def from_xml(self, source_element: Element) -> 'CardAuthInfo':
        self.amount = float(source_element.find("Amount").text)
        self.auth_response = source_element.find("Auth-Response").text
        self.avs_response = source_element.find("AVS-Response").text
        self.ccv_response = source_element.find("CCV-Response").text
        self.trans_id = source_element.find("TransId").text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class AffiliateInfo(IXMLSerializer):
    def __init__(self):
        self.id = 0
        self.affiliate = None
        self.commission = 0  # Money ?

    def from_xml(self, source_element: Element) -> 'AffiliateInfo':
        self.id = int(source_element.find("Id").text)
        self.affiliate = source_element.find("Affiliate").text
        self.commission = float(source_element.find("Commission").text)
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class AddressInfo(IXMLSerializer):
    def __init__(self):
        self.name = Name()
        self.address1 = ""
        self.address2 = ""
        self.city = ""
        self.state = ""
        self.country = ""
        self.zip = ""
        self.phone = ""
        self.email = ""

    def from_xml(self, source_element: Element) -> 'AddressInfo':
        self.name = Name().from_xml(source_element.find("Name"))
        self.address1 = source_element.find("Address1").text
        self.address2 = source_element.find("Address2").text
        self.city = source_element.find("City").text
        self.state = source_element.find("State").text
        self.country = source_element.find("Country").text
        self.zip = source_element.find("Zip").text
        self.phone = source_element.find("Phone").text
        self.email = source_element.find("Email").text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class Name(IXMLSerializer):
    def __init__(self):
        self.first = ""
        self.last = ""
        self.full = ""

    def from_xml(self, source_element: Element) -> 'Name':
        self.first = source_element.find("First").text
        self.last = source_element.find("Last").text
        self.full = source_element.find("Full").text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class PaymentInfo(IXMLSerializer):
    def __init__(self):
        self.payment_method = ''
        self.credit_card_info = CreditCardInfo()

    def from_xml(self, source_element: Element) -> 'PaymentInfo':
        self.payment_method = source_element.find('PaymentMethod').text
        self.credit_card_info = CreditCardInfo().from_xml(source_element.find('CreditCardInfo'))
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class CreditCardInfo(IXMLSerializer):
    def __init__(self):
        self.credit_card = CreditCard()
        self.card_auth_info = CardAuthInfo()

    def from_xml(self, source_element: Element) -> 'CreditCardInfo':
        self.credit_card = CreditCard().from_xml(source_element.find('CreditCard'))
        self.card_auth_info = CardAuthInfo().from_xml(source_element.find('CardAuthInfo'))
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError


class CreditCard(IXMLSerializer):
    def __init__(self):
        self.ccv = ""
        self.expiration = ""
        self.type = ""
        self.number = ''

    def from_xml(self, source_element: Element) -> 'CreditCard':
        self.ccv = source_element.find('CCV').text
        self.expiration = source_element.find("Expiration").text
        self.type = source_element.find('Type').text
        self.number = source_element.find('Number').text
        return self

    def to_xml(self) -> Element:
        raise NotImplementedError
