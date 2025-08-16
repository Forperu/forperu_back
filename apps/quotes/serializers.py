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
      'company',
      'company_id',
      'branch_office',
      'branch_office_id',
      'customer',
      'customer_id',
      'quote_number',
      'quote_date',
      'expiration_date',
      'status',
      'total_amount',
      'discount',
      'tax',
      'grand_total',
      'notes',
      'created_by_user',
      'created_by',
      'updated_by_user',
      'updated_by',
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