class CottonBS5ComponentMixin:
    """Mixin for Django class-based views to manage and merge component sections and their configurations.
    This mixin provides a mechanism to define, override, and merge UI component sections across a class hierarchy.
    It exposes methods to retrieve the merged section definitions, fetch per-section configuration, and build a context
    dictionary suitable for template rendering.
    Attributes:
        sections (dict): A mapping of section names to component names. Can be overridden in subclasses.
    Methods:
        get_component_sections():
            Walks the method resolution order (MRO) and merges all 'sections' dictionaries found in the class hierarchy.
            Subclass definitions override base class definitions.
        get_component_config(section_name):
            Retrieves configuration for a given section. Looks for an attribute named '{section_name}_config' or a method
            named 'get_{section_name}_config'. Returns an empty dict if neither is found.
        get_component_context():
            Constructs a dictionary mapping section names to their component configuration, suitable for use in templates.
            If a component name is falsy, it is returned as-is; otherwise, the configuration is merged with the component name.
        get_context_data(**kwargs):
            Extends the context data with a 'sections' key containing the component context for use in templates."""

    sections = {}
    layout = {}

    def get_component_sections(self):
        """
        Walks the MRO and merges all 'sections' definitions.
        Subclasses override base definitions.
        """
        return self._merge_config("sections")

    def get_component_config(self, section_name):
        """
        Merges section configuration from all base classes.
        Later definitions override earlier ones.
        """
        merged_config = {}
        attr_name = f"{section_name}_config"
        method_name = f"get_{section_name}_config"

        for base in reversed(self.__class__.__mro__):
            # Attribute-based config
            base_attr = getattr(base, attr_name, None)
            if isinstance(base_attr, dict):
                merged_config.update(base_attr)

            # Method-based config
            base_method = getattr(base, method_name, None)
            if callable(base_method):
                config = base_method(self) if base_method != getattr(self, method_name, None) else base_method()
                if isinstance(config, dict):
                    merged_config.update(config)

        return merged_config

    def get_component_context(self):
        """
        Returns a dict structured as:
        {
            section_name: {
                "component": component_name,
                "config": config_dict
            },
            ...
        }
        """
        context_sections = {}
        for section_name, component_name in self.get_component_sections().items():
            # if the component is Falsy, we return it as is.
            # This way existence can be checked in the template.
            if not component_name:
                context_sections[section_name] = component_name
            else:
                options = self.get_component_config(section_name)
                options.update({"is": component_name})
                context_sections[section_name] = options
        return context_sections

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sections"] = self.get_component_context()
        context["layout"] = self.get_layout()
        return context

    def get_layout(self):
        """
        Returns the layout configuration for the view.
        This can be overridden in subclasses to provide specific layout configurations.
        """
        return self._merge_config("layout")

    def _merge_config(self, attr):
        merged = {}
        for base in reversed(self.__class__.__mro__):
            base_val = getattr(base, attr, None)
            if isinstance(base_val, dict):
                merged.update(base_val)
        if hasattr(self, attr) and isinstance(getattr(self, attr), dict):
            merged.update(self.layout)
        return merged
