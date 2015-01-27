from workflow import Workflow
from jenkins.jenkins_interface import JenkinsInterface, NoJobsFound


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

    try:
        jobs = options[command](query)

        if not query:
            wf.add_item("Open Jenkins", arg=interface.get_jenkins_url(), valid=True)

        for job in jobs:
            wf.add_item(job.name, subtitle=job.description, arg=job.url, valid=True, icon=job.image)
    except NoJobsFound:
        wf.logger.debug("Could not find any jobs for instance: %s", wf.settings['jenkins_url'])
        wf.add_item("Error: No jobs found")

    wf.send_feedback()


if __name__ == '__main__':  # pragma: no cover
    print Workflow().run(main)
