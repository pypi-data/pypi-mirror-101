import datetime
import discord
from discord.ext import commands
from typing import List, Optional, Union


def get_image_url(entity: Union[discord.User, discord.Guild, str]):
    """Returns an image url depending on if the desired entity is a User, Guild, or string

    Parameters
    ----------
    entity : Union(discord.User, discord.Guild, str)
        The entity to get the image from
    
    Returns
    -------
    The image url as a string, or the entity itself if its already a string
    """
    if isinstance(entity, (discord.User, discord.Guild, str)):
        if isinstance(entity, discord.User):
            return entity.avatar_url
        elif isinstance(entity, discord.Guild):
            return entity.icon_url
        return entity
    else:
        raise TypeError(f"Expected discord.User, discord.Guild, or string, got \"{entity.__class__.__name__}\" instead")


def truncate(string: str, max_length: int, end: Optional[str] = "...") -> str:
    """Truncates a string

    Parameters
    ----------
    string : str
        The string to truncate, if needed
    max_length : int
        The maximum length of the string before truncation is needed
    end : Optional str
        The string to append to the end of the string after truncation
        The string is automatically downsized to accommodate the size of `end`
        This automatically defaults to "..."
    
    Raises
    ------
    ValueError
        If the size of `end` is larger than `max_length`

    Returns
    -------
    The truncated string
    """

    if len(end) > max_length:
        raise ValueError(f"End string \"{end}\" of length {len(end)} can't be larger than {max_length} characters")
    
    truncated = string[:max_length]
    if string != truncated:
        truncated = string[:max_length - len(end)] + end

    return truncated


def chunkify_string(string: str, max_length: int) -> List[str]:
    """Returns a list of strings of a particular maximum length
    
    Original solution taken from https://stackoverflow.com/a/18854817

    Parameters
    ----------
    string : str
        The string to chunkify
    max_length : int
        The maximum length for each string chunk
    
    Returns
    -------
    A list of strings with maximum length of `max_length`
    """

    return [string[0+i:max_length+i] for i in range(0, len(string), max_length)]


def get_base_embed(
    title: Optional[str] = discord.Embed.Empty,
    description: Optional[str] = discord.Embed.Empty,
    color: Optional[discord.Color] = discord.Embed.Empty,
    timestamp: Optional[datetime.datetime] = datetime.datetime.utcnow(),
    author: Optional[Union[discord.User, discord.Guild]] = None,
    author_name: Optional[str] = None,
    author_icon: Optional[Union[discord.User, discord.Guild, str]] = discord.Embed.Empty,
    author_url: Optional[str] = discord.Embed.Empty,
    thumbnail: Optional[Union[discord.User, discord.Guild, str]] = None,
    image: Optional[Union[discord.User, discord.Guild, str]] = None,
    footer: Optional[Union[discord.User, discord.Guild]] = None,
    footer_text: Optional[str] = discord.Embed.Empty,
    footer_icon: Optional[Union[discord.User, discord.Guild, str]] = discord.Embed.Empty,
    url: Optional[str] = discord.Embed.Empty,
) -> discord.Embed:
    """Returns a "base" embed without any fields

    This function automatically truncates any excess characters for each field with "..."

    Parameters
    ----------
    title : Optional str
        The embed title
    description : Optional str
        The embed description
    color : Optional discord.Color
        The color to use for the embed
    timestamp : Optional datetime.datetime
        The utc timestamp to use for the embed (defaults to the current utc timestamp)
    author : Optional Union(discord.User, discord.Guild)
        The user or guild to use for the embed author name/icon. This overrides both `author_name` and `author_icon`
    author_name : Optional str
        The string to use for the embed author name
    author_icon: Optional str
        The url to use for the embed author icon
    author_url : Optional str
        The url to use for the embed author (for when the author name is clicked)
    thumbnail : Optional Union(discord.User, discord.Guild, str)
        The url of the image to use for the embed thumbail
    image : Optional Union(discord.User, discord.Guild, str)
        The url of the image to use for the embed image
    footer : Optional Union(discord.User, discord.Guild)
        The user or guild to use for the embed footer text/icon. This overrides both `footer_text` and `footer_icon`
    footer_text : Optional str
        The string to use for the footer text
    footer_icon : Optional str
        The url to use for the embed footer icon
    url : Optional str
        The url to use for the embed (for when the title is clicked)

    Raises
    ------
    ValueError
        - If the total embed character limit of 6000 characters is exceeded after attempting to truncate the embed title,
        description, footer text, and author_name
        - If all fields are empty
    """

    Empty = discord.Embed.Empty

    # check if all None
    if title is Empty and description is Empty and color is Empty and author is None and author_name is None and thumbnail is None and image is None and footer is None and footer_text is Empty and footer_icon is Empty and url is None:
        raise ValueError("Cannot construct an empty base embed")

    # set author icon
    if author_icon is not Empty:
        author_icon = get_image_url(author_icon)

    # override author attributes
    if author is not None:
        author_name = str(author)
        author_icon = author.avatar_url if isinstance(author, discord.User) else author.icon_url
    
    # set footer icon
    if footer_icon is not Empty:
        footer_icon = get_image_url(footer_icon)

    # override footer attributes
    if footer is not None:
        footer_text = str(footer)
        footer_icon = footer.avatar_url if isinstance(footer, discord.User) else author.icon_url

    # truncate neccesary fields
    MAX_TITLE_LENGTH = 256
    MAX_DESCRIPTION_LENGTH = 2048
    MAX_FOOTER_TEXT_LENGTH = 2048
    MAX_AUTHOR_NAME_LENGTH = 256
    MAX_TOTAL_LENGTH = 6000

    title = truncate(title, MAX_TITLE_LENGTH) if title is not discord.Embed.Empty else discord.Embed.Empty
    description = truncate(description, MAX_DESCRIPTION_LENGTH) if description is not discord.Embed.Empty else discord.Embed.Empty
    footer_text = truncate(footer_text, MAX_FOOTER_TEXT_LENGTH) if footer_text is not Empty else Empty
    author_name = truncate(author_name, MAX_AUTHOR_NAME_LENGTH) if author_name is not None else None

    # construct embed
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=timestamp,
        url=url,
    )

    # set embed author
    if author_name is not None:
        embed.set_author(
            name=author_name,
            icon_url=author_icon,
            url=author_url
        )
    
    # set embed footer
    if footer_text is not Empty and footer_icon is not Empty:
        embed.set_footer(
            text=footer_text,
            icon_url=footer_icon
        )
    
    # set embed thumbnail
    if thumbnail is not None:
        embed.set_thumbnail(get_image_url(thumbnail))
    
    # set embed image
    if image is not None:
        embed.set_image(get_image_url(image))
    
    # check max length
    if len(embed) > MAX_TOTAL_LENGTH:
        raise ValueError(f"Base embed character count of {len(embed)} is over limit of {MAX_TOTAL_LENGTH}")
    
    return embed