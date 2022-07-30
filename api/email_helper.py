from djoser.email import ActivationEmail
from decouple import config
from url_shortner.celery import app
from django.utils.decorators import method_decorator
from url_shortner.celery import app


class ActivationEmail(ActivationEmail):
    template_name = "email_activation.html"

    def get_context_data(self):   
        context =  super().get_context_data()
        print(context["domain"])
        context["domain"] = config("FRONTEND_HOST")
        print(context["domain"])
        return context
    
    @method_decorator(app.task)
    def send(self, to, *args, **kwargs):
        print(f"sending email to {to}")
        return super().send(to, *args, **kwargs)