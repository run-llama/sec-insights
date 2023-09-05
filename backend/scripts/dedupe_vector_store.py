import asyncio
from fire import Fire
from sqlalchemy import text
from app.db.session import SessionLocal


async def _async_dedupe_vectore_store(dry_run: bool = False):
    async with SessionLocal() as db:
        try:
            common_table_expression = """
                WITH cte AS (
                    SELECT 
                        max(id) as max_id,
                        text, 
                        (metadata_ ->> 'page_label'):: text as page_label, 
                        (metadata_ ->> 'db_document_id'):: text as db_document_id
                    FROM 
                        data_pg_vector_store 
                    GROUP BY 
                        text, 
                        page_label, 
                        db_document_id
                )
            """
            # Count rows that would be deleted
            stmt = text(
                f"""
                {common_table_expression}
                SELECT COUNT(id) FROM data_pg_vector_store WHERE id NOT IN (SELECT max_id FROM cte);
                """
            )
            result = await db.execute(stmt)
            num_duplicate_rows = result.scalar()

            num_rows = (
                await db.execute(text("SELECT COUNT(*) FROM data_pg_vector_store"))
            ).scalar()

            print(f"{num_duplicate_rows} duplicate rows found out of {num_rows} total.")
            print(
                f"{num_rows - num_duplicate_rows} rows would be remaining if deleted."
            )
            if dry_run or num_duplicate_rows == 0:
                return

            # Ask for confirmation before deleting rows
            confirmation = input("Do you want to delete these rows? (y/n) ")
            if confirmation.lower() != "y":
                print("Aborted.")
                return

            # Delete the rows
            delete_stmt = text(
                f"""
                {common_table_expression}
                DELETE FROM data_pg_vector_store WHERE id NOT IN (SELECT max_id FROM cte);
                """
            )
            await db.execute(delete_stmt)
            await db.commit()  # Explicitly commit the transaction
            print(f"{num_duplicate_rows} rows have been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")


def dedupe_vectore_store(dry_run: bool = False):
    """
    Deduplicate the vector store.

    :param dry_run: If True, do not commit changes to the database.
    """
    asyncio.run(_async_dedupe_vectore_store(dry_run=dry_run))


if __name__ == "__main__":
    Fire(dedupe_vectore_store)
