from modeltranslation.translator import translator, TranslationOptions, register
from .models import Course, Page

@register(Course)  
class CourseTranslationOptions(TranslationOptions):
	fields = ('course_name', 'description')
	#required_languages = ('en', 'ar') to make translation required
	#required_languages = {'en': ('title', 'text'), 'default': ('title',)}
	# For English, all fields (both title and text) are required; 
	# for all other languages - only title is required. The 'default' is optional

@register(Page)  
class PageTranslationOptions(TranslationOptions):
	fields = ('title', 'description')

# translator.register(Course, CourseTranslationOptions)