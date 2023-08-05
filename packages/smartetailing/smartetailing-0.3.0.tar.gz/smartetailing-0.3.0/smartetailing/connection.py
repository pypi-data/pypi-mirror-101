import logging
from typing import List, Iterator

import requests
from lxml import etree
from lxml.etree import Element

from smartetailing.objects import WebOrder, Order


class SmartetailingConnection:
    def __init__(self, base_url: str, merchant_id: int, url_key: str):
        self.base_url = base_url
        self.merchant_id = merchant_id
        self.url_key = url_key

    def export_orders(self) -> Iterator[Order]:
        """
        Export the order XML and generate the order objects
        :return:
        """
        order_xml = self.__export_order_xml()
        for order in order_xml.findall('WebOrder'):
            yield WebOrder().from_xml(order).order

    def confirm_order_receipts(self, order_ids: Iterator[str]) -> None:
        for order_id in order_ids:
            self.__update_order(order_id)
            logging.info(f"Updated order {order_id}")

    def update_order_status(self, order_id: str, order_status: str) -> None:
        self.__update_status(order_id, order_status)
        logging.info(f"Updated order={order_id} to status={order_status}")

    def __export_order_xml(self) -> Element:
        r = self.__make_http_request(self.base_url, 'Orders', self.merchant_id, self.url_key)
        return etree.XML(r.content)

    def __update_order(self, order_id: str) -> requests.Response:
        return self.__make_http_request(self.base_url, 'UpdateOrder', self.merchant_id, self.url_key, order_id)

    def __update_status(self, order_id: str, order_status: str) -> requests.Response:
        return self.__make_http_request(self.base_url, 'UpdateStatus', self.merchant_id, self.url_key, order_id,
                                        order_status)

    @staticmethod
    def __make_http_request(base_url: str, method: str, merchant_id: int, url_key: str, order_id: str = '',
                            order_status: str = '') -> requests.Response:
        query_parameters: dict = {
            'method': method,
            'ver': '2.00',
            'merchant': f'{merchant_id}',
            'URLkey': url_key,
            'OrderNumber': order_id,
            'OrderStatus': order_status
        }
        r = requests.get(base_url, params=query_parameters)
        SmartetailingConnection.__handle_http_error(r)
        return r

    @staticmethod
    def __handle_http_error(response: requests.Response) -> None:
        if response.status_code >= 300:
            logging.debug(response)
            raise RuntimeError(f"Error {response}")
