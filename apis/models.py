from django_mongoengine import Document, fields

class Freelancer(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    country = fields.StringField(blank=False)
    phone_number = fields.StringField(blank=True)
    agreed_to_terms = fields.BooleanField(default=False, blank=False)
    is_active = fields.BooleanField(default=False)
    activation_token = fields.StringField(blank=True)
    activation_token_valid = fields.BooleanField(blank=True, default=True)
    password_reset_token = fields.StringField(blank=True)
    password_reset_token_valid = fields.BooleanField(blank=True, default=False)
    session_tokens = fields.ListField(fields.StringField(), blank=True, default=list)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'password_reset_token', 'activation_token'],
    }

    def add_session_token(self, token):
        if len(self.session_tokens) < 4:
            self.session_tokens.append(token)
        else:
            self.session_tokens.pop(0)
            self.session_tokens.append(token)
        self.save()

    def remove_session_token(self, token):
        if token in self.session_tokens:
            self.session_tokens.remove(token)
            self.save()

    def is_session_token_valid(self, token):
        return token in self.session_tokens

class Client(Document):
    email = fields.EmailField(blank=False, unique=True)
    first_name = fields.StringField(blank=False)
    last_name = fields.StringField(blank=False)
    password = fields.StringField(blank=False)
    country = fields.StringField(blank=False)
    phone_number = fields.StringField(blank=True)
    agreed_to_terms = fields.BooleanField(default=False, blank=False)
    is_active = fields.BooleanField(default=False)
    activation_token = fields.StringField(blank=True)
    activation_token_valid = fields.BooleanField(blank=True, default=True)
    password_reset_token = fields.StringField(blank=True)
    password_reset_token_valid = fields.BooleanField(blank=True, default=False)
    session_tokens = fields.ListField(fields.StringField(), blank=True, default=list)

    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'password_reset_token', 'activation_token'],
    }

    def add_session_token(self, token):
        if len(self.session_tokens) < 4:
            self.session_tokens.append(token)
        else:
            self.session_tokens.pop(0)
            self.session_tokens.append(token)
        self.save()

    def remove_session_token(self, token):
        if token in self.session_tokens:
            self.session_tokens.remove(token)
            self.save()

    def is_session_token_valid(self, token):
        return token in self.session_tokens
