import argparse
import logging
import os
import sys
import tempfile

import flywheel

from .supporting_files import bidsify_flywheel, utils, templates
from .supporting_files.project_tree import get_project_tree

# TODO: log and logger should not both be used. Logging setup must be explicit.
logger = logging.getLogger("curate-bids")


def clear_meta_info(context, template):
    if "info" in context and template.namespace in context["info"]:
        del context["info"][template.namespace]


def format_validation_error(err):
    path = "/".join(err.path)
    if path:
        return path + " " + err.message
    return err.message


def validate_meta_info(container, template):
    """Validate meta information

    Adds 'BIDS.NA' if no BIDS info present
    Adds 'BIDS.valid' and 'BIDS.error_message'
        to communicate to user if values are valid (!!! minimal being checked)

    TODO: validation needs to check for more than non-empty strings; e.g., alphanumeric

    """
    # Get namespace
    namespace = template.namespace

    # If 'info' is NOT in container, then must not
    #   have matched to a template, create 'info'
    #  field with object {'BIDS': 'NA'}
    if "info" not in container:
        container["info"] = {namespace: "NA"}
    # if the namespace ('BIDS') is NOT in 'info',
    #   then must not have matched to a template,
    #   add  {'BIDS': 'NA'} to the meta info
    elif namespace not in container["info"]:
        container["info"][namespace] = "NA"
    # If already assigned BIDS 'NA', then break
    elif container["info"][namespace] == "NA":
        pass
    # Otherwise, iterate over keys within container
    else:
        valid = True
        error_message = ""

        # Find template
        templateName = container["info"][namespace].get("template")
        if templateName:
            templateDef = template.definitions.get(templateName)
            if templateDef:
                errors = template.validate(templateDef, container["info"][namespace])
                if errors:

                    for ee in errors:

                        log_message = (
                            f"{ee.schema.get('title','Invalid')}: {ee.message} for "
                        )
                        if len(ee.path) == 0:
                            log_message += f"{ee.schema.get('description', ee.instance.get('template'))}"
                        else:
                            log_message += f"BIDS value <{ee.path[0]}>"

                        logger.error(log_message)

                    valid = False
                    error_message = "\n".join(
                        [format_validation_error(err) for err in errors]
                    )
            else:
                valid = False
                error_message += "Unknown template: %s. " % templateName

        # Assign 'valid' and 'error_message' values
        container["info"][namespace]["valid"] = valid
        container["info"][namespace]["error_message"] = error_message


def update_meta_info(fw, context):
    """Update file information"""
    # Modify file
    if context["container_type"] == "file":
        # Modify acquisition file
        if context["parent_container_type"] == "acquisition":
            fw.set_acquisition_file_info(
                context["acquisition"]["id"],
                context["file"]["name"],
                context["file"]["info"],
            )
        # Modify project file
        elif context["parent_container_type"] == "project":
            fw.set_project_file_info(
                context["project"]["id"],
                context["file"]["name"],
                context["file"]["info"],
            )
        # Modify session file
        elif context["parent_container_type"] == "session":
            fw.set_session_file_info(
                context["session"]["id"],
                context["file"]["name"],
                context["file"]["info"],
            )
        else:
            logger.info(
                "Cannot determine file parent container type: "
                + context["parent_container_type"]
            )
    # Modify project
    elif context["container_type"] == "project":
        fw.replace_project_info(context["project"]["id"], context["project"]["info"])
    # Modify session
    elif context["container_type"] == "session":
        fw.replace_session_info(context["session"]["id"], context["session"]["info"])
    # Modify acquisition
    elif context["container_type"] == "acquisition":
        fw.replace_acquisition_info(
            context["acquisition"]["id"], context["acquisition"]["info"]
        )
    # Cannot determine container type
    else:
        logger.info("Cannot determine container type: " + context["container_type"])


def curate_bids_dir(
    fw,
    project_id,
    session_id=None,
    reset=False,
    session_only=False,
    template_type=None,
    template_file=None,
):
    """Curate BIDS directory.

    Args:
        fw (Flywheel Client): The Flywheel Client
        project_id (str): The Flywheel Project container ID.
        session_id (str): The Flywheel Session container ID.
        reset (bool): Whether to erase info.BIDS before curation.
        session_only (bool): Curate a Session (True) or the Project (False).
        template_type (str): Which template type to use. Options include:
                Default, BIDS-v1, ReproIn, or Custom.
        template_file (str): Provide a specific template file. Supercedes template_type.

    """
    project = get_project_tree(
        fw, project_id, session_id=session_id, session_only=session_only
    )

    curate_bids_tree(
        fw,
        project,
        reset=reset,
        template_type=template_type,
        template_file=template_file,
    )


def curate_bids_tree(fw, project, reset=False, template_type=None, template_file=None):
    """Curate BIDS tree.

    Args:
        fw (Flywheel Client): The Flywheel Client
        project (Flywheel Project): The Flywheel Project container.
        reset (bool): Whether to erase info.BIDS before curation.
        template_type (str): Which template type to use. Options include:
                Default, ReproIn, or Custom.
        template_file (str): Provide a specific template file. Supercedes template_type.

    TODO: Split this function into two.
    !!!: The template file is not stored; potential issue for reproducibility
    """
    container_counter = 0

    # If a template file is provided, this supercedes template type
    if template_file:
        template_type = None
        template = templates.loadTemplate(template_file)

    # If neither a template file nor a template type are indicated, the the Default template is selected
    if not template_file and not template_type:
        template_type = "Default"

    if template_type:

        if template_type == "Default":
            logger.info(
                "Using project curation template: Flywheel Default: "
                "https://gitlab.com/flywheel-io/public/bids-client/-/blob/master/flywheel_bids/templates/default.json"
            )
            template = templates.DEFAULT_TEMPLATE

        elif template_type == "BIDS-v1":
            logger.info(
                "Using project curation template: Flywheel BIDS-v1: "
                "https://gitlab.com/flywheel-io/public/bids-client/-/blob/master/flywheel_bids/templates/bids-v1.json"
            )
            template = templates.BIDS_V1_TEMPLATE

        elif template_type == "ReproIn":
            logger.info(
                "Using project curation template: Flywheel ReproIn: "
                "https://gitlab.com/flywheel-io/public/bids-client/-/blob/master/flywheel_bids/templates/reproin.json"
            )
            template = templates.REPROIN_TEMPLATE

        elif template_type == "Custom":
            logger.info("Using project curation template: Custom")

            # Capture project-level files
            project_files = project.get("files", [])
            template_filename = utils.find_custom_template(project_files)

            if template_filename:

                # Download template file
                fd, template_file = tempfile.mkstemp(".json")
                os.close(fd)
                fw.download_file_from_project(
                    project["id"], template_filename, template_file
                )

                logger.info(f"Using Project Curation Template: {template_filename}")

                template = templates.loadTemplate(template_file)

            else:
                logger.error(
                    (
                        "Unable to find a BIDS Project Curation JSON "
                        "Template as a project-level file. Using a Custom "
                        "BIDS Project Curation JSON Template requires a "
                        "project-level file ending in "
                        "<project-template.json>. Exiting."
                    )
                )
                # TODO: Create custom error for exit
                os.sys.exit(1)

        else:
            logger.info("Unable to determine Project Curation Template file. Exiting.")
            # TODO: Create custom error for exit
            os.sys.exit(1)

    # Curation begins: match, resolve, update

    # Match: do initial template matching and updating
    for context in project.context_iter():

        ctype = context["container_type"]
        parent_ctype = context["parent_container_type"]

        # Cleanup, if indicated
        if reset:
            clear_meta_info(context[ctype], template)

        elif context[ctype].get("info", {}).get("BIDS") == "NA":
            continue

        # BIDSIFY
        if ctype in ["project", "session", "acquisition"]:
            logger.info(
                f"\n\n===================================================================================\n"
                f"{container_counter}: Bidsifying Container: <{ctype}> <{context.get(ctype).get('label')}>"
                f"\n===================================================================================\n"
            )

            container_counter += 1

            bidsify_flywheel.process_matching_templates(context, template)

            # Add run counter for session
            if ctype == "session":
                logger.debug(
                    f"adding run counter for session {context.get(ctype).get('label')}"
                )
                context["run_counters"] = utils.RunCounterMap()

        elif ctype == "file":

            logger.info(
                f"\n\n"
                f"Bidsifying file: <{ctype}> <{context.get(ctype).get('name')}>"
                f"\n------------------------------------------------------------------"
            )

            # Don't BIDSIFY the project template (?)
            if (
                parent_ctype == "project"
                and utils.PROJECT_TEMPLATE_FILE_NAME_REGEX.search(
                    context["file"]["name"]
                )
            ):
                logger.debug(
                    f"Skipping Project Curation Template {context.get(ctype).get('name')}"
                )
                continue

            # Process matching
            context["file"] = bidsify_flywheel.process_matching_templates(
                context, template
            )

            # Validate meta information
            validate_meta_info(context["file"], template)

    # Resolve: perform path resolutions, if needed (?)
    for context in project.context_iter():
        bidsify_flywheel.process_resolvers(context, template)

    # Update: send updates to Flywheel, if the Flywheel Client is instantiated
    if fw:
        for context in project.context_iter():
            ctype = context["container_type"]
            node = context[ctype]
            if node.is_dirty():
                update_meta_info(fw, context)


def configure_logging(verbosity):
    my_logs = ["curate-bids"]

    # TODO: loggers is never used. Broken function.

    loggers = [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name in my_logs
    ]

    if verbosity == 0:
        print('setting log level to "info"')
        logging.basicConfig(
            format="[ %(module)s %(asctime)2s %(levelname)2s] %(message)s"
        )
        log = logging.getLogger("curate-bids")
        log.setLevel(logging.INFO)

    elif verbosity == 1:
        print('setting log level to "debug"')
        logging.basicConfig(
            format="[ %(module)s %(asctime)2s %(levelname)2s: %(lineno)s] %(message)s"
        )
        log = logging.getLogger("curate-bids")
        log.setLevel(logging.DEBUG)


def main_with_args(
    api_key, session_id, reset, session_only, template_type, verbosity=1
):
    """Run BIDS Curation, called by curate-bids Gear."""
    fw = flywheel.Client(api_key)

    configure_logging(verbosity)

    if session_id:
        project_id = utils.get_project_id_from_session_id(fw, session_id)
    else:
        logger.error("Session ID is required. Exiting")
        sys.exit(1)

    # Curate BIDS
    curate_bids_dir(
        fw,
        project_id,
        session_id=session_id,
        reset=reset,
        session_only=session_only,
        template_type=template_type,
    )


def main():

    parser = argparse.ArgumentParser(description="BIDS Curation")
    parser.add_argument(
        "--api-key", dest="api_key", action="store", required=True, help="API key"
    )
    parser.add_argument(
        "-p",
        dest="project_label",
        action="store",
        required=False,
        default=None,
        help="A Flywheel instance Project label.",
    )
    parser.add_argument(
        "--session",
        dest="session_id",
        action="store",
        required=False,
        default=None,
        help="A Flywheel instance Session ID; alternative to determine Project label.",
    )
    parser.add_argument(
        "--reset",
        dest="reset",
        action="store_true",
        default=False,
        help="Hard reset of BIDS metadata before running.",
    )
    parser.add_argument(
        "--session-only",
        dest="session_only",
        action="store_true",
        default=False,
        help="Only curate the session identified by the --session flag.",
    )
    parser.add_argument(
        "--template-type",
        dest="template_type",
        action="store",
        required=False,
        default=None,
        help=" Which template type to use. Options include: Default, ReproIn, or Custom.",
    )
    parser.add_argument(
        "--template-file",
        dest="template_file",
        action="store",
        default=None,
        help="Template file to use. Supersedes the --template-type flag.",
    )
    parser.add_argument(
        "--verbosity",
        dest="verbosity",
        action="store",
        default=1,
        help="Verbosity of output logs. 0 (Least Verbose) to 3 (Most Verbose).",
    )

    args = parser.parse_args()

    configure_logging(int(args.verbosity))

    # Prep
    # Check API key - raises Error if key is invalid
    fw = flywheel.Client(args.api_key)
    # Get project id from label
    if args.project_label:
        project_id = utils.validate_project_label(fw, args.project_label)
    elif args.session_id:
        project_id = utils.get_project_id_from_session_id(fw, args.session_id)
    else:
        logger.error("Either project label or session id is required!")
        sys.exit(1)

    # Curate BIDS project
    curate_bids_dir(
        fw,
        project_id,
        args.session_id,
        reset=args.reset,
        session_only=args.session_only,
        template_type=args.template_type,
        template_file=args.template_file,
    )


if __name__ == "__main__":
    main()
