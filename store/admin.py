from operator import inv
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.contrib import messages
from .models import Collection, Product


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'purchase_price', 'sale_price')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Wrong file type uploaded!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            parts_collection = Collection.objects.get(name="Truck Spare Parts")

            for line in csv_data:

                fields = line.split(",")
                # print(fields)
                name = fields[1],
                slug = ''.join(el for el in name[0] if el.isalnum()),
                stock_unit = str(fields[2]),
                purchase_price = float(fields[3]),
                sale_price = float(fields[4]),
                inventory = int(fields[5]),
                description = str(fields[0]),
                print("unit:", stock_unit[0])

                # print(stock_unit[0], purchase_price[0], sale_price, inventory[0])
                # break
                created = Product.objects.update_or_create(
                    collection=parts_collection,
                    name=name[0],
                    slug=slug,
                    stock_unit=stock_unit[0],
                    purchase_price=purchase_price[0],
                    sale_price=sale_price[0],
                    inventory=inventory[0],
                    description=description,
                )
                # created.save()
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {'form': form }
        return render(request, 'admin/csv_upload.html', data)

admin.site.register(Collection)
admin.site.register(Product, ProductAdmin)