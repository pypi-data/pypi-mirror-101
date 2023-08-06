# Modular Message Bot
App/Package that takes data from sources and sends them somewhere based on a schedule that is defined in YAML

## Notes:
It's probably really easy to write jobs that are not escaped correctly, so be careful! It is a good idea to read the
source anyway especially of the handlers you are using!
The best way to start is to look at some example jobs in the component-resources folder

## Documentation
* [Code Docs](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot.html)
* [Pdoc index](https://mage-sauce.gitlab.io/programs/pdoc-index.html)
* [Config](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/config.html)
* [Modules/Handlers](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/handlers.html)
* [Health check - readiness and liveness](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/utils/healthcheck_utils.html)
* [Extensions (advanced)](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/utils/module_util.html)
* [Run with blocking scheduler (docker default)](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/run.html)
* [Run a job by id](https://mage-sauce.gitlab.io/programs/modular-message-bot/modular_message_bot/run_by_id.html)
* [Example Job configs](https://gitlab.com/mage-sauce/programs/modular-message-bot/-/tree/develop/tests/component-resources)

## Help wanted
We are actively looking for help with anything including but not limited to design work, documentation and coding.
To contribute please open a ticket first.
I am relatively new to Python so please make any code suggestions in issues. I am open to new ideas

## Installing
If you are not customising anything, the best way to run this project is via Docker

### Docker

An example of running the job in Docker. Note you will need to set DOCKER_IMAGE from one of the sources below
```shell
mkdir job-configs
touch job-configs/jobs.yml
echo "jobs:" >> job-configs/jobs.yml
echo "  - schedule: '* * * * *'" >> job-configs/jobs.yml
echo "    outputs:" >> job-configs/jobs.yml
echo "      - code: stdout" >> job-configs/jobs.yml
echo "        parameters:" >> job-configs/jobs.yml
echo "          message: \"Hello :)\"" >> job-configs/jobs.yml
docker pull registry.gitlab.com/mage-sauce/programs/modular-message-bot:stable
docker run --rm -it -v `pwd`/job-configs:/job-configs -e "RUN_DETAILS_DIR=/job-configs" ${DOCKER_IMAGE}
```

#### Docker - gitlab.com
See: [Gitlab Containers](https://gitlab.com/mage-sauce/programs/modular-message-bot/container_registry/1519867)
```shell
export DOCKER_IMAGE=registry.gitlab.com/mage-sauce/programs/modular-message-bot:stable
# Run the commands above under Docker
```

#### Docker - hub.docker.com
See: [Docker Hub](https://hub.docker.com/r/magesauce/modular-message-bot)
```shell
export DOCKER_IMAGE=magesauce/modular-message-bot:stable
# Run the commands above under Docker
```

### Package (PyPI)
Once installed from PyPI you should be able to run like:
```shell
docker run --rm -it python:3.8.7 bash
# Command from below to install such as `pip install modular-message-bot`
mkdir /job-configs
touch /job-configs/jobs.yml
echo "jobs:" >> /job-configs/jobs.yml
echo "  - schedule: '* * * * *'" >> /job-configs/jobs.yml
echo "    outputs:" >> /job-configs/jobs.yml
echo "      - code: stdout" >> /job-configs/jobs.yml
echo "        parameters:" >> /job-configs/jobs.yml
echo "          message: \"Hello :)\"" >> /job-configs/jobs.yml
RUN_DETAILS_DIR=/job-configs python -m modular_message_bot.run
```

#### Package (PyPI) - gitlab.com Stable (master)
See: [Gitlab PyPI](https://gitlab.com/mage-sauce/programs/modular-message-bot/-/packages)
```shell
pip install modular-message-bot --extra-index-url https://gitlab.com/api/v4/projects/22692467/packages/pypi/simple
```

#### Package (PyPI) - pypi.org Stable (master)
See: [PyPI](https://pypi.org/project/modular-message-bot/)
```shell
pip install modular-message-bot
```

#### Package (PyPI) - https://test.pypi.org/ Test (develop)
See: [TestPyPI](https://test.pypi.org/project/modular-message-bot/)
```shell
pip install modular-message-bot --extra-index-url https://test.pypi.org/simple/
```

## Run Detail (Job Config)
The run details config is read from YAML. Have a look in `tests/component-resources` for examples. By default, we load
no jobs. All the methods below can be used (i.e. it will combine them)

### Run Detail Methods
1. A base64 encoded config (e.g. ENV). Set RUN_DETAILS_B64 to the appropriate value
   For example (`cat config/jobs.yml | base64 -w0`)
2. A Single file. This uses the config `RUN_DETAILS_FILE` to specify it
3. A directory containing files with extension `.yaml` or `.yml`. This directory is specified with the config
   RUN_DETAILS_FILE

## Job strings
Job strings are messages you want to interpolate with inputs and then pass to output modules.
Each input has a code that is replaced inside the job string. For example `var: datehere` in an input module, would
replace `{datehere}` in any job string.
Each job string has a code and that code is then interpolated into the output parameters.
E.g.
```yaml
strings:
  my_message: "This is a test message"
```
Would replace `{my_message}` in any output parameter for that job
