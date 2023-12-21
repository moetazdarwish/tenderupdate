from django.db import models
from django.db.models.signals import post_save

# Create your models here.
from employee.models import EmployeeDetail
from inventory.models import RawProducts, Inventory


def Kitchen_Products_path(instance, filename):
    return 'kitchen_Products/{0}'.format(filename)

class Ingredients(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    receipt = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)
    min_level = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} '

class SubIngredients(models.Model):
    sub = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    ingre = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True, related_name='ingre')
    items = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sub.name} '

class KitCategory(models.Model):
    cate = models.CharField(max_length=100, null=True, blank=True)
    photo = models.FileField(blank=True, null=True, default='dePhoto.png', upload_to=Kitchen_Products_path,)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cate} '

class KitchenRecipe(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    cate = models.ForeignKey(KitCategory, on_delete=models.CASCADE, null=True, blank=True)
    s_descrip = models.TextField(null=True, blank=True)
    l_descrip = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)
    min_level = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    pause = models.BooleanField(null=True, blank=True, default=False)
    photo = models.FileField(blank=True, null=True, default='dePhoto.png', upload_to=Kitchen_Products_path)
    feature = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} '
    @property
    def get_rfeatuer(self):
        feat = self.recipefeatuers_set.all()
        return feat
class SubKitchenRecipe(models.Model):
    sub = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    raw = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sub.name} '

class RecipeFeatuers(models.Model):
    name = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    raw = models.ForeignKey(RawProducts, on_delete=models.CASCADE, null=True, blank=True)
    ingre = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name.name} '

class PricingSystem(models.Model):
    point = models.CharField(max_length=50, null=True, blank=True)

class RecipePrice(models.Model):
    profil = models.ForeignKey(PricingSystem, on_delete=models.CASCADE, null=True, blank=True)
    name = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    feature = models.BooleanField(default=False,null=True,blank=True)
    pause = models.BooleanField(default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    @property
    def get_featuers(self):
        feat = self.featuersprice_set.filter(pause=False)
        return feat

class FeatuersPrice(models.Model):
    name = models.ForeignKey(RecipePrice, on_delete=models.CASCADE, null=True, blank=True)
    extra = models.ForeignKey(RecipeFeatuers, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    pause = models.BooleanField(default=False,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)

class kitchenTask(models.Model):
    task = models.CharField(max_length=100, null=True, blank=True)
    emply = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    j_stat = models.BooleanField(null=True, blank=True, default=False)
    j_end = models.BooleanField(null=True, blank=True, default=False)
    for_sale = models.BooleanField(null=True, blank=True, default=True)
    for_cart = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=50,null=True,blank=True)

    @property
    def get_tasks(self):
        tasks = self.kitchenjobsassign_set.all()
        return tasks

def JournalkitchenTask(sender, instance, *args, **kwargs):
    if instance.task is None:
        instance.task = 'TK-{0}'.format(instance.id)
        instance.save()

post_save.connect(JournalkitchenTask, sender=kitchenTask)
class KitchenJobsAssign(models.Model):
    task = models.ForeignKey(kitchenTask, on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    ingrd = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True)
    feat = models.ForeignKey(RecipeFeatuers, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    descrp = models.TextField(null=True, blank=True)
    ord_id = models.IntegerField(null=True, blank=True, default=0)
    for_sale = models.BooleanField(null=True, blank=True, default=True)
    for_cart = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task.task} '
    class Meta:
        ordering = ['-date']

    @property
    def get_subtasks(self):
        sub_tasks = self.kitchensubtask_set.all()
        return sub_tasks




class KitchenInventory(models.Model):
    patch = models.CharField(max_length=100, null=True, blank=True)
    name = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    ingred = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True)
    cate = models.ForeignKey(KitCategory, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    q_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    q_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    fnsh = models.BooleanField(null=True, blank=True, default=False)
    p_return = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patch} '

class SideKitchenInventory(models.Model):
    patch = models.CharField(max_length=100, null=True, blank=True)
    name = models.ForeignKey(KitchenRecipe, on_delete=models.CASCADE, null=True, blank=True)
    ingred = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True, blank=True)
    cate = models.ForeignKey(KitCategory, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    q_in = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    q_out = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    fnsh = models.BooleanField(null=True, blank=True, default=False)
    p_return = models.BooleanField(null=True, blank=True, default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patch} '

class KitchenSubTask(models.Model):
    job = models.ForeignKey(KitchenJobsAssign, on_delete=models.CASCADE, null=True, blank=True)
    ingrd = models.ForeignKey(KitchenInventory, on_delete=models.CASCADE, null=True, blank=True)
    raw = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    feat = models.ForeignKey(RecipeFeatuers, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)