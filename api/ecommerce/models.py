from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.CharField(max_length=255)
    src = models.URLField()
    name = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.name

class Product(models.Model):


   
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    permalink = models.URLField()
    date_created = models.DateTimeField()
    date_created_gmt = models.DateTimeField()
    date_modified = models.DateTimeField()
    date_modified_gmt = models.DateTimeField()
    TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('grouped', 'Grouped'),
        ('external', 'External'),
        ('variable', 'Variable'),
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='simple')


    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('private', 'Private'),
        ('publish', 'Publish'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    featured = models.BooleanField()
    
    CATALOG_VISIBILITY_CHOICES = (
        ('visible', 'Visible'),
        ('catalog', 'Catalog'),
        ('search', 'Search'),
        ('hidden', 'Hidden'),
    )
    catalog_visibility = models.CharField(max_length=100, choices=CATALOG_VISIBILITY_CHOICES)

    description = models.TextField()
    short_description = models.TextField()
    sku = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_on_sale_from = models.DateTimeField(null=True, blank=True)
    date_on_sale_from_gmt = models.DateTimeField(null=True, blank=True)
    date_on_sale_to = models.DateTimeField(null=True, blank=True)
    date_on_sale_to_gmt = models.DateTimeField(null=True, blank=True)
    on_sale = models.BooleanField()
    purchasable = models.BooleanField()
    total_sales = models.IntegerField()
    virtual = models.BooleanField()
    downloadable = models.BooleanField()
    download_limit = models.IntegerField()
    download_expiry = models.IntegerField()
    external_url = models.URLField(null=True, blank=True)
    button_text = models.CharField(max_length=100, null=True, blank=True)
    
    TAX_STATUS_CHOICES = (
        ('taxable', 'Taxable'),
        ('none', 'None'),
    )
    tax_status = models.CharField(max_length=100, choices=TAX_STATUS_CHOICES)
    
    tax_class = models.CharField(max_length=100, null=True, blank=True)
    manage_stock = models.BooleanField()
    stock_quantity = models.IntegerField(null=True, blank=True)
    
    BACKORDERS_CHOICES = (
        ('no', 'No'),
        ('notify', 'Notify'),
        ('yes', 'Yes'),
    )
    backorders = models.CharField(max_length=100, choices=BACKORDERS_CHOICES)
    
    backorders_allowed = models.BooleanField()
    backordered = models.BooleanField()
    low_stock_amount = models.IntegerField(null=True, blank=True)
    sold_individually = models.BooleanField()
    weight = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    width = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=100, null=True, blank=True)
    shipping_required = models.BooleanField()
    shipping_taxable = models.BooleanField()
    shipping_class = models.CharField(max_length=100, null=True, blank=True)
    shipping_class_id = models.IntegerField(null=True, blank=True)
    reviews_allowed = models.BooleanField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    rating_count = models.IntegerField()
    parent_id = models.IntegerField(null=True, blank=True)
    purchase_note = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')
    images = models.ManyToManyField(Image, related_name='products')
    
    menu_order = models.IntegerField(null=True, blank=True)
    price_html = models.TextField(null=True, blank=True)
    
    STOCK_STATUS_CHOICES = (
        ('instock', 'In stock'),
        ('outofstock', 'Out of stock'),
        ('onbackorder', 'On backorder'),
    )
    stock_status = models.CharField(max_length=100, choices=STOCK_STATUS_CHOICES)
    
    has_options = models.BooleanField()
    post_password = models.CharField(max_length=100, null=True, blank=True)
    
    # Meta Data
    wpcom_is_markdown = models.BooleanField()
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    

# class Customer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     phone = models.CharField(max_length=20, blank=True)

#     def __str__(self):
#         return self.user.username

# class Address(models.Model):
#     customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
#     address_type = models.CharField(max_length=10, choices=(('billing', 'Billing'), ('shipping', 'Shipping')))
#     address_line_1 = models.CharField(max_length=255)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=50)
#     postal_code = models.CharField(max_length=20)

#     def __str__(self):
#         return f"{self.address_line_1}, {self.city}"

# class Cart(models.Model):
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cart for {self.customer.user.username}"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity}"

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     paid = models.BooleanField(default=False)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#     billing_address = models.ForeignKey(Address, related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
#     shipping_address = models.ForeignKey(Address, related_name='+', on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f'Order {self.id}'

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return str(self.id)

# class Payment(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     successful = models.BooleanField(default=False)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=50)  # Could be extended to a separate model if needed
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment of {self.amount} for Order {self.order.id}"
