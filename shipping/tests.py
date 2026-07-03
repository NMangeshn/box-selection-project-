from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Box, Order, OrderItem, Product
from .services import recommend_box_for_order


class BoxRecommendationTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Coffee Mug',
            length=Decimal('10.00'),
            width=Decimal('8.00'),
            height=Decimal('8.00'),
            weight=Decimal('0.50'),
        )
        self.order = Order.objects.create(customer_name='Test Customer')
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
        )

    def test_recommends_lowest_cost_box_that_fits(self):
        Box.objects.create(
            name='Small Box',
            inner_length=Decimal('12.00'),
            inner_width=Decimal('10.00'),
            inner_height=Decimal('10.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('50.00'),
        )
        cheaper_box = Box.objects.create(
            name='Cheaper Box',
            inner_length=Decimal('15.00'),
            inner_width=Decimal('12.00'),
            inner_height=Decimal('12.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('40.00'),
        )

        recommendation = recommend_box_for_order(self.order)

        self.assertEqual(recommendation['box'], cheaper_box)
        self.assertEqual(recommendation['total_weight'], Decimal('1.00'))

    def test_ignores_box_when_weight_is_too_high(self):
        Box.objects.create(
            name='Weak Box',
            inner_length=Decimal('20.00'),
            inner_width=Decimal('20.00'),
            inner_height=Decimal('20.00'),
            max_weight=Decimal('0.50'),
            cost=Decimal('10.00'),
        )

        recommendation = recommend_box_for_order(self.order)

        self.assertIsNone(recommendation)

    def test_ignores_inactive_boxes(self):
        Box.objects.create(
            name='Inactive Box',
            inner_length=Decimal('20.00'),
            inner_width=Decimal('20.00'),
            inner_height=Decimal('20.00'),
            max_weight=Decimal('5.00'),
            cost=Decimal('10.00'),
            is_active=False,
        )

        recommendation = recommend_box_for_order(self.order)

        self.assertIsNone(recommendation)


class ApiTests(APITestCase):
    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'Notebook',
            'length': '20.00',
            'width': '15.00',
            'height': '2.00',
            'weight': '0.30',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_product_rejects_negative_weight(self):
        url = reverse('product-list')
        data = {
            'name': 'Bad Product',
            'length': '20.00',
            'width': '15.00',
            'height': '2.00',
            'weight': '-1.00',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_items(self):
        product = Product.objects.create(
            name='Book',
            length=Decimal('18.00'),
            width=Decimal('12.00'),
            height=Decimal('3.00'),
            weight=Decimal('0.70'),
        )
        url = reverse('order-list')
        data = {
            'customer_name': 'Test Customer',
            'items': [
                {
                    'product': product.id,
                    'quantity': 1,
                }
            ],
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_order_rejects_empty_items(self):
        url = reverse('order-list')
        data = {
            'customer_name': 'Test Customer',
            'items': [],
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_recommend_box_api(self):
        product = Product.objects.create(
            name='Phone Case',
            length=Decimal('16.00'),
            width=Decimal('8.00'),
            height=Decimal('2.00'),
            weight=Decimal('0.20'),
        )
        order = Order.objects.create(customer_name='API Customer')
        OrderItem.objects.create(order=order, product=product, quantity=1)
        box = Box.objects.create(
            name='Mailer Box',
            inner_length=Decimal('20.00'),
            inner_width=Decimal('12.00'),
            inner_height=Decimal('5.00'),
            max_weight=Decimal('2.00'),
            cost=Decimal('15.00'),
        )
        url = reverse('order-recommend-box', args=[order.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['box']['id'], box.id)

    def test_recommend_box_api_returns_404_when_no_box_fits(self):
        product = Product.objects.create(
            name='Large Product',
            length=Decimal('100.00'),
            width=Decimal('80.00'),
            height=Decimal('50.00'),
            weight=Decimal('20.00'),
        )
        order = Order.objects.create(customer_name='API Customer')
        OrderItem.objects.create(order=order, product=product, quantity=1)
        url = reverse('order-recommend-box', args=[order.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
