import base64

from workflow import web
from jenkins.job import Job


class JenkinsInterface(object):
    def __init__(self, workflow):
        super(JenkinsInterface, self).__init__()
        self._workflow = workflow

    def set_jenkins_url(self, url):
        self._workflow.settings['jenkins_url'] = url
        self._workflow.settings.save()

    def set_login(self, query):
        query = query.split(' ')
        username = query[0]
        api_token = query[1]
        self._workflow.settings['username'] = username
        self._workflow.save_password('jenkins_api_token', api_token)

    def clear_login(self):
        del self._workflow.settings['username']
        self._workflow.clear_password('jenkins_api_token')

    @staticmethod
    def parse_jobs(data):
        jobs = [Job(data)]
        if data.get('jobs', []):
            for job in data.get('jobs', []):
                job['name'] = '{}/{}'.format(data.get('name'), job['name'])
                jobs.append(Job(job))
        return jobs

    def get_all_jobs(self, query=None):
        def _get_jobs_json():
            jenkins_url = self.get_jenkins_url()
            headers = {}
            job_params = 'name,url,color,description'
            url = "{}/api/json?tree=jobs[{params},jobs[{params}]]".format(jenkins_url,
                                                                          params=job_params)
            headers = {}
            if 'username' in self._workflow.settings:
                username = self._workflow.settings['username']
                token = self._workflow.get_password('jenkins_api_token')
                base64string = base64.encodestring('%s:%s' % (username, token)).replace('\n', '')
                headers['Authorization'] = "Basic %s" % base64string
            return web.get(url, headers=headers).json()['jobs']

        jobs = []
        for job in _get_jobs_json():
            jobs.extend(self.parse_jobs(job))

        if query:
            filtered_jobs = self._workflow.filter(query, jobs, lambda x: x.name)
            return filtered_jobs
        else:
            if not jobs:
                raise NoJobsFound()
            return jobs

    def get_failed_jobs(self, query=None):
        all_jobs = self.get_all_jobs(query)
        return [job for job in all_jobs if 'red' in job.status]

    def get_building_jobs(self, query=None):
        all_jobs = self.get_all_jobs(query)
        return [job for job in all_jobs if 'anime' in job.status]

    def get_jenkins_url(self):
        jenkins_url = self._workflow.settings.get('jenkins_url')
        if not jenkins_url:
            self._workflow.add_item("No jenkins url set, please set using command: 'jenkins_url'")
            self._workflow.send_feedback()
        return jenkins_url


class NoJobsFound(Exception):
    pass
