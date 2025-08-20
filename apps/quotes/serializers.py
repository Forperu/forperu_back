from rest_framework import serializers
from apps.quotes.models import Quote, QuoteDetail
from apps.companies.serializers import CompanySerializer
from apps.branch_offices.serializers import BranchOfficeSerializer
from apps.customers.serializers import CustomerSerializer
from apps.users.serializers import UserSerializer
from apps.products.serializers import ProductSerializer

class QuoteSerializer(serializers.ModelSerializer):
  company = serializers.SerializerMethodField()
  company_id = serializers.IntegerField(required=False, allow_null=True)
  branch_office = serializers.SerializerMethodField()
  branch_office_id = serializers.IntegerField(required=False, allow_null=True)
  customer = serializers.SerializerMethodField()
  customer_id = serializers.IntegerField(required=False, allow_null=True)
  created_by_user = serializers.SerializerMethodField()
  created_by = serializers.IntegerField(required=False, allow_null=True)
  updated_by_user = serializers.SerializerMethodField()
  updated_by = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = Quote
    fields = [
      'id',
      'reference',
      'warehouse',
      'warehouse_id',
      'customer',
      'customer_id',
      'currency',
      'currency_id',
      'user',
      'user_id',
      'issue_date',
      'exchange_rate',
      'expiration_date',
      'approved_by',
      'approved_by_id',
      'approved_at',
      'canceled_by',
      'canceled_by_id',
      'canceled_at',
      'discount',
      'subtotal',
      'total',
      'quote_status',
      'migrate_quote',
      'details',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

  def get_company(self, obj):
    if obj.company:
      CompanySerializer.Meta.model = obj.company.__class__
      return CompanySerializer(obj.company).data
    return None

  def get_branch_office(self, obj):
    if obj.branch_office:
      BranchOfficeSerializer.Meta.model = obj.branch_office.__class__
      return BranchOfficeSerializer(obj.branch_office).data
    return None

  def get_customer(self, obj):
    if obj.customer:
      CustomerSerializer.Meta.model = obj.customer.__class__
      return CustomerSerializer(obj.customer).data
    return None

  def get_created_by_user(self, obj):
    if obj.created_by_user:
      UserSerializer.Meta.model = obj.created_by_user.__class__
      return UserSerializer(obj.created_by_user).data
    return None

  def get_updated_by_user(self, obj):
    if obj.updated_by_user:
      UserSerializer.Meta.model = obj.updated_by_user.__class__
      return UserSerializer(obj.updated_by_user).data
    return None


class QuoteDetailSerializer(serializers.ModelSerializer):
  quote = serializers.SerializerMethodField()
  quote_id = serializers.IntegerField(required=False, allow_null=True)
  product = serializers.SerializerMethodField()
  product_id = serializers.IntegerField(required=False, allow_null=True)

  class Meta:
    model = QuoteDetail
    fields = [
      'id',
      'quote',
      'quote_id',
      'product',
      'product_id',
      'quantity',
      'unit_price',
      'discount',
      'tax',
      'subtotal',
      'total',
      'created_by',
      'updated_by',
      'created_at',
      'updated_at',
      'deleted_at'
    ]

  def get_quote(self, obj):
    if obj.quote:
      QuoteSerializer.Meta.model = obj.quote.__class__
      return QuoteSerializer(obj.quote).data
    return None

  def get_product(self, obj):
    if obj.product:
      ProductSerializer.Meta.model = obj.product.__class__
      return ProductSerializer(obj.product).data
    return None