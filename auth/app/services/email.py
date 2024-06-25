# send_mail
from app.config.email import send_mail
from app.models.user import UserModel
from app.config.security import hashed_password
from app.config.setting import BACKEND_HOST
from fastapi import BackgroundTasks
# from app

async def send_verification_mail(user: UserModel ):
    get_context_str = user.get_context_str()
    token = hashed_password(get_context_str)
    url = f"{BACKEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    context = {
        "url": url,
        "username":f"{user.first_name} {user.last_name}",
        "application":"RaiBott"
    }
    subject = "This is only for user verification"

    await send_mail(email=[user.email], subject=subject, template_name="users/accountverification.html", context=context)

async def send_activation_confirmation_mail(user: UserModel):
    context = {
        "url": BACKEND_HOST,
        "username":f"{user.first_name} {user.last_name}",
        "application":"RaiBott"
    }
    subject = "This is only for user confirmation"

    await send_mail([user.email], subject, "users/account-verification-confirmation.html", context )