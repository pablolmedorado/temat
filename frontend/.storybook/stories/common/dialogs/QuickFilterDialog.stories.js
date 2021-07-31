import { action } from "@storybook/addon-actions";

import QuickFilterDialog from "@/components/dialogs/QuickFilterDialog";

export default {
  title: "Components/Common/Dialogs/QuickFilterDialog",
  component: QuickFilterDialog,
  args: {
    quickFilters: [{ label: "Dummy filter", filters: { name__icontains: "acme" } }],
  },
  argTypes: {
    scrollable: { table: { disable: true } },
    persistent: { table: { disable: true } },
    maxWidth: { table: { disable: true } },
  },
};

const Template = (args, { argTypes }) => ({
  components: { QuickFilterDialog },
  props: Object.keys(argTypes),
  data() {
    return {
      showDialog: true,
    };
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue) {
        this.showDialog = newValue;
      },
    },
  },
  methods: {
    addQuickFilter: action("addQuickFilter"),
  },
  template: `
    <div>
      <v-btn color="primary" @click="showDialog = true">Open dialog</v-btn>
      <QuickFilterDialog
        v-model="showDialog"
        v-bind="$props"
        @add:quick-filter="addQuickFilter"
      />
    </div>
  `,
});

export const Default = Template.bind({});
