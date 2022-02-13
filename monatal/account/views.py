from typing import Dict

from cerberus import Validator
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..school.validations import SpecificEmailError
from .models import User


class ValidatedModelViewSet(ModelViewSet):
    validation_schema = {}
    validation_error_handler = None
    allowed_validation_methods = ['post', 'put', 'patch']

    @classmethod
    def validate_user_input(cls, request):
        method = request.method.lower()
        schema = cls.validation_schema.get(method)

        if method in cls.allowed_validation_methods and schema:
            validator = Validator()
            if cls.validation_error_handler:
                validator = Validator(error_handler=SpecificEmailError)
            if not validator.validate(request.data, schema):
                raise ValidationError({'errors': validator.errors})

    def initial(self, request, *args, **kwargs):
        super(ValidatedModelViewSet, self).initial(request, *args, **kwargs)
        self.validate_user_input(request)


class BaseRegisterView(ValidatedModelViewSet):
    """Base API to register The user, it can either be Student or Tin future
        teacher or any other
    """

    @classmethod
    def create_type(cls, user: User, data: Dict):
        """OverRide this method to either create any type os user
        linked to User model
        """
        raise NotImplemented("create_type method must be overridden")

    @classmethod
    def create_serialized_user_object(cls, user: User) -> Dict:
        """Serialize User object """
        return {"email": user.email, "date_joined": user.date_joined}

    def create(self, request, *args, **kwargs):
        """Create the base User"""

        try:
            user = User.objects.create_user(**request.data.pop('user'))
        except IntegrityError as exc:
            raise ValidationError({
                'message': 'the user with these credentials already exists.',
                'traceback': exc.with_traceback(exc.__traceback__)

            })

        self.create_type(user, request.data)
        data = self.create_serialized_user_object(user)

        return Response(data=data,
                        status=status.HTTP_201_CREATED)
