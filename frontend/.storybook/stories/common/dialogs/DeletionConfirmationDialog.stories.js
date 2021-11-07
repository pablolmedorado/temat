import { action } from "@storybook/addon-actions";

import DeletionConfirmationDialog from "@/components/dialogs/DeletionConfirmationDialog";

export default {
  title: "Components/Common/Dialogs/DeletionConfirmationDialog",
  component: DeletionConfirmationDialog,
  args: {
    data: undefined,
  },
  argTypes: {
    value: { table: { disable: true } },
    scrollable: { table: { disable: true } },
    persistent: { table: { disable: true } },
    maxWidth: { table: { disable: true } },
  },
};

const Template = (args, { argTypes }) => ({
  components: { DeletionConfirmationDialog },
  props: Object.keys(argTypes),
  mounted() {
    this.openDialog();
  },
  methods: {
    openDialog() {
      this.$refs.deleteDialog.open(this.data);
    },
    onDeleteConfirm: action("deleteConfirm"),
  },
  template: `
    <div>
      <v-btn color="error" @click="openDialog">Delete</v-btn>
      <DeletionConfirmationDialog
        ref="deleteDialog"
        v-bind="$props"
        @confirm="onDeleteConfirm"
      />
    </div>
  `,
});

export const Default = Template.bind({});
Default.args = {
  data: { name: "Item 1" },
};

export const Multiple = Template.bind({});
Multiple.args = {
  data: [{ name: "Item 1" }, { name: "Item 2" }],
};
