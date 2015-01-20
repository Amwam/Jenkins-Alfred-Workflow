from unittest import TestCase

from mockito import mock, any, when

from workflow import Workflow
from jenkins.jenkins_interface import JenkinsInterface


JENKINS_URL = "http://some-url:8080"


class TestJenkinsInterface(TestCase):
    def setUp(self):
        self.mock_wrapper = mock()
        self.workflow = Workflow()
        self.workflow.settings['jenkins_url'] = "%s" % JENKINS_URL
        self.jenkins_interface = JenkinsInterface(self.workflow, self.mock_wrapper)
        self.mock_response = mock()
        when(self.mock_wrapper).get(any()).thenReturn(self.mock_response)

    def test_get_all_jobs(self):
        when(self.mock_response).json().thenReturn({'jobs': [{'name': 'test'}]})
        jobs = self.jenkins_interface.get_all_jobs()
        self.assertEqual(1, len(jobs))

    def test_get_all_jobs_filters_with_query(self):
        when(self.mock_response).json().thenReturn({
            'jobs': [
                {'name': 'test one'},
                {'name': 'test two'},
                {'name': 'ignore one'},
                {'name': 'ignore two'}
            ]
        })

        query = "test"
        jobs = self.jenkins_interface.get_all_jobs(query=query)
        self.assertEqual(2, len(jobs))
        self.assertTrue(all(["one" in jobs[0].name, "two" in jobs[1].name]))

    def test_get_all_failing_jobs(self):
        when(self.mock_response).json().thenReturn(
            {
                'jobs': [
                    {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                    {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                    {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                    {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL}
                ]
            }
        )
        jobs = self.jenkins_interface.get_failed_jobs()

        self.assertEqual(2, len(jobs))
        self.assertEqual('test1', jobs[0].name)
        self.assertEqual('test4', jobs[1].name)


    def test_get_all_failing_jobs_with_query(self):
        when(self.mock_response).json().thenReturn(
            {
                'jobs': [
                    {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                    {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                    {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                    {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL}
                ]
            }
        )
        jobs = self.jenkins_interface.get_failed_jobs('test1')

        self.assertEqual(1, len(jobs))
        self.assertEqual('test1', jobs[0].name)

    def test_get_all_building_jobs(self):
        when(self.mock_response).json().thenReturn(
            {
                'jobs': [
                    {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                    {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                    {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                    {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL},
                    {'name': 'test5', 'color': 'redanime', 'url': JENKINS_URL}
                ]
            }
        )
        jobs = self.jenkins_interface.get_building_jobs()

        self.assertEqual(2, len(jobs))
        self.assertEqual('test4', jobs[0].name)
        self.assertEqual('test5', jobs[1].name)

    def test_get_all_building_jobs_with_query(self):
        when(self.mock_response).json().thenReturn(
            {
                'jobs': [
                    {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                    {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                    {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                    {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL},
                    {'name': 'test5', 'color': 'redanime', 'url': JENKINS_URL}
                ]
            }
        )
        jobs = self.jenkins_interface.get_building_jobs('4')

        self.assertEqual(1, len(jobs))
        self.assertEqual('test4', jobs[0].name)
