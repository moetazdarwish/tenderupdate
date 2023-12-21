from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Ingredients)
admin.site.register(SubIngredients)
admin.site.register(KitCategory)
admin.site.register(KitchenRecipe)
admin.site.register(SubKitchenRecipe)
admin.site.register(KitchenJobsAssign)
admin.site.register(KitchenInventory)
admin.site.register(kitchenTask)
admin.site.register(KitchenSubTask)
admin.site.register(SideKitchenInventory)
admin.site.register(RecipeFeatuers)
admin.site.register(RecipePrice)
admin.site.register(FeatuersPrice)
admin.site.register(PricingSystem)