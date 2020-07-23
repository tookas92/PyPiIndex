from django.db import models

# Create your models here.


class Package(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=128, null=True, blank=True)
    author_email = models.EmailField()
    bugtrack_url = models.CharField(max_length=512, null=True, blank=True)
    classifiers = models.CharField(max_length=512, null=True, blank=True)
    description = models.TextField(blank=True)
    description_content_type = models.CharField(max_length=128, blank=True)
    docs_url = models.CharField(max_length=512, blank=True, null=True)
    download_url = models.CharField(max_length=512, blank=True)
    downloads = models.CharField(max_length=512)
    home_page = models.CharField(max_length=512, null=True, blank=True)
    keywords = models.CharField(max_length=1024, blank=True)
    license = models.CharField(max_length=256, blank=True)
    maintainer = models.CharField(max_length=256, blank=True)
    maintainer_email = models.EmailField(blank=True)
    name = models.CharField(max_length=256, blank=True)
    package_url = models.CharField(max_length=256, blank=True)
    platform = models.CharField(max_length=128, blank=True)
    project_url = models.CharField(max_length=256, blank=True)
    project_urls = models.CharField(max_length=1024, blank=True)
    release_url = models.CharField(max_length=256, blank=True)
    requires_dist = models.CharField(max_length=1024, null=True, blank=True)
    requires_python = models.CharField(max_length=64, blank=True)
    summary = models.CharField(max_length=256, blank=True)
    version = models.CharField(max_length=32)
    yanked = models.BooleanField()
    yanked_reason = models.CharField(max_length=256, null=True, blank=True)
    releases = models.CharField(max_length=2048)

    def __str__(self):
        return self.name
