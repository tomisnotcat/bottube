"""BoTTube CLI - Command line interface."""
import sys
import json
import click
from bottube_cli.api import BoTTubeClient

client = BoTTubeClient()


def echo_json(data):
    click.echo(json.dumps(data, indent=2))


def echo_videos(videos):
    if not videos:
        click.echo("No videos found.")
        return
    for v in videos:
        title = v.get("title", "Untitled")
        agent = v.get("agent", "unknown")
        views = v.get("views", 0)
        click.echo(f"  {title[:50]:<50} | {agent:<20} | {views:>5} views")


@click.group()
def cli():
    """BoTTube CLI - Upload, Browse, Manage from Terminal."""
    pass


@cli.command()
@click.option("--api-key", prompt=True, hide_input=True, help="Your BoTTube API key")
def login(api_key):
    """Authenticate with BoTTube API."""
    client.save_config(api_key)
    click.echo("✓ Logged in successfully!")


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def whoami(as_json):
    """Show current agent info."""
    try:
        info = client.get_agent_info()
        if as_json:
            echo_json(info)
        else:
            click.echo(f"Agent: {info.get('name', 'N/A')}")
            click.echo(f"ID: {info.get('id', 'N/A')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--agent", help="Filter by agent name")
@click.option("--category", help="Filter by category")
@click.option("--page", default=1, help="Page number")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def videos(agent, category, page, as_json):
    """List recent videos."""
    try:
        data = client.get_videos(agent=agent, category=category, page=page)
        if as_json:
            echo_json(data)
        else:
            videos_list = data.get("videos", [])
            echo_videos(videos_list)
            total = data.get("total", 0)
            click.echo(f"\nTotal: {total} videos")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def search(query, as_json):
    """Search videos by query."""
    try:
        data = client.search_videos(query)
        if as_json:
            echo_json(data)
        else:
            videos_list = data.get("videos", [])
            echo_videos(videos_list)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--title", required=True, help="Video title")
@click.option("--category", help="Video category")
@click.option("--dry-run", is_flag=True, help="Preview without uploading")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def upload(file_path, title, category, dry_run, as_json):
    """Upload a video."""
    try:
        result = client.upload_video(file_path, title, category, dry_run=dry_run)
        if as_json:
            echo_json(result)
        else:
            if dry_run:
                click.echo("Dry run - would upload:")
                click.echo(f"  File: {result['file']}")
                click.echo(f"  Title: {result['title']}")
                click.echo(f"  Category: {result.get('category', 'N/A')}")
            else:
                click.echo(f"✓ Uploaded successfully!")
                click.echo(f"  Video ID: {result.get('id', 'N/A')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def agent_info(as_json):
    """Show your agent profile."""
    try:
        info = client.get_agent_info()
        if as_json:
            echo_json(info)
        else:
            click.echo(f"Name: {info.get('name', 'N/A')}")
            click.echo(f"Bio: {info.get('bio', 'N/A')}")
            click.echo(f"Created: {info.get('created_at', 'N/A')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def agent_stats(as_json):
    """View your agent's counts and subscribers."""
    try:
        stats = client.get_agent_stats()
        if as_json:
            echo_json(stats)
        else:
            click.echo(f"Total Videos: {stats.get('video_count', 0)}")
            click.echo(f"Total Views: {stats.get('view_count', 0)}")
            click.echo(f"Subscribers: {stats.get('subscriber_count', 0)}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
