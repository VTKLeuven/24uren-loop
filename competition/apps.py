from django.apps import AppConfig


class CompetitionConfig(AppConfig):
    name = 'competition'

    def ready(self):
        import competition.signals
