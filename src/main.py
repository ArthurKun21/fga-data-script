import asyncio

import click
from anyio import run
from loguru import logger

import directory
from data import process_craft_essence_data, process_servant_data
from log import setup_logger
from preprocess import (
    fetch_local_ce_data,
    fetch_local_servant_data,
    process_craft_essence,
    process_servant,
)


async def main(debug: bool, dry_run: bool, delete: bool):
    """
    Main function to run the application.
    """
    logger.info("Starting the application...")
    if debug:
        logger.debug("Debug mode is enabled.")

    try:
        await directory.check_if_repo_exists()
    except directory.RepositoryNotFoundError:
        logger.error("Repository not found. Exiting...")
        exit()

    if delete:
        logger.info("Deleting the repository support files...")
        await directory.delete_repository_support()

    try:
        (
            ce_latest_data,
            ce_local_data,
            servant_latest_data,
            servant_local_data,
        ) = await asyncio.gather(
            process_craft_essence(),
            fetch_local_ce_data(),
            process_servant(),
            fetch_local_servant_data(),
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    try:
        await asyncio.gather(
            process_servant_data(
                servant_latest_data,
                servant_local_data,
                debug,
                dry_run,
            ),
            process_craft_essence_data(
                ce_latest_data,
                ce_local_data,
                debug,
                dry_run,
            ),
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit()

    await directory.copy_output_to_repo()

    await directory.remove_duplicate_txt_names()


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode.")
@click.option("--dry_run", is_flag=True, help="Enable dry run mode.")
@click.option("--delete", is_flag=True, help="Delete the repository files.")
def app(debug: bool, dry_run: bool, delete: bool):
    setup_logger(debug=debug)

    run(main, debug, dry_run, delete)


if __name__ == "__main__":
    app()
