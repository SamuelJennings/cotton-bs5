"""
Unit tests for Cotton BS5 components.
Tests for accessibility, slot functionality, and attribute handling.
"""

from django.template import Context, Template
from django.test import TestCase
from django_cotton.compiler_regex import CottonCompiler


class CottonBS5ComponentTests(TestCase):
    """Test suite for Cotton BS5 components."""

    def setUp(self):
        super().setUp()
        self.compiler = CottonCompiler()

    def render_template(self, template_string, context=None):
        """Helper method to render a template string with context."""
        if context is None:
            context = {}
        template = self.compiler.process(template_string)
        return Template(template).render(Context(context))

    def assertNotInHTML(self, needle, haystack):
        """Assert that needle is not found in the HTML haystack."""
        self.assertNotIn(needle, haystack)

    def assertInHTML(self, needle, haystack):
        """Assert that needle is found in the HTML haystack."""
        self.assertIn(needle, haystack)

    def assertAttributeExists(self, attr, html):
        """Assert that an attribute exists in the HTML haystack."""
        self.assertIn(f" {attr}", html)

    def assertAttributeNotExist(self, attr, html):
        """Assert that an attribute does not exist in the HTML haystack."""
        self.assertNotIn(f" {attr}", html)


class SpinnerComponentTests(CottonBS5ComponentTests):
    """Tests for spinner component."""

    def test_spinner_basic_rendering(self):
        """Test basic spinner rendering."""
        template_str = "<c-spinner />"
        rendered = self.render_template(template_str)

        self.assertInHTML("spinner-border", rendered)
        self.assertInHTML('role="status"', rendered)
        self.assertInHTML("visually-hidden", rendered)
        self.assertInHTML("Loading", rendered)

    def test_spinner_custom_type(self):
        """Test spinner with custom type."""
        template_str = '<c-spinner type="grow" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("spinner-grow", rendered)
        self.assertNotInHTML("spinner-border", rendered)

    def test_spinner_custom_size(self):
        """Test spinner with custom size."""
        template_str = '<c-spinner size="sm" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("spinner-border-sm", rendered)

    def test_spinner_custom_variant(self):
        """Test spinner with variant."""
        template_str = '<c-spinner variant="primary" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("text-primary", rendered)

    def test_spinner_custom_label(self):
        """Test spinner with custom label."""
        template_str = '<c-spinner label="Custom loading text" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("Custom loading text", rendered)

    def test_spinner_slot_content(self):
        """Test spinner with slot content."""
        template_str = "<c-spinner>Custom content</c-spinner>"
        rendered = self.render_template(template_str)

        self.assertInHTML("Custom content", rendered)

    def test_spinner_no_erroneous_attributes(self):
        """Test that spinner doesn't add variables as HTML attributes."""
        template_str = '<c-spinner type="border" size="sm" variant="primary" label="Test" />'
        rendered = self.render_template(template_str)

        # These should NOT appear as HTML attributes
        self.assertAttributeNotExist('type="border"', rendered)
        self.assertAttributeNotExist('size="sm"', rendered)
        self.assertAttributeNotExist('variant="primary"', rendered)
        self.assertAttributeNotExist('label="Test"', rendered)

    def test_spinner_class_attribute(self):
        """Test spinner with custom class."""
        template_str = '<c-spinner class="my-custom-class" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("my-custom-class", rendered)
        self.assertAttributeNotExist('class="my-custom-class"', rendered)  # Should be merged, not duplicated


class AlertComponentTests(CottonBS5ComponentTests):
    """Tests for alert component."""

    def test_alert_basic_rendering(self):
        """Test basic alert rendering."""
        template_str = '<c-alert text="Test message" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("alert", rendered)
        self.assertInHTML("alert-primary", rendered)  # default variant
        self.assertInHTML('role="alert"', rendered)
        self.assertInHTML("Test message", rendered)

    def test_alert_variant(self):
        """Test alert with different variant."""
        template_str = '<c-alert variant="danger" text="Error message" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("alert-danger", rendered)
        self.assertNotInHTML("alert-primary", rendered)

    def test_alert_dismissible(self):
        """Test dismissible alert."""
        template_str = '<c-alert text="Test" dismissible />'
        rendered = self.render_template(template_str)

        self.assertInHTML("alert-dismissible", rendered)
        self.assertInHTML("btn-close", rendered)

    def test_alert_slot_content(self):
        """Test alert with slot content."""
        template_str = "<c-alert>Slot content</c-alert>"
        rendered = self.render_template(template_str)

        self.assertInHTML("Slot content", rendered)

    def test_alert_text_and_slot(self):
        """Test alert with both text and slot content."""
        template_str = '<c-alert text="Text content">Slot content</c-alert>'
        rendered = self.render_template(template_str)

        self.assertInHTML("Text content", rendered)
        self.assertInHTML("Slot content", rendered)

    def test_alert_no_erroneous_attributes(self):
        """Test that alert doesn't add variables as HTML attributes."""
        template_str = '<c-alert variant="danger" text="Test" animate dismissible />'
        rendered = self.render_template(template_str)

        # These should NOT appear as HTML attributes
        self.assertAttributeNotExist('variant="danger"', rendered)
        self.assertAttributeNotExist('text="Test"', rendered)
        self.assertAttributeNotExist("animate", rendered)
        self.assertAttributeNotExist("dismissible", rendered)


class ButtonComponentTests(CottonBS5ComponentTests):
    """Tests for button component."""

    def test_button_basic_rendering(self):
        """Test basic button rendering."""
        template_str = '<c-button text="Click me" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("<button", rendered)
        self.assertInHTML("btn", rendered)
        self.assertInHTML("btn-primary", rendered)  # default variant
        self.assertInHTML("Click me", rendered)

    def test_button_as_link(self):
        """Test button rendered as link."""
        template_str = '<c-button href="/test/" text="Link button" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("<a", rendered)
        self.assertInHTML('href="/test/"', rendered)
        self.assertNotInHTML("<button", rendered)

    def test_button_variant(self):
        """Test button with different variant."""
        template_str = '<c-button variant="danger" text="Delete" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-danger", rendered)
        self.assertNotInHTML("btn-primary", rendered)

    def test_button_outline(self):
        """Test outline button."""
        template_str = '<c-button variant="primary" outline text="Outline" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-outline-primary", rendered)
        self.assertNotInHTML("btn-primary", rendered)

    def test_button_size(self):
        """Test button with size."""
        template_str = '<c-button size="lg" text="Large button" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-lg", rendered)

    def test_button_slot_priority(self):
        """Test that slot content takes priority over text."""
        template_str = '<c-button text="This should not show">Slot content</c-button>'
        rendered = self.render_template(template_str)

        self.assertInHTML("Slot content", rendered)
        self.assertNotInHTML("This should not show", rendered)

    def test_button_no_erroneous_attributes(self):
        """Test that button doesn't add variables as HTML attributes."""
        template_str = '<c-button variant="danger" size="lg" outline text="Test" />'
        rendered = self.render_template(template_str)

        # These should NOT appear as HTML attributes because they're declared in c-vars
        self.assertAttributeNotExist('variant="danger"', rendered)
        self.assertAttributeNotExist('size="lg"', rendered)
        self.assertAttributeNotExist("outline", rendered)
        self.assertAttributeNotExist('text="Test"', rendered)


class ProgressComponentTests(CottonBS5ComponentTests):
    """Tests for progress component."""

    def test_progress_basic_rendering(self):
        """Test basic progress rendering."""
        template_str = '<c-progress value="50" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("progress", rendered)
        self.assertInHTML('role="progressbar"', rendered)
        self.assertInHTML('aria-valuenow="50"', rendered)
        self.assertInHTML('aria-valuemin="0"', rendered)
        self.assertInHTML('aria-valuemax="100"', rendered)

    def test_progress_custom_min_max(self):
        """Test progress with custom min/max."""
        template_str = '<c-progress value="25" min="10" max="50" />'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-valuemin="10"', rendered)
        self.assertInHTML('aria-valuemax="50"', rendered)

    def test_progress_variant(self):
        """Test progress with variant."""
        template_str = '<c-progress value="50" variant="success" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("bg-success", rendered)

    def test_progress_striped(self):
        """Test striped progress."""
        template_str = '<c-progress value="50" striped />'
        rendered = self.render_template(template_str)

        self.assertInHTML("progress-bar-striped", rendered)

    def test_progress_animated(self):
        """Test animated progress."""
        template_str = '<c-progress value="50" animated />'
        rendered = self.render_template(template_str)

        self.assertInHTML("progress-bar-animated", rendered)

    def test_progress_text_content(self):
        """Test progress with text content."""
        template_str = '<c-progress value="75" text="75%" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("75%", rendered)

    def test_progress_slot_content(self):
        """Test progress with slot content."""
        template_str = '<c-progress value="50">Custom content</c-progress>'
        rendered = self.render_template(template_str)

        self.assertInHTML("Custom content", rendered)

    def test_progress_aria_label(self):
        """Test progress aria-label."""
        template_str = '<c-progress value="50" label="Custom progress label" />'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-label="Custom progress label"', rendered)

    def test_progress_no_erroneous_attributes(self):
        """Test that progress doesn't add variables as HTML attributes."""
        template_str = (
            '<c-progress value="50" min="0" max="100" variant="success" striped animated text="50%" label="Test" />'
        )
        rendered = self.render_template(template_str)

        # Check that values are used in ARIA attributes correctly
        self.assertAttributeExists('aria-valuenow="50"', rendered)
        self.assertAttributeExists('aria-valuemin="0"', rendered)
        self.assertAttributeExists('aria-valuemax="100"', rendered)
        self.assertAttributeExists('aria-label="Test"', rendered)

        # These should NOT appear as HTML attributes because they're declared in c-vars
        self.assertAttributeNotExist('value="50"', rendered)
        self.assertAttributeNotExist('min="0"', rendered)
        self.assertAttributeNotExist('max="100"', rendered)
        self.assertAttributeNotExist('variant="success"', rendered)
        self.assertAttributeNotExist('text="50%"', rendered)
        self.assertAttributeNotExist('label="Test"', rendered)
        self.assertAttributeNotExist("striped", rendered)
        self.assertAttributeNotExist("animated", rendered)


class BreadcrumbsComponentTests(CottonBS5ComponentTests):
    """Tests for breadcrumbs components."""

    def test_breadcrumbs_basic_rendering(self):
        """Test basic breadcrumbs rendering."""
        template_str = """
        <c-breadcrumbs>
            <c-breadcrumbs.item href="/home/" text="Home" />
            <c-breadcrumbs.item text="Current Page" />
        </c-breadcrumbs>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("<nav", rendered)
        self.assertInHTML("aria-label=", rendered)
        self.assertInHTML("breadcrumb", rendered)
        self.assertInHTML("breadcrumb-item", rendered)

    def test_breadcrumbs_custom_divider(self):
        """Test breadcrumbs with custom divider."""
        template_str = """
        <c-breadcrumbs divider=">">
            <c-breadcrumbs.item href="/home/" text="Home" />
        </c-breadcrumbs>"""
        rendered = self.render_template(template_str)

        # Check for custom divider in CSS (may be encoded differently)
        divider_found = (
            "--bs-breadcrumb-divider: '>'" in rendered
            or "--bs-breadcrumb-divider: '&gt;'" in rendered
            or '--bs-breadcrumb-divider: "&gt;"' in rendered
            or '--bs-breadcrumb-divider: ">"' in rendered
        )
        self.assertTrue(divider_found, f"Custom divider CSS not found in: {rendered}")

    def test_breadcrumb_item_link(self):
        """Test breadcrumb item as link."""
        template_str = '<c-breadcrumbs.item href="/test/" text="Test Page" />'
        rendered = self.render_template(template_str)

        self.assertInHTML('<a href="/test/"', rendered)
        self.assertInHTML("Test Page", rendered)
        self.assertNotInHTML("active", rendered)

    def test_breadcrumb_item_active(self):
        """Test active breadcrumb item."""
        template_str = '<c-breadcrumbs.item text="Current Page" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("active", rendered)
        self.assertInHTML('aria-current="page"', rendered)
        self.assertNotInHTML("<a", rendered)

    def test_breadcrumb_item_slot_content(self):
        """Test breadcrumb item with slot content."""
        template_str = '<c-breadcrumbs.item href="/test/">Slot content</c-breadcrumbs.item>'
        rendered = self.render_template(template_str)

        self.assertInHTML("Slot content", rendered)


class CardComponentTests(CottonBS5ComponentTests):
    """Tests for card components."""

    def test_card_basic_rendering(self):
        """Test basic card rendering."""
        template_str = """
        <c-card>
            <c-card.body>Card content</c-card.body>
        </c-card>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("card", rendered)
        self.assertInHTML("card-body", rendered)
        self.assertInHTML("Card content", rendered)

    def test_card_title_default_level(self):
        """Test card title with default heading level."""
        template_str = '<c-card.title text="Card Title" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("<h5", rendered)
        self.assertInHTML("card-title", rendered)
        self.assertInHTML("Card Title", rendered)

    def test_card_title_custom_level(self):
        """Test card title with custom heading level."""
        template_str = '<c-card.title level="2" text="Card Title" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("<h2", rendered)
        self.assertInHTML("</h2>", rendered)
        self.assertNotInHTML("<h5", rendered)

    def test_card_title_slot_content(self):
        """Test card title with slot content."""
        template_str = "<c-card.title>Slot title content</c-card.title>"
        rendered = self.render_template(template_str)

        self.assertInHTML("Slot title content", rendered)

    def test_card_title_no_erroneous_attributes(self):
        """Test that card title doesn't add variables as HTML attributes."""
        template_str = '<c-card.title level="3" text="Title" class="custom-class" />'
        rendered = self.render_template(template_str)

        # These should NOT appear as HTML attributes
        self.assertAttributeNotExist('level="3"', rendered)
        self.assertAttributeNotExist('text="Title"', rendered)


class TableComponentTests(CottonBS5ComponentTests):
    """Tests for table component."""

    def test_table_basic_rendering(self):
        """Test basic table rendering."""
        template_str = """
        <c-table>
            <thead><tr><th>Header</th></tr></thead>
            <tbody><tr><td>Data</td></tr></tbody>
        </c-table>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("table", rendered)
        self.assertInHTML("table-responsive", rendered)
        self.assertInHTML("<thead>", rendered)
        self.assertInHTML("<tbody>", rendered)

    def test_table_striped(self):
        """Test striped table."""
        template_str = "<c-table striped>Content</c-table>"
        rendered = self.render_template(template_str)

        self.assertInHTML("table-striped", rendered)

    def test_table_bordered(self):
        """Test bordered table."""
        template_str = "<c-table bordered>Content</c-table>"
        rendered = self.render_template(template_str)

        self.assertInHTML("table-bordered", rendered)

    def test_table_hover(self):
        """Test hover table."""
        template_str = "<c-table hover>Content</c-table>"
        rendered = self.render_template(template_str)

        self.assertInHTML("table-hover", rendered)

    def test_table_small(self):
        """Test small table."""
        template_str = "<c-table small>Content</c-table>"
        rendered = self.render_template(template_str)

        self.assertInHTML("table-sm", rendered)

    def test_table_variant(self):
        """Test table with variant."""
        template_str = '<c-table variant="dark">Content</c-table>'
        rendered = self.render_template(template_str)

        self.assertInHTML("table-dark", rendered)

    def test_table_responsive(self):
        """Test responsive table."""
        template_str = '<c-table responsive="lg">Content</c-table>'
        rendered = self.render_template(template_str)

        self.assertInHTML("table-responsive-lg", rendered)

    def test_table_caption(self):
        """Test table with caption."""
        template_str = '<c-table caption="Table caption">Content</c-table>'
        rendered = self.render_template(template_str)

        self.assertInHTML("<caption>Table caption</caption>", rendered)

    def test_table_no_erroneous_attributes(self):
        """Test that table doesn't add variables as HTML attributes."""
        template_str = '<c-table striped bordered hover small variant="dark" responsive="lg" caption="Test" />'
        rendered = self.render_template(template_str)

        # These should NOT appear as HTML attributes
        self.assertAttributeNotExist("striped", rendered)
        self.assertAttributeNotExist("bordered", rendered)
        self.assertAttributeNotExist("hover", rendered)
        self.assertAttributeNotExist("small", rendered)
        self.assertAttributeNotExist('variant="dark"', rendered)
        self.assertAttributeNotExist('responsive="lg"', rendered)
        self.assertAttributeNotExist('caption="Test"', rendered)


class TabsComponentTests(CottonBS5ComponentTests):
    """Tests for tabs components."""

    def test_tabs_basic_rendering(self):
        """Test basic tabs rendering."""
        template_str = """
        <c-tabs id="testTabs">
            <c-tabs.item target="tab1" text="Tab 1" />
            <c-tabs.item target="tab2" text="Tab 2" />
        </c-tabs>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("nav", rendered)
        self.assertInHTML('role="tablist"', rendered)
        self.assertInHTML("nav-item", rendered)
        self.assertInHTML('role="presentation"', rendered)

    def test_tabs_vertical(self):
        """Test vertical tabs."""
        template_str = """
        <c-tabs vertical>
            <c-tabs.item target="tab1" text="Tab 1" />
        </c-tabs>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("flex-column", rendered)
        self.assertInHTML('aria-orientation="vertical"', rendered)

    def test_tabs_item_active(self):
        """Test active tab item."""
        template_str = '<c-tabs.item target="tab1" text="Tab 1" active />'
        rendered = self.render_template(template_str)

        self.assertInHTML("active", rendered)
        self.assertInHTML('aria-selected="true"', rendered)
        self.assertInHTML('tabindex="0"', rendered)

    def test_tabs_item_inactive(self):
        """Test inactive tab item."""
        template_str = '<c-tabs.item target="tab2" text="Tab 2" />'
        rendered = self.render_template(template_str)

        self.assertNotInHTML("active", rendered)
        self.assertInHTML('aria-selected="false"', rendered)
        self.assertInHTML('tabindex="-1"', rendered)

    def test_tabs_pane_active(self):
        """Test active tab pane."""
        template_str = '<c-tabs.pane id="tab1" active>Content 1</c-tabs.pane>'
        rendered = self.render_template(template_str)

        self.assertInHTML("tab-pane", rendered)
        self.assertInHTML("active", rendered)
        self.assertInHTML('role="tabpanel"', rendered)
        self.assertInHTML('aria-labelledby="tab1-tab"', rendered)
        self.assertInHTML('tabindex="0"', rendered)

    def test_tabs_pane_inactive(self):
        """Test inactive tab pane."""
        template_str = '<c-tabs.pane id="tab2">Content 2</c-tabs.pane>'
        rendered = self.render_template(template_str)

        self.assertNotInHTML("active", rendered)
        self.assertInHTML('tabindex="-1"', rendered)

    def test_tabs_no_erroneous_attributes_active(self):
        """Test that tabs don't add variables as HTML attributes."""
        template_str = '<c-tabs.item target="tab1" text="Tab 1" active />'
        rendered = self.render_template(template_str)

        # Check that the tab is properly rendered with expected attributes
        self.assertInHTML('data-bs-target="#tab1"', rendered)  # target becomes data-bs-target
        self.assertInHTML("Tab 1", rendered)  # text content appears
        self.assertInHTML("active", rendered)  # active state appears in class
        self.assertInHTML('tabindex="0"', rendered)  # disabled creates tabindex

        # These should NOT appear as HTML attributes because they're declared in c-vars
        self.assertAttributeNotExist('target="tab1"', rendered)
        self.assertAttributeNotExist('text="Tab 1"', rendered)
        self.assertAttributeNotExist("disabled", rendered)

    def test_tabs_no_erroneous_attributes_disabled(self):
        template_str = '<c-tabs.item target="tab1" text="Tab 1" disabled />'
        rendered = self.render_template(template_str)

        # Check that the tab is properly rendered with expected attributes
        self.assertInHTML('data-bs-target="#tab1"', rendered)  # target becomes data-bs-target
        self.assertInHTML("Tab 1", rendered)  # text content appears
        self.assertInHTML("disabled", rendered)  # active state appears in class
        self.assertInHTML('tabindex="-1"', rendered)  # disabled creates tabindex

        # These should NOT appear as HTML attributes because they're declared in c-vars
        self.assertAttributeNotExist('target="tab1"', rendered)
        self.assertAttributeNotExist('text="Tab 1"', rendered)
        self.assertAttributeNotExist("active", rendered)


class ModalComponentTests(CottonBS5ComponentTests):
    """Tests for modal components."""

    def test_modal_basic_rendering(self):
        """Test basic modal rendering."""
        template_str = """
        <c-modal id="testModal">
            <c-modal.title text="Modal Title" />
            <c-modal.body>Modal content</c-modal.body>
        </c-modal>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("modal", rendered)
        self.assertInHTML('id="testModal"', rendered)
        self.assertInHTML('aria-labelledby="testModalLabel"', rendered)
        self.assertInHTML('aria-hidden="true"', rendered)
        self.assertInHTML('tabindex="-1"', rendered)

    def test_modal_fade(self):
        """Test modal with fade."""
        template_str = '<c-modal id="test" fade>Content</c-modal>'
        rendered = self.render_template(template_str)

        self.assertInHTML("fade", rendered)

    def test_modal_centered(self):
        """Test centered modal."""
        template_str = '<c-modal id="test" centered>Content</c-modal>'
        rendered = self.render_template(template_str)

        self.assertInHTML("modal-dialog-centered", rendered)

    def test_modal_title(self):
        """Test modal title."""
        template_str = '<c-modal.title id="test" text="Modal Title" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("modal-title", rendered)
        self.assertInHTML('id="testLabel"', rendered)
        self.assertInHTML("Modal Title", rendered)


class AccordionComponentTests(CottonBS5ComponentTests):
    """Tests for accordion components."""

    def test_accordion_basic_rendering(self):
        """Test basic accordion rendering."""
        template_str = """
        <c-accordion id="testAccordion">
            <c-accordion.item text="Item 1" target="item1" parent="testAccordion">
                Content 1
            </c-accordion.item>
        </c-accordion>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("accordion", rendered)
        self.assertInHTML("accordion-item", rendered)
        self.assertInHTML("accordion-header", rendered)
        self.assertInHTML("accordion-button", rendered)

    def test_accordion_flush(self):
        """Test flush accordion."""
        template_str = "<c-accordion flush>Content</c-accordion>"
        rendered = self.render_template(template_str)

        self.assertInHTML("accordion-flush", rendered)

    def test_accordion_item_expanded(self):
        """Test expanded accordion item."""
        template_str = '<c-accordion.header target="test" text="Title" show />'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-expanded="true"', rendered)
        self.assertNotInHTML("collapsed", rendered)

    def test_accordion_item_collapsed(self):
        """Test collapsed accordion item."""
        template_str = '<c-accordion.header target="test" text="Title" />'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-expanded="false"', rendered)
        self.assertInHTML("collapsed", rendered)


class ListGroupComponentTests(CottonBS5ComponentTests):
    """Tests for list group components."""

    def test_list_group_basic_rendering(self):
        """Test basic list group rendering."""
        template_str = """
        <c-list_group>
            <c-list_group.item text="Item 1" />
            <c-list_group.item text="Item 2" />
        </c-list_group>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("list-group", rendered)
        self.assertInHTML("list-group-item", rendered)
        self.assertInHTML("<ul", rendered)

    def test_list_group_numbered(self):
        """Test numbered list group."""
        template_str = "<c-list_group numbered>Content</c-list_group>"
        rendered = self.render_template(template_str)

        self.assertInHTML("<ol", rendered)
        self.assertNotInHTML("<ul", rendered)

    def test_list_group_horizontal(self):
        """Test horizontal list group."""
        template_str = "<c-list_group horizontal>Content</c-list_group>"
        rendered = self.render_template(template_str)

        self.assertInHTML("list-group-horizontal", rendered)

    def test_list_group_item_active(self):
        """Test active list group item."""
        template_str = '<c-list_group.item text="Active Item" active />'
        rendered = self.render_template(template_str)

        self.assertInHTML("active", rendered)
        self.assertInHTML('aria-current="true"', rendered)

    def test_list_group_item_disabled(self):
        """Test disabled list group item."""
        template_str = '<c-list_group.item text="Disabled Item" disabled />'
        rendered = self.render_template(template_str)

        self.assertInHTML("disabled", rendered)
        self.assertInHTML('aria-disabled="true"', rendered)

    def test_list_group_item_as_link(self):
        """Test list group item as link."""
        template_str = '<c-list_group.item href="/test/" text="Link Item" />'
        rendered = self.render_template(template_str)

        self.assertInHTML("<a", rendered)
        self.assertInHTML('href="/test/"', rendered)
        self.assertInHTML("list-group-item-action", rendered)


class ButtonGroupComponentTests(CottonBS5ComponentTests):
    """Tests for button group component."""

    def test_button_group_basic_rendering(self):
        """Test basic button group rendering."""
        template_str = """
        <c-button_group>
            <c-button text="Button 1" />
            <c-button text="Button 2" />
        </c-button_group>"""
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-group", rendered)
        self.assertInHTML('role="group"', rendered)
        self.assertInHTML("aria-label=", rendered)

    def test_button_group_vertical(self):
        """Test vertical button group."""
        template_str = "<c-button_group vertical>Content</c-button_group>"
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-group-vertical", rendered)

    def test_button_group_size(self):
        """Test button group with size."""
        template_str = '<c-button_group size="lg">Content</c-button_group>'
        rendered = self.render_template(template_str)

        self.assertInHTML("btn-group-lg", rendered)

    def test_button_group_custom_label(self):
        """Test button group with custom label."""
        template_str = '<c-button_group label="Custom label">Content</c-button_group>'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-label="Custom label"', rendered)

    def test_button_group_no_erroneous_attributes(self):
        """Test that button group doesn't add variables as HTML attributes."""
        template_str = '<c-button_group size="lg" vertical label="Test" />'
        rendered = self.render_template(template_str)

        # Check that the values are used correctly
        self.assertInHTML("btn-group-lg", rendered)  # size becomes class
        self.assertInHTML("btn-group-vertical", rendered)  # vertical becomes class
        self.assertInHTML('aria-label="Test"', rendered)  # label becomes aria-label

        # These should NOT appear as HTML attributes because they're declared in c-vars
        self.assertAttributeNotExist('size="lg"', rendered)
        self.assertAttributeNotExist("vertical", rendered)
        self.assertAttributeNotExist('label="Test"', rendered)


class NavbarComponentTests(CottonBS5ComponentTests):
    """Tests for navbar components."""

    def test_navbar_basic_rendering(self):
        """Test basic navbar rendering."""
        template_str = '<c-navbar brand="Test Brand">Content</c-navbar>'
        rendered = self.render_template(template_str)

        self.assertInHTML("navbar", rendered)
        self.assertInHTML("navbar-brand", rendered)
        self.assertInHTML("Test Brand", rendered)

    def test_navbar_expand(self):
        """Test navbar with expand."""
        template_str = '<c-navbar expand="md" brand="Brand">Content</c-navbar>'
        rendered = self.render_template(template_str)

        self.assertInHTML("navbar-expand-md", rendered)
        self.assertInHTML("navbar-toggler", rendered)

    def test_navbar_toggle_button_accessibility(self):
        """Test navbar toggle button accessibility."""
        template_str = '<c-navbar expand="lg" brand="Brand">Content</c-navbar>'
        rendered = self.render_template(template_str)

        self.assertInHTML('aria-controls="navbarNav"', rendered)
        self.assertInHTML('aria-expanded="false"', rendered)
        self.assertIn("Toggle navigation", rendered)  # Should be translatable


if __name__ == "__main__":
    import os
    import sys

    import django

    # Configure Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    sys.path.insert(0, os.path.dirname(__file__))
    django.setup()

    # Run tests
    import unittest

    unittest.main()
