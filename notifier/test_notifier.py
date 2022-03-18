import unittest
from datetime import datetime
from unittest.mock import patch, ANY, call

from notifier import Company, Webinar, Event, ContentItem, CompanyForEvent, CompanyForWebinar, CompanyCompetitor, \
    MyObserver, CRAWLING_STATUSES


@patch("notifier.API.post")
class NotifierTestCase(unittest.TestCase):

    def test_notify_on_create(self, m_post):
        company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")
        competitor_company = Company(employees_min=10, employees_max=500, link="https://competitor.com",
                                     name="Competitor company")
        event = Event(start_date=datetime.now(), link="https://mycompany.com", name="Awesome event")
        webinar = Webinar(start_date=datetime.now(), link="https://mycompany.com", name="Awesome webinar")
        content_item = ContentItem(company=company, snippet="Some snippet here", link="https://mycompany.com",
                                   name="Awesome content")
        company_for_event = CompanyForEvent(event=event, company=company)
        company_for_webinar = CompanyForWebinar(webinar=webinar, company=company)
        company_competitor = CompanyCompetitor(company=company, competitor=competitor_company)

        for entity in [company, competitor_company, event, webinar, content_item, company_for_event,
                       company_for_webinar, company_competitor]:
            entity.attach(MyObserver())

        calls = [
            call(None, ANY, 'Company', ANY),
            call(None, ANY, 'Company', ANY),
            call(None, ANY, 'Event', ANY),
            call(None, ANY, 'Webinar', ANY),
            call(None, ANY, 'ContentItem', ANY),
            call(None, ANY, 'CompanyForEvent', ANY),
            call(None, ANY, 'CompanyForWebinar', ANY),
            call(None, ANY, 'CompanyCompetitor', ANY)
        ]
        m_post.assert_has_calls(calls, any_order=True)

    def test_notify_on_field_change(self, m_post):
        company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")
        company.attach(MyObserver())

        company.is_deleted = True
        args = m_post.call_args_list[1].args
        self.assertIsInstance(args[0], Company)
        self.assertIsInstance(args[1], Company)
        notify_on = 'Company'
        calls = [
            call(ANY, ANY, notify_on, 'is_deleted Updated from False to True'),
        ]
        m_post.assert_has_calls(calls)

    def test_do_not_notify_on_not_supported_field_change(self, m_post):
        company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")
        company.attach(MyObserver())

        company.employees_min = 15
        notify_on = 'Company'
        self.assertFalse(call(ANY, ANY, notify_on, 'employees_min Updated from 10 to 15') in m_post.call_args_list)

    def test_notify_on_field_change_to_different_object(self, m_post):
        company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")

        content_item = ContentItem(company=company, snippet="Some snippet here", link="https://mycompany.com",
                                   name="Awesome company")

        for entity in [company, content_item]:
            entity.attach(MyObserver())

        content_item.is_deleted = True
        content_item.is_blacklisted = True
        content_item.crawling_status = CRAWLING_STATUSES.CRAWLING
        args = m_post.call_args_list[3].args
        self.assertIsInstance(args[0], ContentItem)
        self.assertIsInstance(args[1], ContentItem)
        notify_on = 'Company'
        calls = [
            call(ANY, ANY, notify_on, 'is_deleted Updated from False to True'),
            call(ANY, ANY, notify_on, 'is_blacklisted Updated from False to True'),
            call(ANY, ANY, notify_on, 'crawling_status Updated from 0 to 5'),
        ]
        m_post.assert_has_calls(calls)

    def test_notify_on_delete(self, m_post):
        company = Company(employees_min=10, employees_max=50, link="https://mycompany.com", name="Awesome company")
        company.attach(MyObserver())

        company.__del__()

        create_args = m_post.call_args_list[0].args
        delete_args = m_post.call_args_list[1].args
        self.assertIsInstance(create_args[1], Company)
        self.assertIsInstance(delete_args[0], Company)
        calls = [
            call(None, ANY, 'Company', 'Attach observer'),
            call(ANY, None, 'Company', 'Company is deleted'),
        ]
        m_post.assert_has_calls(calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
