from django.test import TestCase, Client
from homeowners.models import Homeowner
from common.models import Address, User
from staff.models import Staff


class TestLeadModel(object):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(username='uday', email='u@mp.com', role="ADMIN")
        self.user.set_password('uday2293')
        self.user.save()

        self.client.login(username='u@mp.com', password='uday2293')

        self.address = Address.objects.create(street="Gokul enclave colony",
                                              city="Hasthinapuram",
                                              state="Telangana",
                                              postcode="500079",
                                              country="AD")

        self.account = Staff.objects.create(name="account",
                                            email="account@gmail.com",
                                            phone="12345",
                                            billing_address=self.address,
                                            shipping_address=self.address,
                                            website="account.com",
                                            industry="IT",
                                            description="account",
                                            created_by=self.user)

        self.lead = Homeowner.objects.create(title="LeadCreation",
                                             first_name="anjali",
                                             last_name="k",
                                             email="anjalikotha1993@gmail.com",
                                             account=self.account,
                                             address=self.address,
                                             website="www.gmail.com",
                                             status="assigned",
                                             source="Call",
                                             opportunity_amount="700",
                                             description="Iam an Homeowner",
                                             created_by=self.user)
    # @pytest.mark.django_db(transaction=True)
    # def testaddress_post_object_creation(self):
    #     c = Address.objects.count()
    #     self.assertEqual(c, 1)

    # def test_get_addressobject_with_name(self):
    #     p = Address.objects.get(state="Telangana")
    #     self.assertEqual(p.street, "Gokul enclave colony")

    # def test_lead_object_creation(self):
    #     c = Homeowner.objects.count()
    #     self.assertEqual(c, 1)

    # def test_get_leadobjects_with_name(self):
    #     p = Homeowner.objects.get(title="LeadCreation")
    #     self.assertEqual(p.account.name, "account")


class LeadsPostrequestTestCase(TestLeadModel, TestCase):
    def test_valid_postrequesttestcase_date(self):
        data = {'title': 'LeadCreation', 'first_name': "kotha",
                'last_name': "anjali", 'email': "anjalikotha1993@gmail.com",
                'account': self.account, 'address': self.address,
                'website': "www.gmail.com", "status ": "assigned",
                "source": "Call",
                'opportunity_amount': "700",
                'description': "Iam an Homeowner"}
        resp = self.client.post('/homeowners/create/', data)
        self.assertEqual(resp.status_code, 200)

    def test_leads_list(self):
        self.lead = Homeowner.objects.all()
        response = self.client.get('/homeowners/list/')
        self.assertEqual(response.status_code, 200)

    def test_leads_list_html(self):
        response = self.client.get('/homeowners/list/')
        self.assertTemplateUsed(response, 'list.html')


class LeadsCreateUrlTestCase(TestLeadModel, TestCase):
    def test_leads_create_url(self):
        response = self.client.post('/homeowners/create/', {
                                    'title': 'LeadCreation',
                                    'first_name': "kotha",
                                    'email': "anjalikotha1993@gmail.com",
                                    'account': self.account,
                                    'address': self.address,
                                    'website': "www.gmail.com",
                                    "status": "assigned",
                                    "source": "Call",
                                    'opportunity_amount': "700",
                                    'description': "Iam an Homeowner",
                                    'created_by': self.user})
        self.assertEqual(response.status_code, 200)

    def test_leads_create_html(self):
        response = self.client.post('/homeowners/create/', {
            'title': 'LeadCreation', 'name': "kotha", 'email': "anjalikotha1993@gmail.com", 'account': self.account,
            'address': self.address, 'website': "www.gmail.com", 'status': "assigned",
            "source": "Call", 'opportunity_amount': "700", 'description': "Iam an Homeowner", 'created_by': self.user})
        self.assertTemplateUsed(response, 'create.html')


class LeadsEditUrlTestCase(TestLeadModel, TestCase):
    def test_leads_editurl(self):
        response = self.client.get('/homeowners/'+ str(self.lead.id) +'/edit/')
        self.assertEqual(response.status_code, 200)


class LeadsViewTestCase(TestLeadModel, TestCase):

    def test_leads_view(self):
        Homeowner.objects.create(title="LeadCreationbylead",
                                 first_name="anjali",
                                 last_name="k",
                                 email="srilathakotha1993@gmail.com",
                                 account=self.account,
                                 address=self.address,
                                 website="www.gmail.com",
                                 status='converted',
                                 source="Call",
                                 opportunity_amount="900",
                                 description="Iam an Opportunity",
                                 created_by=self.user)
        response = self.client.get('/homeowners/'+ str(self.lead.id) +'/view/')
        self.assertEqual(response.status_code, 200)


class LeadsRemoveTestCase(TestLeadModel, TestCase):

    def test_leads_remove(self):
        response = self.client.get('/homeowners/'+ str(self.lead.id) +'/delete/')
        self.assertEqual(response['location'], '/homeowners/list/')

    def test_leads_remove_status(self):
        Homeowner.objects.filter(id=self.lead.id).delete()
        response = self.client.get('/homeowners/list/')
        self.assertEqual(response.status_code, 200)
