from djoser.email import ActivationEmail
from decouple import config



class ActivationEmail(ActivationEmail):
    template_name = "email_activation.html"

    def get_context_data(self):   
        context =  super().get_context_data()
        print(context["domain"])
        context["domain"] = config("FRONTEND_HOST")
        print(context["domain"])
        return context
    
    def send(self, to, *args, **kwargs):
        print(f"sending email to {to}")
        return super().send(to, *args, **kwargs)