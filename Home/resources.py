from import_export import resources, fields
from import_export.widgets import DateWidget, DecimalWidget, IntegerWidget
from .models import NseTickers

class NseTickersResource(resources.ModelResource):
    # Map Excel headers to model fields
    symbol = fields.Field(
        column_name='SYMBOL',
        attribute='symbol',
    )
    name_of_company = fields.Field(
        column_name='NAME OF COMPANY',
        attribute='name_of_company',
    )
    series = fields.Field(
        column_name='SERIES',
        attribute='series',
    )
    date_of_listing = fields.Field(
        column_name='DATE OF LISTING',
        attribute='date_of_listing',
        widget=DateWidget(format='%d-%b-%y')  # Adjust format as per your data
    )
    paid_up_value = fields.Field(
        column_name='PAID UP VALUE',
        attribute='paid_up_value',
        widget=DecimalWidget()
    )
    market_lot = fields.Field(
        column_name='MARKET LOT',
        attribute='market_lot',
        widget=IntegerWidget()
    )
    ISIN_number = fields.Field(
        column_name='ISIN NUMBER',
        attribute='ISIN_number',
    )
    face_value = fields.Field(
        column_name='FACE VALUE',
        attribute='face_value',
        widget=DecimalWidget()
    )

    class Meta:
        model = NseTickers
        import_id_fields = ('symbol', 'ISIN_number')  # Unique identifiers
        fields = (
            'SYMBOL',
            'NAME OF COMPANY',
            'SERIES',
            'DATE OF LISTING',
            'PAID UP VALUE',
            'MARKET LOT',
            'ISIN NUMBER',
            'FACE VALUE',
        )