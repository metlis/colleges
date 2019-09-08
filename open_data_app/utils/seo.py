from open_data_app.models.college import College
from open_data_app.models.dictionary import Dictionary
from django.core.exceptions import ObjectDoesNotExist


class Seo:
    disciplines = College.get_disciplines()

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {}

        try:
            titles = Dictionary.objects.get(name='seo_titles').content
            if titles is not None:
                templates = titles
        except ObjectDoesNotExist:
            pass

        string = cls.generate_string(templates, key, value, geo)
        return string

    @classmethod
    def generate_description(cls, key, value, geo):
        templates = {}

        try:
            descriptions = Dictionary.objects.get(name='seo_descriptions').content
            if descriptions is not None:
                templates = descriptions
        except ObjectDoesNotExist:
            pass

        string = cls.generate_string(templates, key, value, geo)
        return string

    @classmethod
    def generate_string(cls, templates, key, value, geo):
        try:
            if key in cls.disciplines:
                if not geo:
                    template = templates['academics']
                    return template.format(value)
                else:
                    template = templates['academics_geo']
                    return template.format(geo, value)
            else:
                template = templates[key]
                if geo:
                    return template.format(value, geo)
                else:
                    return template.format(value, geo).replace(', USA', ' USA')
        except:
            return 'Colleges'
