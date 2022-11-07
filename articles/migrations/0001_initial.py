

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('addr', models.CharField(max_length=80)),
                ('position', models.CharField(choices=[('한식', '한식'), ('분식', '분식'), ('중식', '중식'), ('일식', '일식'), ('양식', '양식'), ('아시안', '아시안'), ('카페/디저트', '카페/디저트'), ('기타', None)], default='선택', max_length=10)),
                ('menu', models.TextField()),
                ('contact', models.CharField(blank=True, max_length=14)),
                ('homepage', models.CharField(blank=True, max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('x', models.CharField(max_length=80)),
                ('y', models.CharField(max_length=80)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='images/')),
                ('like_art_users', models.ManyToManyField(related_name='like_review', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grade', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('credit', models.TextField()),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='images/')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
