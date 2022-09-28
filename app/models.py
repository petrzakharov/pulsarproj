from django.core.validators import MinValueValidator
from django.db import models
from PIL import Image

# TODO flake8, isort


class Item(models.Model):
    TO_REENCODE = ['WEBP']
    FROM_REENCODE = ['JPG', 'JPEG', 'PNG']

    InStock = 'IS'  # В наличии
    SpecialDelivery = 'SD'  # Под заказ
    PendingAvailability = 'PA'  # Ожидается поступление
    OutOfStock = 'OS'  # Нет в наличии
    NotAvailable = 'NA'  # Не производится

    STATUSES = [
        (InStock, 'In stock'),
        (SpecialDelivery, 'Special delivery'),
        (PendingAvailability, 'Pending availability'),
        (OutOfStock, 'Out of stock'),
        (NotAvailable, 'Not available'),
    ]

    title = models.CharField(max_length=100, db_index=True)
    part_number = models.CharField(max_length=20, unique=True, db_index=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(1)]
    )
    status = models.CharField(max_length=2, choices=STATUSES, default=InStock)
    image = models.ImageField(upload_to='items/')

    class Meta:
        db_table = 'item'
        ordering = ['-title', ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_image_path(self, file_format):
        return self.image.path + '.' + file_format

    def make_reencode(self):
        image = Image.open(self.image.path)
        if image.format in self.FROM_REENCODE:
            for extension in self.TO_REENCODE:
                image.save(self.get_image_path(extension), quality=60)

    def save(self, *args, **kwargs):
        old = Item.objects.filter(pk=self.pk).first()
        if old and old.image == self.image:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            self.make_reencode()

    def __str__(self):
        return self.title
