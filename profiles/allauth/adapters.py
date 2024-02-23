from allauth.account.adapter import DefaultAccountAdapter


class NoUsernameAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.username = data['email']  # username not in use
        user.email = data['email']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        user.save()
        return user
    
    # def login(self, request, user):
    #     print(f"dispatch - sc before: {request.session.session_key}")
    #     session_key = request.session.session_key
    #     super().login(request, user)
    #     print(f"dispatch - sc after: {request.session.session_key}")
    #     if session_key:
    #         Cart.objects.filter(session_key=session_key).update(user=user)
