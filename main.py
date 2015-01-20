from workflow import Workflow
from jenkins.jenkins_interface import JenkinsInterface


def main(wf):
    command = wf.args[0]
    query = wf.args[1] if len(wf.args) > 1 else None
    interface = JenkinsInterface(wf)

    options = {
        'set_url': interface.set_jenkins_url,
        'failing': interface.get_failed_jobs,
        'building': interface.get_building_jobs,
        'all': interface.get_all_jobs
    }

    for job in options[command](query):
        wf.add_item(job.name, subtitle=job.description, arg=job.url, valid=True, icon=job.image)

    wf.send_feedback()


if __name__ == '__main__':
    print Workflow().run(main)


