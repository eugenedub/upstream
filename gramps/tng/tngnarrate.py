# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2009       Brian G. Matherly
# Copyright (C) 2010       Jakim Friant
# Copyright (C) 2011       Vlada Perić <vlada.peric@gmail.com>
# Copyright (C) 2011       Matt Keenan <matt.keenan@gmail.com>
# Copyright (C) 2011       Tim G L Lyons
# Copyright (C) 2013-2014  Paul Franklin
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

"""
Narrator class for use by plugins.
"""

# ------------------------------------------------------------------------
#
# Gramps modules
#
# ------------------------------------------------------------------------
from gramps.gen.lib.date import Date
from gramps.gen.lib.person import Person
from gramps.gen.lib.eventroletype import EventRoleType
from gramps.gen.lib.eventtype import EventType
from gramps.gen.lib.familyreltype import FamilyRelType
from gramps.gen.display.name import displayer as _nd
from gramps.gen.display.place import displayer as _pd
from gramps.gen.utils.alive import probably_alive
from gramps.gen.plug.report import utils
from gramps.gen.const import GRAMPS_LOCALE as glocale

# -------------------------------------------------------------------------
#
# Private constants
#
# -------------------------------------------------------------------------
# In string arrays, the first strings should include the name, the second
# strings should not include the name.
_NAME_INDEX_INCLUDE_NAME = 0
_NAME_INDEX_EXCLUDE_NAME = 1

# In string arrays, the first strings should not include age.
# The following strings should include year, month and day units.
# And support format with precision (see gen/lib/date.py).
_AGE_INDEX_NO_AGE = 0
_AGE_INDEX = 1


# -------------------------------------------------------------------------
#
# Private functions
#
# -------------------------------------------------------------------------
def _get_empty_endnote_numbers(obj):
    """
    Empty stab function for when endnotes are not needed
    """
    return ""


def convert_prefix(word):
    """
    Convert Hebrew grammar for prefixes
    """
    if not word or len(word) < 2:
        return word
    if word[0] == "ו" and word[1] != "ו":
        # Double the Vav if not already double
        word = "ו" + word
    if word[0] == "ה":
        # Remove the leading He
        word = word[1:]
    if word[0] < "א" or word[0] > "ת":
        # Prefix a maqaf for non-Hebrew words and numbers
        word = "־" + word
    return word


# avoid normal translation!
# enable deferred translations
# (these days this is done elsewhere as _T_ but it was done here first)
##from gramps.gen.const import GRAMPS_LOCALE as glocale
##_ = glocale.translation.gettext
def _(message):
    return message


# ------------------------------------------------------------------------
#
# Born strings
#
# ------------------------------------------------------------------------
born_full_date_with_place = [
    {
        Person.UNKNOWN: _(
            "%(unknown_gender_name)s was born on %(birth_date)s in %(birth_place)s."
        ),
        Person.MALE: _("%(male_name)s was born on %(birth_date)s in %(birth_place)s."),
        Person.FEMALE: _(
            "%(female_name)s was born on %(birth_date)s in %(birth_place)s."
        ),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born on %(birth_date)s in %(birth_place)s."),
        Person.MALE: _("Hij was born on %(birth_date)s in %(birth_place)s."),
        Person.FEMALE: _("Zij was born on %(birth_date)s in %(birth_place)s."),
    },
    _("Born %(birth_date)s in %(birth_place)s."),
]

born_modified_date_with_place = [
    {
        Person.UNKNOWN: _(
            "%(unknown_gender_name)s was born %(modified_date)s in %(birth_place)s."
        ),
        Person.MALE: _("%(male_name)s was born %(modified_date)s in %(birth_place)s."),
        Person.FEMALE: _(
            "%(female_name)s was born %(modified_date)s in %(birth_place)s."
        ),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born %(modified_date)s in %(birth_place)s."),
        Person.MALE: _("Hij was born %(modified_date)s in %(birth_place)s."),
        Person.FEMALE: _("Zij was born %(modified_date)s in %(birth_place)s."),
    },
    _("Born %(modified_date)s in %(birth_place)s."),
]

born_full_date_no_place = [
    {
        Person.UNKNOWN: _("%(unknown_gender_name)s was born on %(birth_date)s."),
        Person.MALE: _("%(male_name)s was born on %(birth_date)s."),
        Person.FEMALE: _("%(female_name)s was born on %(birth_date)s."),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born on %(birth_date)s."),
        Person.MALE: _("Hij was born on %(birth_date)s."),
        Person.FEMALE: _("Zij was born on %(birth_date)s."),
    },
    _("Born %(birth_date)s."),
]

born_modified_date_no_place = [
    {
        Person.UNKNOWN: _("%(unknown_gender_name)s was born %(modified_date)s."),
        Person.MALE: _("%(male_name)s was born %(modified_date)s."),
        Person.FEMALE: _("%(female_name)s was born %(modified_date)s."),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born %(modified_date)s."),
        Person.MALE: _("Hij was born %(modified_date)s."),
        Person.FEMALE: _("Zij was born %(modified_date)s."),
    },
    _("Born %(modified_date)s."),
]

born_partial_date_with_place = [
    {
        Person.UNKNOWN: _(
            "%(unknown_gender_name)s was born in %(month_year)s in %(birth_place)s."
        ),
        Person.MALE: _("%(male_name)s was born in %(month_year)s in %(birth_place)s."),
        Person.FEMALE: _(
            "%(female_name)s was born in %(month_year)s in %(birth_place)s."
        ),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born in %(month_year)s in %(birth_place)s."),
        Person.MALE: _("Hij was born in %(month_year)s in %(birth_place)s."),
        Person.FEMALE: _("Zij was born in %(month_year)s in %(birth_place)s."),
    },
    _("Born %(month_year)s in %(birth_place)s."),
]

born_partial_date_no_place = [
    {
        Person.UNKNOWN: _("%(unknown_gender_name)s was born in %(month_year)s."),
        Person.MALE: _("%(male_name)s was born in %(month_year)s."),
        Person.FEMALE: _("%(female_name)s was born in %(month_year)s."),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born in %(month_year)s."),
        Person.MALE: _("Hij was born in %(month_year)s."),
        Person.FEMALE: _("Zij was born in %(month_year)s."),
    },
    _("Born %(month_year)s."),
]

born_no_date_with_place = [
    {
        Person.UNKNOWN: _("%(unknown_gender_name)s was born in %(birth_place)s."),
        Person.MALE: _("%(male_name)s was born in %(birth_place)s."),
        Person.FEMALE: _("%(female_name)s was born in %(birth_place)s."),
    },
    {
        Person.UNKNOWN: _("Deze persoon was born in %(birth_place)s."),
        Person.MALE: _("Hij was born in %(birth_place)s."),
        Person.FEMALE: _("Zij was born in %(birth_place)s."),
    },
    _("Born in %(birth_place)s."),
]

# ------------------------------------------------------------------------
#
# Died strings
#
# ------------------------------------------------------------------------
died_full_date_with_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed op %(death_date)s te %(death_place)s."),
            _(
                "%(unknown_gender_name)s overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("%(male_name)s overleed op %(death_date)s te %(death_place)s."),
            _(
                "%(male_name)s overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed op %(death_date)s te %(death_place)s."),
            _(
                "%(female_name)s overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed op %(death_date)s te %(death_place)s."),
            _(
                "Deze persoon overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("Hij overleed op %(death_date)s te %(death_place)s."),
            _("Hij overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed op %(death_date)s te %(death_place)s."),
            _("Zij overleed op %(death_date)s te %(death_place)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(death_date)s te %(death_place)s."),
        _("Overleed %(death_date)s te %(death_place)s (%(age)s)."),
    ],
]

died_modified_date_with_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed %(death_date)s te %(death_place)s."),
            _(
                "%(unknown_gender_name)s overleed %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("%(male_name)s overleed %(death_date)s te %(death_place)s."),
            _(
                "%(male_name)s overleed %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed %(death_date)s te %(death_place)s."),
            _(
                "%(female_name)s overleed %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed %(death_date)s te %(death_place)s."),
            _(
                "Deze persoon overleed %(death_date)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("Hij overleed %(death_date)s te %(death_place)s."),
            _("Hij overleed %(death_date)s te %(death_place)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed %(death_date)s te %(death_place)s."),
            _("Zij overleed %(death_date)s te %(death_place)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(death_date)s te %(death_place)s."),
        _("Overleed %(death_date)s te %(death_place)s (%(age)s)."),
    ],
]

died_full_date_no_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed op %(death_date)s."),
            _("%(unknown_gender_name)s overleed op %(death_date)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("%(male_name)s overleed op %(death_date)s."),
            _("%(male_name)s overleed op %(death_date)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed op %(death_date)s."),
            _("%(female_name)s overleed op %(death_date)s %(age)s jaar oud."),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed op %(death_date)s."),
            _("Deze persoon overleed op %(death_date)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("Hij overleed op %(death_date)s."),
            _("Hij overleed op %(death_date)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed op %(death_date)s."),
            _("Zij overleed op %(death_date)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(death_date)s."),
        _("Overleed %(death_date)s (%(age)s)."),
    ],
]

died_modified_date_no_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed %(death_date)s."),
            _("%(unknown_gender_name)s overleed %(death_date)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("%(male_name)s overleed %(death_date)s."),
            _("%(male_name)s overleed %(death_date)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed %(death_date)s."),
            _("%(female_name)s overleed %(death_date)s %(age)s jaar oud."),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed %(death_date)s."),
            _("Deze persoon overleed %(death_date)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("Hij overleed %(death_date)s."),
            _("Hij overleed %(death_date)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed %(death_date)s."),
            _("Zij overleed %(death_date)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(death_date)s."),
        _("Overleed %(death_date)s (%(age)s)."),
    ],
]

died_partial_date_with_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed in %(month_year)s te %(death_place)s."),
            _(
                "%(unknown_gender_name)s overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("%(male_name)s overleed in %(month_year)s te %(death_place)s."),
            _(
                "%(male_name)s overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed in %(month_year)s te %(death_place)s."),
            _(
                "%(female_name)s overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed in %(month_year)s te %(death_place)s."),
            _(
                "Deze persoon overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."
            ),
        ],
        Person.MALE: [
            _("Hij overleed in %(month_year)s te %(death_place)s."),
            _("Hij overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed in %(month_year)s te %(death_place)s."),
            _("Zij overleed in %(month_year)s te %(death_place)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(month_year)s te %(death_place)s."),
        _("Overleed %(month_year)s te %(death_place)s (%(age)s)."),
    ],
]

died_partial_date_no_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed in %(month_year)s."),
            _("%(unknown_gender_name)s overleed in %(month_year)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("%(male_name)s overleed in %(month_year)s."),
            _("%(male_name)s overleed in %(month_year)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed in %(month_year)s."),
            _("%(female_name)s overleed in %(month_year)s %(age)s jaar oud."),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed in %(month_year)s."),
            _("Deze persoon overleed in %(month_year)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("Hij overleed in %(month_year)s."),
            _("Hij overleed in %(month_year)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed in %(month_year)s."),
            _("Zij overleed in %(month_year)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed %(month_year)s."),
        _("Overleed %(month_year)s (%(age)s)."),
    ],
]

died_no_date_with_place = [
    {
        Person.UNKNOWN: [
            _("%(unknown_gender_name)s overleed te %(death_place)s."),
            _("%(unknown_gender_name)s overleed te %(death_place)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("%(male_name)s overleed te %(death_place)s."),
            _("%(male_name)s overleed te %(death_place)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("%(female_name)s overleed te %(death_place)s."),
            _("%(female_name)s overleed te %(death_place)s %(age)s jaar oud."),
        ],
    },
    {
        Person.UNKNOWN: [
            _("Deze persoon overleed te %(death_place)s."),
            _("Deze persoon overleed te %(death_place)s %(age)s jaar oud."),
        ],
        Person.MALE: [
            _("Hij overleed te %(death_place)s."),
            _("Hij overleed te %(death_place)s %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            _("Zij overleed te %(death_place)s."),
            _("Zij overleed te %(death_place)s %(age)s jaar oud."),
        ],
    },
    [
        _("Overleed te %(death_place)s."),
        _("Overleed te %(death_place)s (%(age)s)."),
    ],
]

died_no_date_no_place = [
    {
        Person.UNKNOWN: [
            "",
            _("%(unknown_gender_name)s overleed %(age)s jaar oud."),
        ],
        Person.MALE: [
            "",
            _("%(male_name)s overleed %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            "",
            _("%(female_name)s overleed %(age)s jaar oud."),
        ],
    },
    {
        Person.UNKNOWN: [
            "",
            _("Deze persoon overleed %(age)s jaar oud."),
        ],
        Person.MALE: [
            "",
            _("Hij overleed %(age)s jaar oud."),
        ],
        Person.FEMALE: [
            "",
            _("Zij overleed %(age)s jaar oud."),
        ],
    },
    [
        "",
        _("Overleed (%(age)s)."),
    ],
]

# ------------------------------------------------------------------------
#
# Buried strings
#
# ------------------------------------------------------------------------
buried_full_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Hij werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Zij werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Deze persoon werd begraven op %(burial_date)s te %(burial_place)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(burial_date)s te %(burial_place)s%(endnotes)s."),
}

buried_full_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd begraven op %(burial_date)s%(endnotes)s."),
        _("Hij werd begraven op %(burial_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd begraven op %(burial_date)s%(endnotes)s."),
        _("Zij werd begraven op %(burial_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd begraven op %(burial_date)s%(endnotes)s."),
        _("Deze persoon werd begraven op %(burial_date)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(burial_date)s%(endnotes)s."),
}

buried_partial_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."
        ),
        _("Hij werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."
        ),
        _("Zij werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."
        ),
        _("Deze persoon werd begraven in %(month_year)s te %(burial_place)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(month_year)s te %(burial_place)s%(endnotes)s."),
}

buried_partial_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd begraven in %(month_year)s%(endnotes)s."),
        _("Hij werd begraven in %(month_year)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd begraven in %(month_year)s%(endnotes)s."),
        _("Zij werd begraven in %(month_year)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd begraven in %(month_year)s%(endnotes)s."),
        _("Deze persoon werd begraven in %(month_year)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(month_year)s%(endnotes)s."),
}

buried_modified_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Hij werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Zij werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."
        ),
        _("Deze persoon werd begraven %(modified_date)s te %(burial_place)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(modified_date)s te %(burial_place)s%(endnotes)s."),
}

buried_modified_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd begraven %(modified_date)s%(endnotes)s."),
        _("Hij werd begraven %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd begraven %(modified_date)s%(endnotes)s."),
        _("Zij werd begraven %(modified_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd begraven %(modified_date)s%(endnotes)s."),
        _("Deze persoon werd begraven %(modified_date)s%(endnotes)s."),
    ],
    "succinct": _("Begraven %(modified_date)s%(endnotes)s."),
}

buried_no_date_place = {
    Person.MALE: [
        _("%(male_name)s werd begraven te %(burial_place)s%(endnotes)s."),
        _("Hij werd begraven te %(burial_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd begraven te %(burial_place)s%(endnotes)s."),
        _("Zij werd begraven te %(burial_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd begraven te %(burial_place)s%(endnotes)s."),
        _("Deze persoon werd begraven te %(burial_place)s%(endnotes)s."),
    ],
    "succinct": _("Begraven te %(burial_place)s%(endnotes)s."),
}

buried_no_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd begraven%(endnotes)s."),
        _("Hij werd begraven%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd begraven%(endnotes)s."),
        _("Zij werd begraven%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd begraven%(endnotes)s."),
        _("Deze persoon werd begraven%(endnotes)s."),
    ],
    "succinct": _("Buried%(endnotes)s."),
}
# ------------------------------------------------------------------------
#
# Baptized strings
#
# ------------------------------------------------------------------------
baptised_full_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Hij werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Zij werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt op %(baptism_date)s te %(baptism_place)s%(endnotes)s."
        ),
    ],
    "succinct": _("Gedoopt %(baptism_date)s te %(baptism_place)s%(endnotes)s."),
}

baptised_full_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt op %(baptism_date)s%(endnotes)s."),
        _("Hij werd gedoopt op %(baptism_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt op %(baptism_date)s%(endnotes)s."),
        _("Zij werd gedoopt op %(baptism_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt op %(baptism_date)s%(endnotes)s."),
        _("Deze persoon werd gedoopt op %(baptism_date)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(baptism_date)s%(endnotes)s."),
}

baptised_partial_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Hij werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Zij werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt in %(month_year)s te %(baptism_place)s%(endnotes)s."
        ),
    ],
    "succinct": _("Gedoopt %(month_year)s te %(baptism_place)s%(endnotes)s."),
}

baptised_partial_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Hij werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Zij werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Deze persoon werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(month_year)s%(endnotes)s."),
}

baptised_modified_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Hij werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _("Zij werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."
        ),
    ],
    "succinct": _("Gedoopt %(modified_date)s te %(baptism_place)s%(endnotes)s."),
}

baptised_modified_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Hij werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Zij werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Deze persoon werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(modified_date)s%(endnotes)s."),
}

baptised_no_date_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt te %(baptism_place)s%(endnotes)s."),
        _("Hij werd gedoopt te %(baptism_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt te %(baptism_place)s%(endnotes)s."),
        _("Zij werd gedoopt te %(baptism_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt te %(baptism_place)s%(endnotes)s."),
        _("Deze persoon werd gedoopt te %(baptism_place)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt te %(baptism_place)s%(endnotes)s."),
}

baptised_no_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt%(endnotes)s."),
        _("Hij werd gedoopt%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt%(endnotes)s."),
        _("Zij werd gedoopt%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt%(endnotes)s."),
        _("Deze persoon werd gedoopt%(endnotes)s."),
    ],
    "succinct": _("Gedoopt%(endnotes)s."),
}

# ------------------------------------------------------------------------
#
# Christened strings
#
# ------------------------------------------------------------------------
christened_full_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
        _(
            "Hij werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
        _(
            "Zij werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt op %(christening_date)s te %(christening_place)s%(endnotes)s."
        ),
    ],
    "succinct": _(
        "Gedoopt %(christening_date)s te %(christening_place)s%(endnotes)s."
    ),
}

christened_full_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt op %(christening_date)s%(endnotes)s."),
        _("Hij werd gedoopt op %(christening_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt op %(christening_date)s%(endnotes)s."),
        _("Zij werd gedoopt op %(christening_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt op %(christening_date)s%(endnotes)s."
        ),
        _("Deze persoon werd gedoopt op %(christening_date)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(christening_date)s%(endnotes)s."),
}

christened_partial_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."
        ),
        _("Hij werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."
        ),
        _("Zij werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt in %(month_year)s te %(christening_place)s%(endnotes)s."
        ),
    ],
    "succinct": _("Gedoopt %(month_year)s te %(christening_place)s%(endnotes)s."),
}

christened_partial_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Hij werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Zij werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt in %(month_year)s%(endnotes)s."),
        _("Deze persoon werd gedoopt in %(month_year)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(month_year)s%(endnotes)s."),
}

christened_modified_date_place = {
    Person.MALE: [
        _(
            "%(male_name)s werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."
        ),
        _("Hij werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "%(female_name)s werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."
        ),
        _("Zij werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."
        ),
        _(
            "Deze persoon werd gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."
        ),
    ],
    "succinct": _("Gedoopt %(modified_date)s te %(christening_place)s%(endnotes)s."),
}

christened_modified_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Hij werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Zij werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt %(modified_date)s%(endnotes)s."),
        _("Deze persoon werd gedoopt %(modified_date)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt %(modified_date)s%(endnotes)s."),
}

christened_no_date_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt te %(christening_place)s%(endnotes)s."),
        _("Hij werd gedoopt te %(christening_place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt te %(christening_place)s%(endnotes)s."),
        _("Zij werd gedoopt te %(christening_place)s%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _(
            "%(unknown_gender_name)s werd gedoopt te %(christening_place)s%(endnotes)s."
        ),
        _("Deze persoon werd gedoopt te %(christening_place)s%(endnotes)s."),
    ],
    "succinct": _("Gedoopt te %(christening_place)s%(endnotes)s."),
}

christened_no_date_no_place = {
    Person.MALE: [
        _("%(male_name)s werd gedoopt%(endnotes)s."),
        _("Hij werd gedoopt%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("%(female_name)s werd gedoopt%(endnotes)s."),
        _("Zij werd gedoopt%(endnotes)s."),
    ],
    Person.UNKNOWN: [
        _("%(unknown_gender_name)s werd gedoopt%(endnotes)s."),
        _("Deze persoon werd gedoopt%(endnotes)s."),
    ],
    "succinct": _("Gedoopt%(endnotes)s."),
}

# -------------------------------------------------------------------------
#
#  child to parent relationships
#
# -------------------------------------------------------------------------
child_father_mother = {
    Person.UNKNOWN: [
        [
            _("%(male_name)s is het kind van %(father)s en %(mother)s."),
            _("%(male_name)s was het kind van %(father)s en %(mother)s."),
        ],
        [
            _("Deze persoon is het kind van %(father)s en %(mother)s."),
            _("Deze persoon was het kind van %(father)s en %(mother)s."),
        ],
        _("Child of %(father)s en %(mother)s."),
    ],
    Person.MALE: [
        [
            _("%(male_name)s is de zoon van %(father)s en %(mother)s."),
            _("%(male_name)s was de zoon van %(father)s en %(mother)s."),
        ],
        [
            _("Hij is de zoon van %(father)s en %(mother)s."),
            _("Hij was de zoon van %(father)s en %(mother)s."),
        ],
        _("Zoon van %(father)s en %(mother)s."),
    ],
    Person.FEMALE: [
        [
            _("%(female_name)s is de dochter van %(father)s en %(mother)s."),
            _("%(female_name)s was de dochter van %(father)s en %(mother)s."),
        ],
        [
            _("Zij is de dochter van %(father)s en %(mother)s."),
            _("Zij was de dochter van %(father)s en %(mother)s."),
        ],
        _("Dochter van %(father)s en %(mother)s."),
    ],
}

child_father = {
    Person.UNKNOWN: [
        [
            _("%(male_name)s is het kind van %(father)s."),
            _("%(male_name)s was het kind van %(father)s."),
        ],
        [
            _("Deze persoon is het kind van %(father)s."),
            _("Deze persoon was het kind van %(father)s."),
        ],
        _("Kind van %(father)s."),
    ],
    Person.MALE: [
        [
            _("%(male_name)s is de zoon van %(father)s."),
            _("%(male_name)s was de zoon van %(father)s."),
        ],
        [
            _("Hij is de zoon van %(father)s."),
            _("Hij was de zoon van %(father)s."),
        ],
        _("Zoon van %(father)s."),
    ],
    Person.FEMALE: [
        [
            _("%(female_name)s is de dochter van %(father)s."),
            _("%(female_name)s was de dochter van %(father)s."),
        ],
        [
            _("Zij is de dochter van %(father)s."),
            _("Zij was de dochter van %(father)s."),
        ],
        _("Dochter van %(father)s."),
    ],
}

child_mother = {
    Person.UNKNOWN: [
        [
            _("%(male_name)s is het kind van %(mother)s."),
            _("%(male_name)s was het kind van %(mother)s."),
        ],
        [
            _("Deze persoon is het kind van %(mother)s."),
            _("Deze persoon was het kind van %(mother)s."),
        ],
        _("Child of %(mother)s."),
    ],
    Person.MALE: [
        [
            _("%(male_name)s is de zoon van %(mother)s."),
            _("%(male_name)s was de zoon van %(mother)s."),
        ],
        [
            _("Hij is de zoon van %(mother)s."),
            _("Hij was de zoon van %(mother)s."),
        ],
        _("Zoon van %(mother)s."),
    ],
    Person.FEMALE: [
        [
            _("%(female_name)s is de dochter van %(mother)s."),
            _("%(female_name)s was de dochter van %(mother)s."),
        ],
        [
            _("Zij is de dochter van %(mother)s."),
            _("Zij was de dochter van %(mother)s."),
        ],
        _("Dochter van %(mother)s."),
    ],
}

# ------------------------------------------------------------------------
#
# Marriage strings - Relationship type trouwde
#
# ------------------------------------------------------------------------
marriage_first_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon trouwde %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _("Deze persoon trouwde %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."),
        _("Deze persoon trouwde %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
    Person.MALE: [
        _("Hij trouwde %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."),
        _("Hij trouwde %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."),
        _("Hij trouwde %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("Zij trouwde %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."),
        _("Zij trouwde %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."),
        _("Zij trouwde %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
    "succinct": [
        _("Trouwde %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."),
        _("Trouwde %(spouse)s %(full_date)s te %(place)s%(endnotes)s."),
        _("Trouwde %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
}

marriage_also_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon trouwde ook met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon trouwde ook met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon trouwde ook met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _("Hij trouwde ook met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."),
        _("Hij trouwde ook met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."),
        _("Hij trouwde ook met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("Zij trouwde ook met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."),
        _("Zij trouwde ook met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."),
        _("Zij trouwde ook met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
    "succinct": [
        _("Trouwde ook met %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."),
        _("Trouwde ook met %(spouse)s %(full_date)s te %(place)s%(endnotes)s."),
        _("Trouwde ook met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
}

marriage_first_date = {
    Person.UNKNOWN: [
        _("Deze persoon trouwde %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Deze persoon trouwde %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Deze persoon trouwde %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.MALE: [
        _("Hij trouwde %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Hij trouwde %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Hij trouwde %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("Zij trouwde %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Zij trouwde %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Zij trouwde %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    "succinct": [
        _("Trouwde %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Trouwde %(spouse)s %(full_date)s%(endnotes)s."),
        _("Trouwde %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

marriage_also_date = {
    Person.UNKNOWN: [
        _("Deze persoon trouwde ook met %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Deze persoon trouwde ook met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Deze persoon trouwde ook met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.MALE: [
        _("Hij trouwde ook met %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Hij trouwde ook met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Hij trouwde ook met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("Zij trouwde ook met %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Zij trouwde ook met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Zij trouwde ook met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    "succinct": [
        _("Trouwde ook met %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Trouwde ook met %(spouse)s %(full_date)s%(endnotes)s."),
        _("Trouwde ook met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

marriage_first_place = {
    Person.UNKNOWN: _("Deze persoon trouwde met %(spouse)s te %(place)s%(endnotes)s."),
    Person.MALE: _("Hij trouwde met %(spouse)s te %(place)s%(endnotes)s."),
    Person.FEMALE: _("Zij trouwde met %(spouse)s te %(place)s%(endnotes)s."),
    "succinct": _("Trouwde met %(spouse)s te %(place)s%(endnotes)s."),
}

marriage_also_place = {
    Person.UNKNOWN: _("Deze persoon trouwde ook met %(spouse)s te %(place)s%(endnotes)s."),
    Person.MALE: _("Hij trouwde ook met %(spouse)s te %(place)s%(endnotes)s."),
    Person.FEMALE: _("Zij trouwde ook met %(spouse)s te %(place)s%(endnotes)s."),
    "succinct": _("Trouwde ook met %(spouse)s te %(place)s%(endnotes)s."),
}

marriage_first_only = {
    Person.UNKNOWN: _("Deze persoon trouwde met %(spouse)s%(endnotes)s."),
    Person.MALE: _("Hij trouwde met %(spouse)s%(endnotes)s."),
    Person.FEMALE: _("Zij trouwde met %(spouse)s%(endnotes)s."),
    "succinct": _("Trouwde met %(spouse)s%(endnotes)s."),
}

marriage_also_only = {
    Person.UNKNOWN: _("Deze persoon trouwde ook met %(spouse)s%(endnotes)s."),
    Person.MALE: _("Hij trouwde ook met %(spouse)s%(endnotes)s."),
    Person.FEMALE: _("Zij trouwde ook met %(spouse)s%(endnotes)s."),
    "succinct": _("Trouwde ook met %(spouse)s%(endnotes)s."),
}

# ------------------------------------------------------------------------
#
# Marriage strings - Relationship type UNMARRIED
#
# ------------------------------------------------------------------------
unmarried_first_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had een relatie met  %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met  %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met  %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had een relatie met  %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met  %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met  %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had een relatie met  %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met  %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met  %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _(
            "Relatie met %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Relatie met %(spouse)s %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
}

unmarried_also_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _(
            "Relatie met %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Relatie met %(spouse)s %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
}

unmarried_first_date = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had een relatie met  %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met  %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met  %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had een relatie met  %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met  %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met  %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had een relatie met  %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met  %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met  %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _("Relatie met %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(full_date)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

unmarried_also_date = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _("Ook  relatie met %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Ook  relatie met %(spouse)s %(full_date)s%(endnotes)s."),
        _("Ook  relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

unmarried_first_place = {
    Person.UNKNOWN: _(
        "Deze persoon had een relatie met  %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.MALE: _(
        "Hij had een relatie met  %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.FEMALE: _(
        "Zij had een relatie met  %(spouse)s te %(place)s%(endnotes)s."
    ),
    "succinct": _("Relatie met %(spouse)s te %(place)s%(endnotes)s."),
}

unmarried_also_place = {
    Person.UNKNOWN: _(
        "Deze persoon had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.MALE: _(
        "Hij had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.FEMALE: _(
        "Zij had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    "succinct": _("Relatie met %(spouse)s te %(place)s%(endnotes)s."),
}

unmarried_first_only = {
    Person.UNKNOWN: _(
        "Deze persoon had een relatie met  %(spouse)s%(endnotes)s."
    ),
    Person.MALE: _("Hij had een relatie met  %(spouse)s%(endnotes)s."),
    Person.FEMALE: _("Zij had een relatie met  %(spouse)s%(endnotes)s."),
    "succinct": _("Relatie met %(spouse)s%(endnotes)s."),
}

unmarried_also_only = {
    Person.UNKNOWN: _(
        "Deze persoon had ook een relatie met %(spouse)s%(endnotes)s."
    ),
    Person.MALE: _(
        "Hij had ook een relatie met %(spouse)s%(endnotes)s."
    ),
    Person.FEMALE: _(
        "Zij had ook een relatie met %(spouse)s%(endnotes)s."
    ),
    "succinct": _("Relatie met %(spouse)s%(endnotes)s."),
}

# ------------------------------------------------------------------------
#
# Marriage strings - Relationship type other than trouwde or UNMARRIED
#                    i.e. CIVIL UNION or CUSTOM
#
# ------------------------------------------------------------------------
relationship_first_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _("Relatie met %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(full_date)s te %(place)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."),
    ],
}

relationship_also_date_place = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Hij had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    Person.FEMALE: [
        _(
            "Zij had ook een relatie met %(spouse)s in %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s op %(full_date)s te %(place)s%(endnotes)s."
        ),
        _(
            "Zij had ook een relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
    "succinct": [
        _(
            "Ook relatie met %(spouse)s %(partial_date)s te %(place)s%(endnotes)s."
        ),
        _("Ook relatie met %(spouse)s %(full_date)s te %(place)s%(endnotes)s."),
        _(
            "Ook relatie met %(spouse)s %(modified_date)s te %(place)s%(endnotes)s."
        ),
    ],
}

relationship_first_date = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had een relatie met %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _("Hij had een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Hij had een relatie met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Hij had een relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _("Zij had een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."),
        _("Zij had een relatie met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Zij had een relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    "succinct": [
        _("Relatie met %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(full_date)s%(endnotes)s."),
        _("Relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

relationship_also_date = {
    Person.UNKNOWN: [
        _(
            "Deze persoon had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."
        ),
        _(
            "Deze persoon had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."
        ),
    ],
    Person.MALE: [
        _(
            "Hij had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _("Hij had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Hij had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    Person.FEMALE: [
        _(
            "Zij had ook een relatie met %(spouse)s in %(partial_date)s%(endnotes)s."
        ),
        _("Zij had ook een relatie met %(spouse)s op %(full_date)s%(endnotes)s."),
        _("Zij had ook een relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
    "succinct": [
        _("Ook relatie met %(spouse)s %(partial_date)s%(endnotes)s."),
        _("Ook relatie met %(spouse)s %(full_date)s%(endnotes)s."),
        _("Ook relatie met %(spouse)s %(modified_date)s%(endnotes)s."),
    ],
}

relationship_first_place = {
    Person.UNKNOWN: _(
        "Deze persoon had een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.MALE: _("Hij had een relatie met %(spouse)s te %(place)s%(endnotes)s."),
    Person.FEMALE: _(
        "Zij had een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    "succinct": _("Relatie met %(spouse)s te %(place)s%(endnotes)s."),
}

relationship_also_place = {
    Person.UNKNOWN: _(
        "Deze persoon had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.MALE: _(
        "Hij had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    Person.FEMALE: _(
        "Zij had ook een relatie met %(spouse)s te %(place)s%(endnotes)s."
    ),
    "succinct": _("Ook relatie met %(spouse)s te %(place)s%(endnotes)s."),
}

relationship_first_only = {
    Person.UNKNOWN: _("Deze persoon had een relatie met %(spouse)s%(endnotes)s."),
    Person.MALE: _("Hij had een relatie met %(spouse)s%(endnotes)s."),
    Person.FEMALE: _("Zij had een relatie met %(spouse)s%(endnotes)s."),
    "succinct": _("Relatie met %(spouse)s%(endnotes)s."),
}

relationship_also_only = {
    Person.UNKNOWN: _(
        "Deze persoon had ook een relatie met %(spouse)s%(endnotes)s."
    ),
    Person.MALE: _("Hij had ook een relatie met %(spouse)s%(endnotes)s."),
    Person.FEMALE: _("Zij had ook een relatie met %(spouse)s%(endnotes)s."),
    "succinct": _("Ook relatie met %(spouse)s%(endnotes)s."),
}


# ------------------------------------------------------------------------
#
# Narrator
#
# ------------------------------------------------------------------------
class Narrator:
    """
    Narrator is a class which provides narration text.
    """

    def __init__(
        self,
        dbase,
        verbose=True,
        use_call_name=False,
        use_fulldate=False,
        empty_date="",
        empty_place="",
        place_format=-1,
        nlocale=glocale,
        get_endnote_numbers=_get_empty_endnote_numbers,
    ):
        """
        Initialize the narrator class.

        If nlocale is passed in (a GrampsLocale), then
        the translated values will be returned instead.

        :param dbase: The database that contains the data to be narrated.
        :type dbase: :class:`~gen.db.base,DbBase`
        :param verbose: Specifies whether complete sentences should be used.
        :type verbose: bool
        :param use_call_name: Specifies whether a person's call name should be
            used for the first name.
        :type use_call_name: bool
        :param empty_date: String to use when a date is not known.
        :type empty_date: str
        :param empty_place: String to use when a place is not known.
        :type empty_place: str
        :param get_endnote_numbers: A callable to use for getting a string
            representing endnote numbers.
            The function takes a :class:`~gen.lib.CitationBase` instance.
            A typical return value from get_endnote_numbers() would be "2a" and
            would represent a reference to an endnote in a document.
        :type get_endnote_numbers:
            callable( :class:`~gen.lib.CitationBase` )
        :param nlocale: allow deferred translation of dates and strings
        :type nlocale: a GrampsLocale instance
        :param place_format: allow display of places in any place format
        :type place_format: int
        """
        self.__db = dbase
        self.__verbose = verbose
        self.__use_call = use_call_name
        self.__use_fulldate = use_fulldate
        self.__empty_date = empty_date
        self.__empty_place = empty_place
        self.__get_endnote_numbers = get_endnote_numbers
        self.__person = None
        self.__first_name = ""
        self.__first_name_used = False

        self.__translate_text = nlocale.translation.gettext
        self.__get_date = nlocale.get_date
        self._locale = nlocale
        self._place_format = place_format

    def set_subject(self, person):
        """
        Start a new story about this person. The person's first name will be
        used in the first sentence. A pronoun will be used as the subject for
        each subsequent sentence.
        :param person: The person to be the subject of the story.
        :type person: :class:`~gen.lib.person,Person`
        """
        self.__person = person

        if self.__use_call and person.get_primary_name().get_call_name():
            self.__first_name = person.get_primary_name().get_call_name()
        else:
            self.__first_name = person.get_primary_name().get_first_name()

        if self.__first_name:
            self.__first_name_used = False  # use their name the first time
        else:
            self.__first_name_used = True  # but use a pronoun if no name

    def get_born_string(self):
        """
        Get a string narrating the birth of the subject.
        Example sentences:
            Person was born on Date.
            Person was born on Date in Place.
            Person was born in Place.
            ''

        :returns: A sentence about the subject's birth.
        :rtype: unicode
        """
        if not self.__first_name_used:
            name_index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            name_index = _NAME_INDEX_EXCLUDE_NAME

        text = ""

        bplace = self.__empty_place
        bdate = self.__empty_date
        birth_event = None
        bdate_full = False
        bdate_mod = False

        birth_ref = self.__person.get_birth_ref()
        if birth_ref and birth_ref.ref:
            birth_event = self.__db.get_event_from_handle(birth_ref.ref)
            if birth_event:
                if self.__use_fulldate:
                    bdate = self.__get_date(birth_event.get_date_object())
                else:
                    bdate = birth_event.get_date_object().get_year()
                bplace_handle = birth_event.get_place_handle()
                if bplace_handle:
                    place = self.__db.get_place_from_handle(bplace_handle)
                    bplace = _pd.display_event(
                        self.__db, birth_event, fmt=self._place_format
                    )
                bdate_obj = birth_event.get_date_object()
                bdate_full = bdate_obj and bdate_obj.get_day_valid()
                bdate_mod = bdate_obj and bdate_obj.get_modifier() != Date.MOD_NONE

        if self._locale.locale_code() == "Hij":
            bdate = convert_prefix(bdate)
            bplace = convert_prefix(bplace)

        value_map = {
            "name": self.__first_name,
            "male_name": self.__first_name,
            "unknown_gender_name": self.__first_name,
            "female_name": self.__first_name,
            "birth_date": bdate,
            "birth_place": bplace,
            "month_year": bdate,
            "modified_date": bdate,
        }

        gender = self.__get_gender()

        if bdate:
            if bdate_mod:
                if bplace and self.__verbose:
                    text = born_modified_date_with_place[name_index][gender]
                elif bplace:
                    text = born_modified_date_with_place[2]
                elif self.__verbose:
                    text = born_modified_date_no_place[name_index][gender]
                else:
                    text = born_modified_date_no_place[2]
            elif bdate_full:
                if bplace and self.__verbose:
                    text = born_full_date_with_place[name_index][gender]
                elif bplace:
                    text = born_full_date_with_place[2]
                elif self.__verbose:
                    text = born_full_date_no_place[name_index][gender]
                else:
                    text = born_full_date_no_place[2]
            else:
                if bplace and self.__verbose:
                    text = born_partial_date_with_place[name_index][gender]
                elif bplace:
                    text = born_partial_date_with_place[2]
                elif self.__verbose:
                    text = born_partial_date_no_place[name_index][gender]
                else:
                    text = born_partial_date_no_place[2]
        else:
            if bplace and self.__verbose:
                text = born_no_date_with_place[name_index][gender]
            elif bplace:
                text = born_no_date_with_place[2]
            else:
                text = ""

        if text:
            text = self.__translate_text(text) % value_map

            if birth_event:
                text = text.rstrip(". ")
                text = text + self.__get_endnote_numbers(birth_event) + ". "

            text = text + " "

        return text

    def get_died_string(self, include_age=False):
        """
        Get a string narrating the death of the subject.
        Example sentences:
            Person died on Date
            Person died on Date at the age of 'age'
            Person died on Date in Place
            Person died on Date in Place at the age of 'age'
            Person overleed in Place
            Person overleed in Place at the age of 'age'
            Person died
            ''
        where 'age' string is an advanced age calculation.

        :returns: A sentence about the subject's death.
        :rtype: unicode
        """

        if not self.__first_name_used:
            name_index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            name_index = _NAME_INDEX_EXCLUDE_NAME

        text = ""

        dplace = self.__empty_place
        ddate = self.__empty_date
        death_event = None
        ddate_full = False
        ddate_mod = False

        death_ref = self.__person.get_death_ref()
        if death_ref and death_ref.ref:
            death_event = self.__db.get_event_from_handle(death_ref.ref)
            if death_event:
                if self.__use_fulldate:
                    ddate = self.__get_date(death_event.get_date_object())
                else:
                    ddate = death_event.get_date_object().get_year()
                dplace_handle = death_event.get_place_handle()
                if dplace_handle:
                    place = self.__db.get_place_from_handle(dplace_handle)
                    dplace = _pd.display_event(
                        self.__db, death_event, fmt=self._place_format
                    )
                ddate_obj = death_event.get_date_object()
                ddate_full = ddate_obj and ddate_obj.get_day_valid()
                ddate_mod = ddate_obj and ddate_obj.get_modifier() != Date.MOD_NONE

        if include_age:
            age, age_index = self.__get_age_at_death()
        else:
            age = 0
            age_index = _AGE_INDEX_NO_AGE

        if self._locale.locale_code() == "Hij":
            ddate = convert_prefix(ddate)
            dplace = convert_prefix(dplace)

        value_map = {
            "name": self.__first_name,
            "unknown_gender_name": self.__first_name,
            "male_name": self.__first_name,
            "female_name": self.__first_name,
            "death_date": ddate,
            "modified_date": ddate,
            "death_place": dplace,
            "age": age,
            "month_year": ddate,
        }

        gender = self.__get_gender()

        if ddate and ddate_mod:
            if dplace and self.__verbose:
                text = died_modified_date_with_place[name_index][gender][age_index]
            elif dplace:
                text = died_modified_date_with_place[2][age_index]
            elif self.__verbose:
                text = died_modified_date_no_place[name_index][gender][age_index]
            else:
                text = died_modified_date_no_place[2][age_index]
        elif ddate and ddate_full:
            if dplace and self.__verbose:
                text = died_full_date_with_place[name_index][gender][age_index]
            elif dplace:
                text = died_full_date_with_place[2][age_index]
            elif self.__verbose:
                text = died_full_date_no_place[name_index][gender][age_index]
            else:
                text = died_full_date_no_place[2][age_index]
        elif ddate:
            if dplace and self.__verbose:
                text = died_partial_date_with_place[name_index][gender][age_index]
            elif dplace:
                text = died_partial_date_with_place[2][age_index]
            elif self.__verbose:
                text = died_partial_date_no_place[name_index][gender][age_index]
            else:
                text = died_partial_date_no_place[2][age_index]
        elif dplace and self.__verbose:
            text = died_no_date_with_place[name_index][gender][age_index]
        elif dplace:
            text = died_no_date_with_place[2][age_index]
        elif self.__verbose:
            text = died_no_date_no_place[name_index][gender][age_index]
        else:
            text = died_no_date_no_place[2][age_index]

        if text:
            text = self.__translate_text(text) % value_map

            if death_event:
                text = text.rstrip(". ")
                text = text + self.__get_endnote_numbers(death_event) + ". "

            text = text + " "

        return text

    def get_buried_string(self):
        """
        Get a string narrating the burial of the subject.
        Example sentences:
            Person was  buried on Date.
            Person was  buried on Date in Place.
            Person was  buried in Month_Year.
            Person was  buried in Month_Year in Place.
            Person was  buried in Place.
            ''

        :returns: A sentence about the subject's burial.
        :rtype: unicode
        """

        if not self.__first_name_used:
            name_index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            name_index = _NAME_INDEX_EXCLUDE_NAME

        gender = self.__get_gender()

        text = ""

        bplace = self.__empty_place
        bdate = self.__empty_date
        bdate_full = False
        bdate_mod = False

        burial = None
        for event_ref in self.__person.get_event_ref_list():
            event = self.__db.get_event_from_handle(event_ref.ref)
            if (
                event
                and event.type.value == EventType.BURIAL
                and event_ref.role.value == EventRoleType.PRIMARY
            ):
                burial = event
                break

        if burial:
            if self.__use_fulldate:
                bdate = self.__get_date(burial.get_date_object())
            else:
                bdate = burial.get_date_object().get_year()
            bplace_handle = burial.get_place_handle()
            if bplace_handle:
                place = self.__db.get_place_from_handle(bplace_handle)
                bplace = _pd.display_event(self.__db, burial, fmt=self._place_format)
            bdate_obj = burial.get_date_object()
            bdate_full = bdate_obj and bdate_obj.get_day_valid()
            bdate_mod = bdate_obj and bdate_obj.get_modifier() != Date.MOD_NONE
        else:
            return text

        if self._locale.locale_code() == "Hij":
            bdate = convert_prefix(bdate)
            bplace = convert_prefix(bplace)

        value_map = {
            "unknown_gender_name": self.__first_name,
            "male_name": self.__first_name,
            "name": self.__first_name,
            "female_name": self.__first_name,
            "burial_date": bdate,
            "burial_place": bplace,
            "month_year": bdate,
            "modified_date": bdate,
            "endnotes": self.__get_endnote_numbers(event),
        }

        if bdate and bdate_mod and self.__verbose:
            if bplace:  # male, date, place
                text = buried_modified_date_place[gender][name_index]
            else:  # male, date, no place
                text = buried_modified_date_no_place[gender][name_index]
        elif bdate and bdate_mod:
            if bplace:  # male, date, place
                text = buried_modified_date_place["succinct"]
            else:  # male, date, no place
                text = buried_modified_date_no_place["succinct"]
        elif bdate and bdate_full and self.__verbose:
            if bplace:  # male, date, place
                text = buried_full_date_place[gender][name_index]
            else:  # male, date, no place
                text = buried_full_date_no_place[gender][name_index]
        elif bdate and bdate_full:
            if bplace:  # male, date, place
                text = buried_full_date_place["succinct"]
            else:  # male, date, no place
                text = buried_full_date_no_place["succinct"]
        elif bdate and self.__verbose:
            if bplace:  # male, month_year, place
                text = buried_partial_date_place[gender][name_index]
            else:  # male, month_year, no place
                text = buried_partial_date_no_place[gender][name_index]
        elif bdate:
            if bplace:  # male, month_year, place
                text = buried_partial_date_place["succinct"]
            else:  # male, month_year, no place
                text = buried_partial_date_no_place["succinct"]
        elif bplace and self.__verbose:  # male, no date, place
            text = buried_no_date_place[gender][name_index]
        elif bplace:  # male, no date, place
            text = buried_no_date_place["succinct"]
        elif self.__verbose:
            text = buried_no_date_no_place[gender][name_index]
        else:  # male, no date, no place
            text = buried_no_date_no_place["succinct"]

        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "

        return text

    def get_baptised_string(self):
        """
        Get a string narrating the baptism of the subject.
        Example sentences:
            Person werd gedoopt op Date.
            Person werd gedoopt op Date in Place.
            Person werd gedoopt in Month_Year.
            Person werd gedoopt in Month_Year in Place.
            Person werd gedoopt in Place.
            ''

        :returns: A sentence about the subject's baptism.
        :rtype: unicode
        """

        if not self.__first_name_used:
            name_index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            name_index = _NAME_INDEX_EXCLUDE_NAME

        gender = self.__get_gender()

        text = ""

        bplace = self.__empty_place
        bdate = self.__empty_date
        bdate_full = False
        bdate_mod = False

        baptism = None
        for event_ref in self.__person.get_event_ref_list():
            event = self.__db.get_event_from_handle(event_ref.ref)
            if (
                event
                and event.type.value == EventType.BAPTISM
                and event_ref.role.value == EventRoleType.PRIMARY
            ):
                baptism = event
                break

        if baptism:
            if self.__use_fulldate:
                bdate = self.__get_date(baptism.get_date_object())
            else:
                bdate = baptism.get_date_object().get_year()                
            bplace_handle = baptism.get_place_handle()
            if bplace_handle:
                place = self.__db.get_place_from_handle(bplace_handle)
                bplace = _pd.display_event(self.__db, baptism, fmt=self._place_format)
            bdate_obj = baptism.get_date_object()
            bdate_full = bdate_obj and bdate_obj.get_day_valid()
            bdate_mod = bdate_obj and bdate_obj.get_modifier() != Date.MOD_NONE
        else:
            return text

        if self._locale.locale_code() == "Hij":
            bdate = convert_prefix(bdate)
            bplace = convert_prefix(bplace)

        value_map = {
            "unknown_gender_name": self.__first_name,
            "male_name": self.__first_name,
            "name": self.__first_name,
            "female_name": self.__first_name,
            "baptism_date": bdate,
            "baptism_place": bplace,
            "month_year": bdate,
            "modified_date": bdate,
            "endnotes": self.__get_endnote_numbers(event),
        }

        if bdate and bdate_mod and self.__verbose:
            if bplace:  # male, date, place
                text = baptised_modified_date_place[gender][name_index]
            else:  # male, date, no place
                text = baptised_modified_date_no_place[gender][name_index]
        elif bdate and bdate_mod:
            if bplace:  # male, date, place
                text = baptised_modified_date_place["succinct"]
            else:  # male, date, no place
                text = baptised_modified_date_no_place["succinct"]
        elif bdate and bdate_full and self.__verbose:
            if bplace:  # male, date, place
                text = baptised_full_date_place[gender][name_index]
            else:  # male, date, no place
                text = baptised_full_date_no_place[gender][name_index]
        elif bdate and bdate_full:
            if bplace:  # male, date, place
                text = baptised_full_date_place["succinct"]
            else:  # male, date, no place
                text = baptised_full_date_no_place["succinct"]
        elif bdate and self.__verbose:
            if bplace:  # male, month_year, place
                text = baptised_partial_date_place[gender][name_index]
            else:  # male, month_year, no place
                text = baptised_partial_date_no_place[gender][name_index]
        elif bdate:
            if bplace:  # male, month_year, place
                text = baptised_partial_date_place["succinct"]
            else:  # male, month_year, no place
                text = baptised_partial_date_no_place["succinct"]
        elif bplace and self.__verbose:  # male, no date, place
            text = baptised_no_date_place[gender][name_index]
        elif bplace:  # male, no date, place
            text = baptised_no_date_place["succinct"]
        elif self.__verbose:
            text = baptised_no_date_no_place[gender][name_index]
        else:  # male, no date, no place
            text = baptised_no_date_no_place["succinct"]
        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "
        
        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "
        if event.get_description():
            if text:
                text += ". "
            text += event.get_description() + " "
        return text
    
    def get_witnesses_string(self):
        witnesses = None
        for event_ref in self.__person.get_event_ref_list():
            event = self.__db.get_event_from_handle(event_ref.ref)
            if event and (event.type.value == EventType.BAPTISM \
                    or event.type.value == EventType.CHRISTEN) \
                    and event_ref.role.value == EventRoleType.PRIMARY:
                witnesses = event
                break
        if witnesses:
            note = ""
            notelist = witnesses.get_note_list()
            for notehandle in notelist:
                note = self.__db.get_note_from_handle(notehandle)
                break
            if note:
                text = "{Get: " + str(note.get_styledtext()) + "} "
                return text
            else:
                return None

    
    def get_christening_notes(self):
        christening = None
        for event_ref in self.__person.get_event_ref_list():
            event = self.__db.get_event_from_handle(event_ref.ref)
            if event and event.type.value == EventType.CHRISTEN \
                    and event_ref.role.value == EventRoleType.PRIMARY:
                christening = event
                break

        if christening:
            note = ""
            notelist = christening.get_note_list()
            for notehandle in notelist:
                note = self.__db.get_note_from_handle(notehandle)
                break
            if note:
                return note
            else:
                return None


    def get_christened_string(self):
        """
        Get a string narrating the christening of the subject.
        Example sentences:
            Person werd gedoopt op Date.
            Person werd gedoopt op Date in Place.
            Person werd gedoopt in Month_Year.
            Person werd gedoopt in Month_Year in Place.
            Person werd gedoopt in Place.
            ''

        :returns: A sentence about the subject's christening.
        :rtype: unicode
        """

        if not self.__first_name_used:
            name_index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            name_index = _NAME_INDEX_EXCLUDE_NAME

        gender = self.__get_gender()

        text = ""

        cplace = self.__empty_place
        cdate = self.__empty_date
        cdate_full = False
        cdate_mod = False

        christening = None
        for event_ref in self.__person.get_event_ref_list():
            event = self.__db.get_event_from_handle(event_ref.ref)
            if (
                event
                and event.type.value == EventType.CHRISTEN
                and event_ref.role.value == EventRoleType.PRIMARY
            ):
                christening = event
                break

        if christening:
            if self.__use_fulldate:
                cdate = self.__get_date(christening.get_date_object())
                cdate = cdate.replace(" ", "\xa0")
            else:
                cdate = christening.get_date_object().get_year()
            cplace_handle = christening.get_place_handle()
            if cplace_handle:
                place = self.__db.get_place_from_handle(cplace_handle)
                cplace = _pd.display_event(
                    self.__db, christening, fmt=self._place_format
                )
            cdate_obj = christening.get_date_object()
            cdate_full = cdate_obj and cdate_obj.get_day_valid()
            cdate_mod = cdate_obj and cdate_obj.get_modifier() != Date.MOD_NONE
        else:
            return text

        if self._locale.locale_code() == "He":
            cdate = convert_prefix(cdate)
            cplace = convert_prefix(cplace)

        value_map = {
            "unknown_gender_name": self.__first_name,
            "male_name": self.__first_name,
            "name": self.__first_name,
            "female_name": self.__first_name,
            "christening_date": cdate,
            "christening_place": cplace,
            "month_year": cdate,
            "modified_date": cdate,
            "endnotes": self.__get_endnote_numbers(event),
        }

        if cdate and cdate_mod and self.__verbose:
            if cplace:  # male, date, place
                text = christened_modified_date_place[gender][name_index]
            else:  # male, date, no place
                text = christened_modified_date_no_place[gender][name_index]
        elif cdate and cdate_mod:
            if cplace:  # male, date, place
                text = christened_modified_date_place["succinct"]
            else:  # male, date, no place
                text = christened_modified_date_no_place["succinct"]
        elif cdate and cdate_full and self.__verbose:
            if cplace:  # male, date, place
                text = christened_full_date_place[gender][name_index]
            else:  # male, date, no place
                text = christened_full_date_no_place[gender][name_index]
        elif cdate and cdate_full:
            if cplace:  # male, date, place
                text = christened_full_date_place["succinct"]
            else:  # male, date, no place
                text = christened_full_date_no_place["succinct"]
        elif cdate and self.__verbose:
            if cplace:  # male, month_year, place
                text = christened_partial_date_place[gender][name_index]
            else:  # male, month_year, no place
                text = christened_partial_date_no_place[gender][name_index]
        elif cdate:
            if cplace:  # male, month_year, place
                text = christened_partial_date_place["succinct"]
            else:  # male, month_year, no place
                text = christened_partial_date_no_place["succinct"]
        elif cplace and self.__verbose:  # male, no date, place
            text = christened_no_date_place[gender][name_index]
        elif cplace:  # male, no date, place
            text = christened_no_date_place["succinct"]
        elif self.__verbose:
            text = christened_no_date_no_place[gender][name_index]
        else:  # male, no date, no place
            text = christened_no_date_no_place["succinct"]
        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "
            return text
    
    def get_married_string(self, family, is_first=True, name_display=None):
        """
        Get a string narrating the marriage of the subject.
        Example sentences:
            Person was trouwde to Spouse on Date.
            Person was trouwde to Spouse.
            Person was trouwde ook met to Spouse on Date.
            Person was trouwde ook met to Spouse.
            ""

        :param family: The family that contains the Spouse for this marriage.
        :type family: :class:`~gen.lib.family,Family`
        :param is_first: Indicates whether this sentence represents the first
            marriage. If it is not the first marriage, the sentence will
            include "also".
        :type is_first: bool
        :param name_display: An object to be used for displaying names
        :type name_display: :class:`~gen.display.name,NameDisplay`
        :returns: A sentence about the subject's marriage.
        :rtype: unicode
        """

        date = self.__empty_date
        place = self.__empty_place

        spouse_name = None
        spouse_handle = utils.find_spouse(self.__person, family)
        if spouse_handle:
            spouse = self.__db.get_person_from_handle(spouse_handle)
            if spouse:
                if not name_display:
                    spouse_name = _nd.display(spouse)
                else:
                    spouse_name = name_display.display(spouse)
        if not spouse_name:
            spouse_name = self.__translate_text("Unknown")  # not: _("Unknown")

        event = utils.find_marriage(self.__db, family)
        if event:
            if self.__use_fulldate:
                mdate = self.__get_date(event.get_date_object())
            else:
                mdate = event.get_date_object().get_year()
            if mdate:
                date = mdate
            place_handle = event.get_place_handle()
            if place_handle:
                place_obj = self.__db.get_place_from_handle(place_handle)
                place = _pd.display_event(self.__db, event, fmt=self._place_format)
        relationship = family.get_relationship()

        if self._locale.locale_code() == "Hij":
            date = convert_prefix(date)
            place = convert_prefix(place)

        value_map = {
            "spouse": spouse_name,
            "endnotes": self.__get_endnote_numbers(event),
            "full_date": date,
            "modified_date": date,
            "partial_date": date,
            "place": place,
        }

        date_full = 0

        if event:
            dobj = event.get_date_object()

            if dobj.get_modifier() != Date.MOD_NONE:
                date_full = 2
            elif dobj and dobj.get_day_valid():
                date_full = 1

        gender = self.__get_gender()

        # This would be much simpler, excepting for translation considerations
        # Currently support FamilyRelType's:
        #     trouwde     : civil and/or religious
        #     UNMARRIED
        #     CIVIL UNION : described as a relationship
        #     UNKNOWN     : also described as a relationship
        #     CUSTOM      : also described as a relationship
        #
        # In the future, there may be a need to distinguish between
        # CIVIL UNION, UNKNOWN and CUSTOM relationship types
        # CUSTOM will be difficult as user can supply any arbitrary string to
        # describe type

        if is_first:
            if date and place and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_date_place[gender][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_date_place[gender][date_full]
                else:
                    text = relationship_first_date_place[gender][date_full]
            elif date and place:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_date_place["succinct"][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_date_place["succinct"][date_full]
                else:
                    text = relationship_first_date_place["succinct"][date_full]
            elif date and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_date[gender][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_date[gender][date_full]
                else:
                    text = relationship_first_date[gender][date_full]
            elif date:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_date["succinct"][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_date["succinct"][date_full]
                else:
                    text = relationship_first_date["succinct"][date_full]
            elif place and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_place[gender]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_place[gender]
                else:
                    text = relationship_first_place[gender]
            elif place:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_place["succinct"]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_place["succinct"]
                else:
                    text = relationship_first_place["succinct"]
            elif self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_only[gender]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_only[gender]
                else:
                    text = relationship_first_only[gender]
            else:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_first_only["succinct"]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_first_only["succinct"]
                else:
                    text = relationship_first_only["succinct"]
        else:
            if date and place and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_date_place[gender][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_date_place[gender][date_full]
                else:
                    text = relationship_also_date_place[gender][date_full]
            elif date and place:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_date_place["succinct"][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_date_place["succinct"][date_full]
                else:
                    text = relationship_also_date_place["succinct"][date_full]
            elif date and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_date[gender][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_date[gender][date_full]
                else:
                    text = relationship_also_date[gender][date_full]
            elif date:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_date["succinct"][date_full]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_date["succinct"][date_full]
                else:
                    text = relationship_also_date["succinct"][date_full]
            elif place and self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_place[gender]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_place[gender]
                else:
                    text = relationship_also_place[gender]
            elif place:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_place["succinct"]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_place["succinct"]
                else:
                    text = relationship_also_place["succinct"]
            elif self.__verbose:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_only[gender]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_only[gender]
                else:
                    text = relationship_also_only[gender]
            else:
                if relationship == FamilyRelType.MARRIED:
                    text = marriage_also_only["succinct"]
                elif relationship == FamilyRelType.UNMARRIED:
                    text = unmarried_also_only["succinct"]
                else:
                    text = relationship_also_only["succinct"]

        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "
        return text

    def get_child_string(self, father_name="", mother_name="", gender=""):
        """
        Get a string narrating the relationship to the parents of the subject.
        Missing information will be omitted without loss of readability.
        Example sentences:
            Person was de zoon van father_name and mother_name.
            Person was de dochter van father_name and mother_name.
            ""

        :param father_name: The name of the Subjects' father.
        :type father_name: unicode
        :param mother_name: The name of the Subjects' mother.
        :type mother_name: unicode
        :returns: A sentence about the subject's parents.
        :rtype: unicode
        """

        value_map = {
            "father": father_name,
            "mother": mother_name,
            "male_name": self.__first_name,
            "name": self.__first_name,
            "female_name": self.__first_name,
            "unknown_gender_name": self.__first_name,
        }

        dead = not probably_alive(self.__person, self.__db)

        if not self.__first_name_used:
            index = _NAME_INDEX_INCLUDE_NAME
            self.__first_name_used = True
        else:
            index = _NAME_INDEX_EXCLUDE_NAME
        
        if gender == "":
            gender = self.__get_gender()

        text = ""
        if mother_name and father_name and self.__verbose:
            text = child_father_mother[gender][index][dead]
        elif mother_name and father_name:
            text = child_father_mother[gender][2]
        elif mother_name and self.__verbose:
            text = child_mother[gender][index][dead]
        elif mother_name:
            text = child_mother[gender][2]
        elif father_name and self.__verbose:
            text = child_father[gender][index][dead]
        elif father_name:
            text = child_father[gender][2]

        if text:
            text = self.__translate_text(text) % value_map
            text = text + " "

        return text

    def __get_gender(self):
        """
        Return a gender to be used for translations.
        """
        gender = self.__person.get_gender()
        if gender == Person.OTHER:
            gender = Person.UNKNOWN
        return gender

    def __get_age_at_death(self):
        """
        Calculate the age the person died.

        Returns a tuple representing (age, age_index).
        """
        birth_ref = self.__person.get_birth_ref()
        if birth_ref:
            birth_event = self.__db.get_event_from_handle(birth_ref.ref)
            birth = birth_event.get_date_object()
            birth_year_valid = birth.get_year_valid()
        else:
            birth_year_valid = False
        death_ref = self.__person.get_death_ref()
        if death_ref:
            death_event = self.__db.get_event_from_handle(death_ref.ref)
            death = death_event.get_date_object()
            death_year_valid = death.get_year_valid()
        else:
            death_year_valid = False

        # without at least a year for each event no age can be calculated
        if birth_year_valid and death_year_valid:
            span = death - birth
            if span and span.is_valid():
                if span:
                    age = span.get_repr(dlocale=self._locale)
                    age_index = _AGE_INDEX
                else:
                    age = 0
                    age_index = _AGE_INDEX_NO_AGE
            else:
                age = 0
                age_index = _AGE_INDEX_NO_AGE
        else:
            age = 0
            age_index = _AGE_INDEX_NO_AGE

        return age, age_index
