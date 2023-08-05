from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


@dataclass
class Actor:
    class Meta:
        name = "actor"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Adapter:
    class Meta:
        name = "adapter"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Aspect:
    class Meta:
        name = "aspect"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Audio:
    class Meta:
        name = "audio"

    present: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    stereo: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Category:
    class Meta:
        name = "category"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Colour:
    class Meta:
        name = "colour"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Commentator:
    class Meta:
        name = "commentator"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Composer:
    class Meta:
        name = "composer"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Country:
    class Meta:
        name = "country"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Date:
    class Meta:
        name = "date"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Desc:
    class Meta:
        name = "desc"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Director:
    class Meta:
        name = "director"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class DisplayName:
    class Meta:
        name = "display-name"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Editor:
    class Meta:
        name = "editor"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class EpisodeNum:
    class Meta:
        name = "episode-num"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    system: str = field(
        default="onscreen",
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Guest:
    class Meta:
        name = "guest"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Icon:
    class Meta:
        name = "icon"

    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    width: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    height: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Keyword:
    class Meta:
        name = "keyword"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Language:
    class Meta:
        name = "language"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class LastChance:
    class Meta:
        name = "last-chance"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class LengthUnits(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"


@dataclass
class New:
    class Meta:
        name = "new"


@dataclass
class OrigLanguage:
    class Meta:
        name = "orig-language"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Premiere:
    class Meta:
        name = "premiere"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Present:
    class Meta:
        name = "present"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Presenter:
    class Meta:
        name = "presenter"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class PreviouslyShown:
    class Meta:
        name = "previously-shown"

    start: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Producer:
    class Meta:
        name = "producer"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Quality:
    class Meta:
        name = "quality"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


class ReviewType(Enum):
    TEXT = "text"
    URL = "url"


@dataclass
class Stereo:
    class Meta:
        name = "stereo"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class SubTitle:
    class Meta:
        name = "sub-title"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class SubtitlesType(Enum):
    TELETEXT = "teletext"
    ONSCREEN = "onscreen"
    DEAF_SIGNED = "deaf-signed"


@dataclass
class Title:
    class Meta:
        name = "title"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Url:
    class Meta:
        name = "url"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Value:
    class Meta:
        name = "value"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Video:
    class Meta:
        name = "video"

    present: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    colour: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    aspect: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    quality: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Writer:
    class Meta:
        name = "writer"

    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )


@dataclass
class Channel:
    class Meta:
        name = "channel"

    display_name: List[DisplayName] = field(
        default_factory=list,
        metadata={
            "name": "display-name",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    icon: List[Icon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    url: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Credits:
    class Meta:
        name = "credits"

    director: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    actor: List[Actor] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    writer: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    adapter: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    producer: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    composer: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    editor: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    presenter: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    commentator: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    guest: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Length:
    class Meta:
        name = "length"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    units: Optional[LengthUnits] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Rating:
    class Meta:
        name = "rating"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    icon: List[Icon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    system: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Review:
    class Meta:
        name = "review"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    type: Optional[ReviewType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    source: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    reviewer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class StarRating:
    class Meta:
        name = "star-rating"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    icon: List[Icon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    system: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Subtitles:
    class Meta:
        name = "subtitles"

    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[SubtitlesType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Programme:
    class Meta:
        name = "programme"

    title: List[Title] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    sub_title: List[SubTitle] = field(
        default_factory=list,
        metadata={
            "name": "sub-title",
            "type": "Element",
        }
    )
    desc: List[Desc] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    credits: Optional[Credits] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    category: List[Category] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    keyword: List[Keyword] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    language: Optional[Language] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    orig_language: Optional[OrigLanguage] = field(
        default=None,
        metadata={
            "name": "orig-language",
            "type": "Element",
        }
    )
    length: Optional[Length] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    icon: List[Icon] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    url: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    country: List[Country] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    episode_num: List[EpisodeNum] = field(
        default_factory=list,
        metadata={
            "name": "episode-num",
            "type": "Element",
        }
    )
    video: Optional[Video] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    previously_shown: Optional[PreviouslyShown] = field(
        default=None,
        metadata={
            "name": "previously-shown",
            "type": "Element",
        }
    )
    premiere: Optional[Premiere] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    last_chance: Optional[LastChance] = field(
        default=None,
        metadata={
            "name": "last-chance",
            "type": "Element",
        }
    )
    new: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    subtitles: List[Subtitles] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    rating: List[Rating] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    star_rating: List[StarRating] = field(
        default_factory=list,
        metadata={
            "name": "star-rating",
            "type": "Element",
        }
    )
    review: List[Review] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    start: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    stop: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    pdc_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "pdc-start",
            "type": "Attribute",
        }
    )
    vps_start: Optional[str] = field(
        default=None,
        metadata={
            "name": "vps-start",
            "type": "Attribute",
        }
    )
    showview: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    videoplus: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    channel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    clumpidx: str = field(
        default="0/1",
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Tv:
    class Meta:
        name = "tv"

    channel: List[Channel] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    programme: List[Programme] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    source_info_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-info-url",
            "type": "Attribute",
        }
    )
    source_info_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-info-name",
            "type": "Attribute",
        }
    )
    source_data_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "source-data-url",
            "type": "Attribute",
        }
    )
    generator_info_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "generator-info-name",
            "type": "Attribute",
        }
    )
    generator_info_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "generator-info-url",
            "type": "Attribute",
        }
    )
