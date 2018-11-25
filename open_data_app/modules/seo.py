class Seo():

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {'city': 'Colleges and universities in {}, {}, USA',
                     'ownership': '{} colleges and universities in {}, USA',
                     'degree': 'Colleges and universities with {} as the highest in {}, USA',
                     'religion': '{} colleges and universities in {}, USA',
                     'level': 'Colleges and universities of {} institutional level in {}, USA',
                     'carnegie': '{} in {}, USA',
                     'locale': '{} colleges and universities in {}, USA',
                     'state': 'Colleges and universities in {}, {}, USA',
                     'hist_black': '{} colleges and universities in {}, USA',
                     'predom_black': '{} colleges and universities in {}, USA',
                     'hispanic': '{} colleges and universities in {}, USA',
                     'men_only': '{} colleges and universities in {}, USA',
                     'women_only': '{} colleges and universities in {}, USA',
                     'online_only': '{} colleges and universities in {}, USA',
                     'cur_operating': '{} colleges and universities in {}, USA',
                     'academics': 'American colleges and universities with programs in {}',
                     'academics_geo': 'Colleges and universities in {} with programs in {}',
                     }

        disciplines = ['agriculture', 'architecture', 'ethnic_cultural_gender', 'biological', 'business_marketing',
                       'communication', 'communications_technology', 'computer', 'construction', 'education',
                       'engineering', 'engineering_technology', 'english', 'family_consumer_science', 'language',
                       'health', 'history', 'security_law_enforcement', 'legal', 'humanities', 'library', 'mathematics',
                       'mechanic_repair_technology', 'military', 'multidiscipline', 'resources',
                       'parks_recreation_fitness', 'personal_culinary', 'philosophy_religious', 'physical_science',
                       'precision_production', 'psychology', 'public_administration_social_service',
                       'science_technology', 'social_science', 'theology_religious_vocation', 'transportation',
                       'visual_performing']
        try:
            if key in disciplines:
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