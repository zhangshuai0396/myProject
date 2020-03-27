
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from category.models import Category
from good.models import Goods
from permission.permission import CategoryPermission
from user.serializer import CategorySerializers


# 商品分类添加
class CategoryApiView(CreateAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    permission_classes = [CategoryPermission]


# 单个商品分类的查删改
class SingleCategoryApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    permission_classes = [CategoryPermission]

    #  删除分类时 要把相应类别的商品 删除
    def delete(self, request, *args, **kwargs):
        category_id = request.parser_context.get("kwargs").get("pk")
        Goods.objects.filter(category_id=category_id).delete()
        return self.destroy(request, *args, **kwargs)


# 商品分类分页
class PageListCategoryApiView(ListAPIView):
    serializer_class = CategorySerializers
    permission_classes = [CategoryPermission]

    # 此处不定义过滤器，简单
    def get_queryset(self):
        category = Category.objects.all()
        category_name = self.request.query_params.get("query")
        page_size = self.request.query_params.get("page_size")
        # 指定每页大小
        if page_size:
            self.paginator.page_size = page_size
        if category_name:
            category = category.filter(name=category_name)
        return category.order_by("id")
