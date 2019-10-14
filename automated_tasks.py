import random
import string

from Model import Email, EmailSchema, Contact, ContactSchema, db
from run import celery
from logging import getLogger

logger = getLogger(__name__)
contacts_schema = ContactSchema(many=True)
contact_schema = ContactSchema()
email_shema = EmailSchema()
emails_schema = EmailSchema(many=True)


def create_random_contact(random_contact_dict):
    json_data = random_contact_dict
    if not json_data:
        return {'message': 'No input data provided'}, 400
    # Validate and deserialize input
    data, errors = contact_schema.load(json_data)
    if errors:
        print('malformed data')
    contact = Contact.query.filter_by(username=data['username']).first()
    if contact:
        print('Contact already exists')
    contact = Contact(
        username=json_data['username'],
        firstname=json_data['firstname'],
        lastname=json_data['lastname']
    )

    db.session.add(contact)

    # contact id should be present at this point get it to inset in email table
    contact_rec = Contact.query.filter_by(username=data['username']).first()
    contact_rec = contact_schema.dump(contact_rec).data
    data_email, error = email_shema.load(json_data)
    # this is brand new record so dont expect an exisitng for this one
    if data_email['email']:
        email = Email(contact_rec['id'], data_email['email'])
        db.session.add(email)
    db.session.commit()

    result = {**contact_schema.dump(contact).data, **data_email}
    print('contact created with username.{}'.format(contact_rec['username']))

    return 1


def randomString2(stringLength=8):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))


@celery.task()
def create_random_contact_15sec():
    random_con = {
        "username": randomString2(6),
        "firstname": randomString2(5),
        "lastname": randomString2(7),
        "email": randomString2(8)
    }
    create_random_contact(random_con)


@celery.task()
def delete_task_older_1min():
    # errg didnt check 1 min older contact need to be deleted.. i m not maintaining insert timestamp.. too late
    min_id = Contact.query.first()
    contact_rec = contact_schema.dump(min_id).data
    contact_del_rec = Contact.query.filter_by(username=contact_rec['username']).delete()
    db.session.commit()
    logger.info('{} User Deleted !'.format(contact_rec['username']))
    return 1


@celery.task()
def print_hello():
    logger = getLogger(__name__)
    logger.info("Hello")
