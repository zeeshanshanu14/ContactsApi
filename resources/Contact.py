from flask import request
from flask_restful import Resource
from Model import db, Contact, ContactSchema, Email, EmailSchema

contacts_schema = ContactSchema(many=True)
contact_schema = ContactSchema()
email_shema = EmailSchema()
emails_schema = EmailSchema(many=True)


class ContactResource(Resource):
    def get(self):

        ###
        json_data = request.get_json(force=False)
        emails = Email.query.all()
        emails = emails_schema.dump(emails).data
        if json_data and json_data['username']:
            # Validate and deserialize input
            data, errors = contact_schema.load(json_data)
            if errors:
                return errors, 422
            contact = Contact.query.filter_by(username=data['username']).first()
            contact = contact_schema.dump(contact).data
            if contact:
                contact = self.enrich_with_emails([contact], emails)
                return {'status': 'success', 'data': contact}, 200
            else:
                return {'message': 'Contact does not exist'}, 400
        ####
        contacts = Contact.query.all()
        contacts = contacts_schema.dump(contacts).data

        result_list = self.enrich_with_emails(contacts, emails)

        return {'status': 'success', 'data': result_list}, 200

    def enrich_with_emails(self, contacts, emails):
        result_list = list()
        for contact_dict in contacts:
            new_contact_dict = contact_dict
            emails_list = ''
            for email_dict in emails:
                if email_dict['contact_id'] == contact_dict['id']:
                    emails_list = emails_list + "; " + email_dict['email'] if emails_list else email_dict['email']
            new_contact_dict['email'] = emails_list
            result_list.append(new_contact_dict)
        return result_list

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(username=data['username']).first()
        if contact:
            return {'message': 'Contact already exists'}, 400
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

        return {"status": 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(id=data['id']).first()

        if not contact:
            return {'message': 'Contact does not exist'}, 400
        contact.username = data['username']
        contact.firstname = data['firstname']
        contact.lastname = data['lastname']

        # lets try to update the email if new email add it
        # contact = Contact.query.filter_by(id=data['id']).first()

        contact_rec = contact_schema.dump(contact).data
        data_email, error = email_shema.load(json_data)
        if data_email['email']:
            # get all emails id for this contact if any
            existing_emails = Email.query.filter_by(contact_id=contact_rec['id']).all()
            existing_emails = emails_schema.dump(existing_emails).data

            found = False
            found_email_key = None
            if existing_emails:
                for e in existing_emails:
                    if e['email'] == data_email['email']:
                        #already exisits do nothing
                        found = True
                        found_email_key = e['id']
                        break

            if not found:
                # this is brand new record so dont expect an exisitng for this one
                email = Email(contact_rec['id'], data_email['email'])
                db.session.add(email)

        db.session.commit()

        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = contact_schema.load(json_data)
        if errors:
            return errors, 422
        contact = Contact.query.filter_by(username=data['username']).delete()
        db.session.commit()

        result = contact_schema.dump(contact).data

        return {"status": 'success', 'data': result}, 204
