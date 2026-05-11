"""
Models cho app wishlist.
"""
from django.db import models

from apps.users.models import Account
from apps.products.models import Product


class Wishlist(models.Model):
    """
    Bang Wishlist - luu ds san pham yeu thich cua user.
    """
    wishlist_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='wishlist',
        db_column='account_id'
    )
    created_at = models.DateTimeField('Ngay tao', auto_now_add=True)

    class Meta:
        db_table = 'Wishlists'
        verbose_name = 'Danh sach yeu thich'
        verbose_name_plural = 'Danh sach yeu thich'

    def __str__(self):
        return f"Wishlist of {self.account.username}"


class WishlistItem(models.Model):
    """
    Item trong wishlist.
    """
    item_id = models.AutoField(primary_key=True)
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items',
        db_column='wishlist_id'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlist_items',
        db_column='product_id'
    )
    added_at = models.DateTimeField('Ngay them', auto_now_add=True)

    class Meta:
        db_table = 'WishlistItems'
        verbose_name = 'San pham yeu thich'
        verbose_name_plural = 'San pham yeu thich'
        unique_together = ['wishlist', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.product.name} in {self.wishlist}"


class RecentlyViewed(models.Model):
    """
    Bang theo doi san pham da xem gan day.
    Gioi han 20 san pham moi nguoi.
    """
    record_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='recently_viewed',
        db_column='account_id'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='recently_viewed_by',
        db_column='product_id'
    )
    viewed_at = models.DateTimeField('Thoi gian xem', auto_now_add=True)

    class Meta:
        db_table = 'RecentlyViewed'
        verbose_name = 'Da xem gan day'
        verbose_name_plural = 'Da xem gan day'
        unique_together = ['account', 'product']
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.account.username} viewed {self.product.name}"
