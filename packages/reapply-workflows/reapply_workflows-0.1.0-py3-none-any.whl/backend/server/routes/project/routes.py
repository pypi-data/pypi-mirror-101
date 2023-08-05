import os
import shutil

import pandas as pd
from flask import Blueprint, jsonify, request

from backend.inference_core.reapply.data_structures.Provenance.graph import Graph
from backend.server.database.schemas.datasetRecord import DatasetRecord
from backend.server.database.schemas.project import Project
from backend.server.database.session import (
    dropAllTables,
    getDBSession,
    getEngine,
    getSessionScopeFromEngine,
    initializeDatabase,
)
from backend.server.paths import DATABASE_ROOT
from backend.server.routes.utils import handle_exception

projectRoute = Blueprint("project", __name__)


@projectRoute.route("/clearall", methods=["GET"])
def clearAll():
    shutil.rmtree(DATABASE_ROOT)
    os.mkdir(DATABASE_ROOT)
    print("Test")

    return "Done!"


@projectRoute.route("/project", methods=["GET"])
def getAllProjects():
    """List all projects endpoint
    -------
    get:
        description: Gets all the available projects
    """

    arr = list(
        filter(lambda x: x, map(lambda x: x.split(".")[0], os.listdir(DATABASE_ROOT)))
    )

    projects = []

    for proj in arr:
        session = getDBSession(proj)
        try:
            project = session.query(Project).one()
            projects.append(project.toJSON())
        except Exception as ex:
            return handle_exception(ex)
        finally:
            session.close()

    print(projects)
    return jsonify(projects)


@projectRoute.route("/project/<key>", methods=["POST"])
def createProject(key: str):
    if "reset" in request.form:
        dropAllTables(key)
    initializeDatabase(key)
    session = getDBSession(key)

    try:
        count = session.query(Project).count()

        if count > 0:
            raise Exception(422, "PROJECT_EXISTS", "Project already exists")

        if "name" not in request.form:
            raise Exception(400, "PROJECT_NAME_MISSING", "Please provide project name")

        name = request.form["name"]
        project = Project(key=key, name=name)
        session.add(project)
        session.commit()
        return jsonify({"message": "Project added successfully"})
    except Exception as ex:
        session.rollback()
        return handle_exception(ex)
    finally:
        session.close()


@projectRoute.route("/project/<project>/reapply", methods=["POST"])
def reapplyProvenance(project):
    targetKey = request.json["target"]

    provenance = request.json["provenance"]

    engine = getEngine(project)

    with engine.begin() as connection:
        with getSessionScopeFromEngine(connection) as session:
            targetDatasetRecord = (
                session.query(DatasetRecord)
                .filter(DatasetRecord.key == targetKey)
                .one()
            )

            allData = pd.read_sql("Dataset", con=connection)

            targetDataset = allData[allData["record_id"] == str(targetDatasetRecord.id)]
            targetDataset = targetDataset.drop("record_id", axis=1)

            graph = Graph(target=targetDataset, target_id=targetKey, **provenance)

            return jsonify(graph.apply())
