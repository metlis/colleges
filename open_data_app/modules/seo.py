class Seo():
    disciplines = ['agriculture', 'architecture', 'ethnic_cultural_gender', 'biological', 'business_marketing',
                   'communication', 'communications_technology', 'computer', 'construction', 'education',
                   'engineering', 'engineering_technology', 'english', 'family_consumer_science', 'language',
                   'health', 'history', 'security_law_enforcement', 'legal', 'humanities', 'library', 'mathematics',
                   'mechanic_repair_technology', 'military', 'multidiscipline', 'resources',
                   'parks_recreation_fitness', 'personal_culinary', 'philosophy_religious', 'physical_science',
                   'precision_production', 'psychology', 'public_administration_social_service',
                   'science_technology', 'social_science', 'theology_religious_vocation', 'transportation',
                   'visual_performing']

    @classmethod
    def generate_title(cls, key, value, geo):
        templates = {'city': '2019 colleges and universities in {}, {}, USA',
                     'ownership': '2019 {} colleges and universities in {}, USA',
                     'degree': '2019 colleges and universities with {} as the highest in {}, USA',
                     'religion': '2019 {} colleges and universities in {}, USA',
                     'level': '2019 colleges and universities of {} institutional level in {}, USA',
                     'carnegie': '2019 {} in {}, USA',
                     'locale': '2019 {} colleges and universities in {}, USA',
                     'state': '2019 colleges and universities in {}, {}, USA',
                     'hist_black': '2019 {} colleges and universities in {}, USA',
                     'predom_black': '2019 {} colleges and universities in {}, USA',
                     'hispanic': '2019 {} colleges and universities in {}, USA',
                     'men_only': '2019 {} colleges and universities in {}, USA',
                     'women_only': '2019 {} colleges and universities in {}, USA',
                     'online_only': '2019 {} colleges and universities in {}, USA',
                     'cur_operating': '2019 {} colleges and universities in {}, USA',
                     'academics': '2019 american colleges and universities with programs in {}',
                     'academics_geo': '2019 colleges and universities in {} with programs in {}',
                     }

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

    @classmethod
    def generate_description(cls, key, value, geo):
        templates = {'city': 'This page provides details about colleges and universities based in {}, {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'ownership': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'degree': 'This page provides details about colleges and universities with {} as the highest in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'religion': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'level': 'This page provides details about colleges and universities of {} institutional level in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'carnegie': 'This page provides details about {} in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'locale': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'state': 'This page provides details about colleges and universities in {}, {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'hist_black': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'predom_black': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'hispanic': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'men_only': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'women_only': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'online_only': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'cur_operating': 'This page provides details about {} colleges and universities in {}, USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'academics': 'This page provides details about colleges and universities with programs in {} in USA in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     'academics_geo': 'This page provides details about colleges and universities in {} with programs in {} in 2019. Here you can find supporting data on student completion, debt and repayment, earnings, and more.',
                     }
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