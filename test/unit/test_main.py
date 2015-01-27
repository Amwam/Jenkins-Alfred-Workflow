from unittest import TestCase

from mock import patch, Mock

from jenkins.jenkins_interface import JenkinsInterface, NoJobsFound
from jenkins.job import Job
from workflow import Workflow
from main import main


class TestMain(TestCase):
    def setUp(self):
        self.mock_interface = Mock(JenkinsInterface)
        self.workflow = Mock(Workflow)

    @patch("main.JenkinsInterface.get_all_jobs")
    @patch("main.JenkinsInterface.get_jenkins_url")
    def test_main_calls_add_item_for_all_jobs(self, get_jenkins_url, all_jobs):
        self.workflow.args = ['all']

        job_data = {
            'name': 'dummy job',
            'url': 'http://some-url',
            'color': 'blue'
        }

        all_jobs.return_value = [Job(job_data), Job(job_data)]
        get_jenkins_url.return_value = "http://jenkins-url.com"

        main(self.workflow)

        self.assertEquals(3, self.workflow.add_item.call_count)
        self.assertEqual("http://jenkins-url.com", self.workflow.add_item.mock_calls[0][2]['arg'])
        self.workflow.send_feedback.assert_called_once()


    @patch("main.JenkinsInterface.get_all_jobs", )
    def test_main_calls_add_item_once_with_error_for_all_jobs_none_returned(self, all_jobs):
        self.workflow.args = ['all']
        self.workflow.settings = {'jenkins_url': 'http://some-url:8080'}
        all_jobs.side_effect = NoJobsFound

        main(self.workflow)

        self.workflow.add_item.assert_called_once_with("Error: No jobs found")
        self.workflow.send_feedback.assert_called_once()
