"""Tests for SAGA algorithm and tool-group display names."""

from pathlib import Path
from unittest import TestCase

from ..processing.SagaNameDecorator import decoratedGroupName


class NameDecoratorTests(TestCase):
    """Tests for user-facing SAGA tool-group names."""

    def test_new_catalogue_groups_have_friendly_names(self):
        """Raw library identifiers introduced after SAGA 9.2 are categorized."""
        expected_groups = {
            "group_files": "Import/Export",
            "imagery": "Imagery",
            "polygon_tools": "Features",
            "sim_air_flow": "Simulation",
            "sim_cellular_automata": "Simulation",
            "sim_ecosystems_hugget": "Simulation",
            "sim_erosion": "Simulation",
            "sim_fire_spreading": "Simulation",
            "sim_geomorphology": "Simulation",
            "sim_hydrology": "Simulation",
            "sim_landscape_evolution": "Simulation",
            "sim_qm_of_esp": "Simulation",
            "sim_rivflow": "Simulation",
            "terrain_analysis": "Terrain Analysis",
            "toolchains": "Tool Chains",
        }

        for raw_name, display_name in expected_groups.items():
            with self.subTest(raw_name=raw_name):
                self.assertEqual(display_name, decoratedGroupName(raw_name))

    def test_unknown_library_identifiers_are_humanized(self):
        """Future SAGA identifiers do not appear as raw underscore names."""
        self.assertEqual(
            "Future Tool Library", decoratedGroupName("future_tool_library")
        )
        self.assertEqual("Already Friendly", decoratedGroupName("Already Friendly"))

    def test_catalogue_contains_no_raw_group_display_names(self):
        """Every current catalogue group has a user-friendly display name."""
        description_path = Path(__file__).parents[1] / "description"
        raw_groups = set()

        for description_file in description_path.glob("*.txt"):
            with description_file.open(encoding="utf-8") as stream:
                stream.readline()
                group = stream.readline().strip()
                if group == "##known_issues":
                    group = stream.readline().strip()
                raw_groups.add(group)

        undecorated = {
            group
            for group in raw_groups
            if "_" in group and decoratedGroupName(group) == group
        }
        self.assertEqual(set(), undecorated)
