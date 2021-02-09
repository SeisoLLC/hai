#!/usr/bin/env python3
"""
Task execution tool & library
"""

import json
import sys
from logging import basicConfig, getLogger
from pathlib import Path

import docker
import git
from invoke import task


# Helper functions
def opinionated_docker_run(
    *,
    image: str,
    auto_remove: bool = False,
    command: str = None,
    detach: bool = True,
    environment: dict = {},
    expected_exit: int = 0,
    volumes: dict = {},
):
    """Perform an opinionated docker run"""
    container = CLIENT.containers.run(
        auto_remove=auto_remove,
        command=command,
        detach=detach,
        environment=environment,
        image=image,
        volumes=volumes,
    )

    if not auto_remove:
        response = container.wait(condition="not-running")
        decoded_response = container.logs().decode("utf-8")
        response["logs"] = decoded_response.strip().replace("\n", "  ")
        #container.remove()
        if not is_status_expected(expected=expected_exit, response=response):
            sys.exit(response["StatusCode"])


def is_status_expected(*, expected: int, response: dict) -> bool:
    """Check to see if the status code was expected"""
    actual = response["StatusCode"]

    if expected != actual:
        LOG.error(
            "Received an unexpected status code from docker (%s); additional details: %s",
            response["StatusCode"],
            response["logs"],
        )
        return False

    return True


# Globals
CWD = Path(".").absolute()
VERSION = "0.1.0"
NAME = "hai"
WORKING_DIR = "/hai"

LOG_FORMAT = json.dumps(
    {
        "timestamp": "%(asctime)s",
        "namespace": "%(name)s",
        "loglevel": "%(levelname)s",
        "message": "%(message)s",
    }
)
basicConfig(level="INFO", format=LOG_FORMAT)
LOG = getLogger("seiso." + NAME)

# git
REPO = git.Repo(CWD)
COMMIT_HASH = REPO.head.object.hexsha

# Docker
CLIENT = docker.from_env()
IMAGE = "seiso/" + NAME
TAGS = [IMAGE + ":latest", IMAGE + ":" + VERSION]


# Tasks
@task
def run(c):  # pylint: disable=unused-argument
    """Say hai"""
    LOG.info("hai")
    opinionated_docker_run(image=IMAGE)


@task
def build(c):  # pylint: disable=unused-argument
    """Prepare to say hai"""
    buildargs = {"VERSION": VERSION, "COMMIT_HASH": COMMIT_HASH}

    for tag in TAGS:
        LOG.info("Building %s...", tag)
        CLIENT.images.build(path=str(CWD), rm=True, tag=tag, buildargs=buildargs)
