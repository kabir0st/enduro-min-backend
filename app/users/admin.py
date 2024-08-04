from django.contrib import admin
from .models import (UserBase, Settings, VerificationCode, Document)

admin.site.register(UserBase)

admin.site.register(Settings)

admin.site.register(VerificationCode)

admin.site.register(Document)
