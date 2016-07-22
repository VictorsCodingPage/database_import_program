import datetime

class ProductDTO(object):
    def __init__(self, variant, **kwargs):
        self.id = None
        self.name = kwargs.get("name")
        self.brand = kwargs.get("brand")
        self.description = kwargs.get("description")
        self.product_code = kwargs.get("product_code")
        self.specification = kwargs.get("specification")
        self.category = kwargs.get("category")
        self.category_level_2 = kwargs.get("category_level_2")
        self.category_id = kwargs.get("category_id")
        self.shipping_info = kwargs.get("shipping_info")
        self.price_range = kwargs.get("price_range")
        self.post_id = kwargs.get("post_id")
        self.option_type = kwargs.get("option_type")
        self.option_type_id = kwargs.get("option_type_id")
        self.file_type = kwargs.get("file_type")
        self.file = kwargs.get("file")
        self.vendor = kwargs.get("vendor")
        self.vendor_url = kwargs.get("vendor_url")
        self.small_version_url = kwargs.get("small_version_url")
        self.normal_version_url = kwargs.get("normal_version_url")
        self.large_version_url = kwargs.get("large_version_url")
        self.cover_image = kwargs.get("cover_image")
        self.created_at = datetime.datetime.now()
        self.updated_at = kwargs.get("updated_at")
        self.product_file = kwargs.get("product_file")
        self.variant = variant

        def __getattribute__(self, item):
            return __dict__.get(self.item)

        def __repr__(self):
            return "{name} - {category}".format(name=self.name, category=self.category)

class VariantDTO(object):
    def __init__(self, **kwargs):
        self.id = None
        self.product_id = None
        self.description = kwargs.get("description")
        self.price = kwargs.get("price")
        self.currency = kwargs.get("currency")
        self.url = kwargs.get("url")
        self.sku = kwargs.get("sku")
      # self.store_id = kwargs.get("store_id")
      # self.quantity = kwargs.get("quantity")
        self.file_type = kwargs.get("file_type")
        self.file = kwargs.get("file")
        self.cover_image = kwargs.get("cover_image")
        self.specification = kwargs.get("specification")
        self.small_version_url = kwargs.get("small_version_url")
        self.normal_version_url = kwargs.get("normal_version_url")
        self.large_version_url = kwargs.get("large_version_url")
        self.created_at = datetime.datetime.now()
        self.updated_at = kwargs.get("updated_at")
        self.variant_file = kwargs.get("variant_file")