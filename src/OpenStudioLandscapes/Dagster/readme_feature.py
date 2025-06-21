import textwrap
import snakemd


def readme_feature(doc: snakemd.Document) -> snakemd.Document:

    ## Some Specific information

    doc.add_heading(
        text="Official Resources",
        level=1,
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
                "Dagster": "https://dagster-website.vercel.app/images/brand/logos/dagster-primary-horizontal.png",
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
                Logo Dagster Labs
                """
            ),
            image={
                "Dagster": "https://docs.dagster.io/img/dagster_labs-primary-horizontal.svg",
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
            Dagster is evolving at a very fast pace and it can be hard to keep up. 
            Therefore, for now, the Dagster version used in `OpenStudioLandscapes-Dagster` 
            is locked to [version 1.9.11](https://pypi.org/project/dagster/1.9.11/). 
            When consulting the official [Dagster Documentation](https://docs.dagster.io), 
            make sure you consult the matching [version](#official-documentation-version-19).
            """
        )
    )

    doc.add_heading(
        text="Official Documentation (Version 1.9)",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[https://release-1-9-13.archive.dagster-docs.io](https://release-1-9-13.archive.dagster-docs.io)",
        ]
    )

    doc.add_heading(
        text="Getting Started with Dagster",
        level=2,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Dagsters primary learning resource is called 
            [Dagster University](https://courses.dagster.io).
            It is a fantastic learning path and you should check it out
            if you plan to use Dagster as you automation platform (a 
            personal recommendation by the `OpenStudioLandscapes-Dagster`
            maintainer). The course 
            [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials) 
            will give you a basic but deep enough understanding of how Dagster works. 
            """
        )
    )

    doc.add_heading(
        text="Resources",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[All Resources](https://dagster.io/resources)",
            "[GitHub](https://github.com/dagster-io/dagster)",
            "[Issue Tracker](https://github.com/dagster-io/dagster/issues)",
            "[PyPi](https://pypi.org/project/dagster)",
            "[Slack](https://app.slack.com/client/TCDGQDUKF)",
        ]
    )

    return doc


if __name__ == "__main__":
    pass
