# -*- coding: utf-8 -*-

"""Extract registry information."""

from .resolve import (  # noqa
    get, get_banana, get_email, get_example, get_format, get_homepage, get_identifiers_org_prefix, get_name,
    get_pattern, get_pattern_re, get_version, get_versions, is_deprecated, namespace_in_lui, normalize_prefix,
    parse_curie,
)
from .resolve_identifier import (  # noqa
    get_identifiers_org_curie, get_identifiers_org_url, get_link, get_obofoundry_link, get_ols_link, get_providers,
    validate,
)
from .utils import read_bioregistry  # noqa
