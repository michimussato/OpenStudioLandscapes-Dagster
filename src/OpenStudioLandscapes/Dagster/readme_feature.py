import textwrap
import snakemd


def readme_feature(doc: snakemd.Document) -> snakemd.Document:

    ## Some Specific information

    doc.add_heading(
        text="Dagster Documentation",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[https://release-1-9-13.archive.dagster-docs.io/]()",
        ]
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo Dagster
                """
            ),
            image={
                "Dagster": "https://dagster.io/images/brand/logos/dagster-primary-horizontal.png",
            }["Dagster"],
            link="https://dagster.io/platform",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Dagster is written and maintained by Dagster Labs.
            """
        )
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo Dagster
                """
            ),
            image={
                "Dagster": "https://dagster.io/images/brand/logos/dagster_labs-primary-horizontal.png",
            }["Dagster"],
            link="https://dagster.io",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Dagster is available in two flavors:
            """
        )
    )

    doc.add_ordered_list(
        [
            "[Dagster Community](https://dagster.io/community)",
            "[Dagster+](https://dagster.io/plus)",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            `OpenStudioLandscapes-Dagster` is based on the Community release.
            The Dagster version used in `OpenStudioLandscapes-Dagster` is locked to 
            version `1.9.11`.
            """
        )
    )

    return doc


if __name__ == "__main__":
    pass
