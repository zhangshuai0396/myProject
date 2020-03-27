from rest_framework import serializers

from address.models import Address
from category.models import Category
from good.models import Goods
from goodcar.models import Goodcar
from order.models import Order, Goodorder, Orderaddress
from user.models import User


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address', 'u_id')


# 参考 https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield 物理关联外键，增加数据库性能
class AddressListSerializers(serializers.ModelSerializer):
    # SerializerMethodField() 该方法内参数默认为 get_<field_name>
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ('id', 'address', 'u_id', "user_name")

    @staticmethod
    def get_user_name(obj):
        user = User.objects.get(id=obj.u_id)
        return user.name


class GoodListSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = ('id', 'name', 'u_id', "price", "num", "img", "category_id", "user_name", "category_name")

    @staticmethod
    def get_user_name(obj):
        user = User.objects.get(id=obj.u_id)
        return user.name

    @staticmethod
    def get_category_name(obj):
        category_obj = Category.objects.get(id=obj.category_id)
        return category_obj.name


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GoodCarListSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    good_name = serializers.SerializerMethodField()
    is_select_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    class Meta:
        model = Goodcar
        fields = ('id', 'u_id', 'good_id', 'buy_good_num', 'is_select', 'is_select_name', 'user_name', 'good_name', 'seller_name')

    @staticmethod
    def get_user_name(obj):
        user = User.objects.get(id=obj.u_id)
        return user.name

    @staticmethod
    def get_good_name(obj):
        goodobj = Goods.objects.get(id=obj.good_id)
        return goodobj.name

    @staticmethod
    def get_seller_name(obj):
        goodobj = Goods.objects.get(id=obj.good_id)
        seller = User.objects.get(id=goodobj.u_id)
        return seller.name

    @staticmethod
    def get_is_select_name(obj):
        if obj.is_select == 0:
            return "未选中"
        else:
            return "已选中"


class OrderSerializers(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    good_name = serializers.SerializerMethodField()
    order_address = serializers.SerializerMethodField()
    status_name = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'u_id', 'total_price', 'status', 'status_name', 'user_name', 'good_name', 'order_address')

    @staticmethod
    def get_user_name(obj):
        user = User.objects.get(id=obj.u_id)
        return user.name

    @staticmethod
    def get_good_name(obj):
        good_name = []
        goodsOrder = Goodorder.objects.filter(order_id=obj.id)
        for goodOrder in goodsOrder:
            goodobj = Goods.objects.get(id=goodOrder.good_id)
            good_name.append(goodobj.name)
            good_name.append(",")
        return good_name

    @staticmethod
    def get_order_address(obj):
        addressobj = Orderaddress.objects.get(order_id=obj.id)
        return addressobj.order_address

    @staticmethod
    def get_status_name(obj):
        if obj.status == 0:
            return "未付款"
        else:
            return "已付款"