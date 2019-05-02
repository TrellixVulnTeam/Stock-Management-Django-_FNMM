from django.contrib import admin

import product
from product.models import Product, Team, TeamMember, Units

admin.site.register(Product)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Units)
