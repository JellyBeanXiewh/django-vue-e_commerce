# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.encoding import smart_str


class Account(models.Model):
    username = models.CharField('用户名', primary_key=True, max_length=20)
    password = models.CharField('密码', max_length=16)

    class Meta:
        verbose_name = verbose_name_plural = '账户'
        db_table = 'Account'

    def __str__(self):
        return smart_str(self.username)


class Address(models.Model):
    addr_id = models.AutoField('地址ID', primary_key=True, auto_created=True)
    username = models.ForeignKey('UserInfo', models.CASCADE, db_column='username', verbose_name='账户')
    receiver = models.CharField('收件人', max_length=10)
    address = models.CharField('收货地址', max_length=50)
    phone_number = models.CharField('联系电话', max_length=15)

    class Meta:
        verbose_name = verbose_name_plural = '收货地址'
        db_table = 'Address'


class Cart(models.Model):
    username = models.ForeignKey('UserInfo', models.CASCADE, db_column='username', verbose_name='账户')
    item_id = models.ForeignKey('Item', models.CASCADE, db_column='item_id', verbose_name='商品ID')
    amount = models.IntegerField('数量')
    update_time = models.DateTimeField('更新时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '购物车'
        db_table = 'Cart'
        unique_together = (('item_id', 'username'),)


class Item(models.Model):
    item_id = models.AutoField('商品ID', primary_key=True, auto_created=True)
    item_name = models.CharField('商品名称', max_length=20)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    typeid = models.ForeignKey('ItemType', models.PROTECT, db_column='typeid', verbose_name='商品类型')
    description = models.TextField('商品描述', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '商品信息'
        db_table = 'Item'

    def __str__(self):
        return smart_str('{}: {}'.format(self.item_id, self.item_name))


class ItemType(models.Model):
    typeid = models.AutoField('商品类型ID', primary_key=True, auto_created=True)
    typename = models.CharField('类型名称', max_length=20)

    class Meta:
        verbose_name = verbose_name_plural = '商品类型'
        db_table = 'ItemType'

    def __str__(self):
        return smart_str('{}({})'.format(self.typename, self.typeid))


class Order(models.Model):
    order_id = models.AutoField('订单号', primary_key=True, auto_created=True)
    username = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='username', verbose_name='账户')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    payment_time = models.DateTimeField('支付时间', blank=True, null=True)
    ship_time = models.DateTimeField('发货时间', blank=True, null=True)
    finish_time = models.DateTimeField('完成时间', blank=True, null=True)
    summary_price = models.DecimalField('总金额', max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField('订单状态',
                                 choices=[
                                     (0, '待支付'),
                                     (1, '待发货'),
                                     (2, '已发货'),
                                     (3, '已完成'),
                                     (4, '已取消'),
                                     (5, '已退款'),
                                     (6, '已退货')
                                 ],
                                 default=0)
    delivery_company = models.CharField('物流公司', max_length=8, blank=True, null=True)
    delivery_id = models.CharField('快递单号', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '订单'
        db_table = 'Order'

    def __str__(self):
        return smart_str(self.order_id)


class OrderDetails(models.Model):
    order_id = models.ForeignKey('Order', models.CASCADE, db_column='order_id', verbose_name='订单号')
    item_id = models.CharField('商品ID', max_length=8)
    item_name = models.CharField('商品名称', max_length=20)
    price = models.DecimalField('购买单价', max_digits=10, decimal_places=2)
    amount = models.IntegerField('数量')
    product_review = models.OneToOneField('ProductReview', models.SET_NULL, db_column='pr_id', blank=True, null=True, verbose_name='评价ID')

    class Meta:
        verbose_name = verbose_name_plural = '订单详情'
        db_table = 'OrderDetails'
        unique_together = (('order_id', 'item_id'),)


class ProductReview(models.Model):
    review_id = models.AutoField('评价ID', primary_key=True, auto_created=True)
    order_id = models.OneToOneField(OrderDetails, models.CASCADE, db_column='order_id', verbose_name='订单ID')
    review_property = models.IntegerField('评价属性',
                                          default=3,
                                          choices=[
                                              (0, '差评'),
                                              (1, '中评'),
                                              (2, '好评')
                                          ],)
    content = models.TextField('评价内容', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '评价'
        db_table = 'ProductReview'


class StockInfo(models.Model):
    item = models.OneToOneField(Item, models.CASCADE, db_column='item_id', primary_key=True, verbose_name='商品ID')
    inventory = models.IntegerField('库存量')

    class Meta:
        verbose_name = verbose_name_plural = '库存信息'
        db_table = 'StockInfo'

    def __str__(self):
        return smart_str(self.item)


class UserInfo(models.Model):
    username = models.OneToOneField(Account, models.CASCADE, db_column='username', primary_key=True, verbose_name='账户')
    name = models.CharField('昵称', max_length=10, blank=True, null=True)
    sex = models.BooleanField('性别', choices=[(True, '男'), (False, '女')])
    phone = models.CharField('绑定手机', max_length=15, blank=True, null=True)
    register_date = models.DateField('注册日期', blank=True, null=True, auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '用户信息'
        db_table = 'UserInfo'

    def __str__(self):
        return smart_str('{}({})'.format(self.name, self.username))
