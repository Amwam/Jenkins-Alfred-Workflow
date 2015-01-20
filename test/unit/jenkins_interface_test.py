from unittest import TestCase

from mock import patch, Mock

from workflow import Workflow
from jenkins.jenkins_interface import JenkinsInterface, NoJobsFound


JENKINS_URL = "http://some-url:8080"


class TestJenkinsInterface(TestCase):
    def setUp(self):
        self.workflow = Workflow()

        self.old_jenkins_url = self.workflow.settings.get('jenkins_url')
        self.workflow.settings['jenkins_url'] = JENKINS_URL
        self.jenkins_interface = JenkinsInterface(self.workflow)

    def tearDown(self):
        self.workflow.settings['jenkins_url'] = self.old_jenkins_url

    def _patch_get_with_response(self, mock_get, response):
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_response.json.return_value = response

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_jobs(self, mock_get):
        self._patch_get_with_response(mock_get, {'jobs': [{'name': 'test'}]})
        jobs = self.jenkins_interface.get_all_jobs()
        self.assertEqual(1, len(jobs))

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_jobs_finds_no_jobs_raises_error(self, mock_get):
        self._patch_get_with_response(mock_get, {'jobs': []})
        self.assertRaises(NoJobsFound, self.jenkins_interface.get_all_jobs)

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_jobs_filters_with_query_no_jobs_does_not_error(self, mock_get):
        self._patch_get_with_response(mock_get, {'jobs': []})

        jobs = self.jenkins_interface.get_all_jobs(query="query")
        self.assertEqual(0, len(jobs))


    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_jobs_filters_with_query(self, mock_get):
        self._patch_get_with_response(mock_get, {
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
        self.assertTrue(all(["two" in jobs[0].name, "one" in jobs[1].name]))

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_failing_jobs(self, mock_get):
        self._patch_get_with_response(mock_get, {
            'jobs': [
                {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL}
            ]
        })
        jobs = self.jenkins_interface.get_failed_jobs()

        self.assertEqual(2, len(jobs))
        self.assertEqual('test1', jobs[0].name)
        self.assertEqual('test4', jobs[1].name)


    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_failing_jobs_with_query(self, mock_get):
        self._patch_get_with_response(mock_get, {
            'jobs': [
                {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL}
            ]
        })
        jobs = self.jenkins_interface.get_failed_jobs('test1')

        self.assertEqual(1, len(jobs))
        self.assertEqual('test1', jobs[0].name)

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_building_jobs(self, mock_get):
        self._patch_get_with_response(mock_get, {
            'jobs': [
                {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL},
                {'name': 'test5', 'color': 'redanime', 'url': JENKINS_URL}
            ]
        })
        jobs = self.jenkins_interface.get_building_jobs()

        self.assertEqual(2, len(jobs))
        self.assertEqual('test4', jobs[0].name)
        self.assertEqual('test5', jobs[1].name)

    @patch("jenkins.jenkins_interface.web.get")
    def test_get_all_building_jobs_with_query(self, mock_get):
        self._patch_get_with_response(mock_get, {
            'jobs': [
                {'name': 'test1', 'color': 'red', 'url': JENKINS_URL},
                {'name': 'test2', 'color': 'blue', 'url': JENKINS_URL},
                {'name': 'test3', 'color': 'yellow', 'url': JENKINS_URL},
                {'name': 'test4', 'color': 'redanime', 'url': JENKINS_URL},
                {'name': 'test5', 'color': 'redanime', 'url': JENKINS_URL}
            ]
        })
        jobs = self.jenkins_interface.get_building_jobs('4')

        self.assertEqual(1, len(jobs))
        self.assertEqual('test4', jobs[0].name)
