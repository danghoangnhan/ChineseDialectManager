from django.contrib import admin
from rules.models import  rules
from rules.ToneRuleAdmin import RulesAdmin
admin.register(rules, RulesAdmin)
