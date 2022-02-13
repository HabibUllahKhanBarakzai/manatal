from cerberus import errors


class SpecificEmailError(errors.BasicErrorHandler):
    """
        This Error class Overriden to send proper
         error message in case of Email Mismatch
    """
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REGEX_MISMATCH.code] = 'The email provided is in incorrect format'


class Schemas:
    Student = {
        'school_id': {'type': 'integer', 'min': 1},
        'user': {
            'type': 'dict',
            'required': True,
            'schema': {
                'first_name': {'required': True, 'type': 'string'},
                'last_name': {'required': True, 'type': 'string'},
                'email': {
                    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
                    'type': 'string',
                    'required': True,

                }
            }
        }
    }
    StudentWithOutSchoolId = {
        'user': {
            'type': 'dict',
            'required': True,
            'schema': {
                'first_name': {'required': True, 'type': 'string'},
                'last_name': {'required': True, 'type': 'string'},
                'email': {
                    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
                    'type': 'string',
                    'required': True,

                }
            }
        }
    }

    StudentPartialUpdateSchema = {
        'school_id': {
            'type': 'integer',
            'required': False,
        },
        'user': {
            'type': 'dict',
            'required': False,
            'schema': {
                'first_name': {'required': False, 'type': 'string'},
                'last_name': {'required': False, 'type': 'string'},
                'email': {
                    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$",
                    'type': 'string',
                    'required': False,

                }
            }
        }
    }


STUDENT_VALIDATION_SCHEME = {
    'post': Schemas.Student,
    'patch': Schemas.StudentWithOutSchoolId,
}

LINKED_STUDENT_SCHOOL_SCHEMA = {
    'post': Schemas.StudentWithOutSchoolId,
    'patch': Schemas.StudentPartialUpdateSchema,
}
