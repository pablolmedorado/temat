import { action } from "@storybook/addon-actions";

import TableHeadersConfigDialog from "@/components/dialogs/TableHeadersConfigDialog";

export default {
  title: "Components/Common/Dialogs/TableHeadersConfigDialog",
  component: TableHeadersConfigDialog,
  args: {
    availableHeaders: [
      { text: "Id", value: "id", fixed: true },
      { text: "Name", value: "name", default: true },
      { text: "Age", value: "age" },
      { text: "Telephone", value: "telephone" },
    ],
    headers: [
      { text: "Id", value: "id" },
      { text: "Name", value: "name" },
      { text: "Age", value: "age" },
    ],
  },
  argTypes: {
    scrollable: { table: { disable: true } },
    persistent: { table: { disable: true } },
    maxWidth: { table: { disable: true } },
  },
};

const Template = (args, { argTypes }) => ({
  components: { TableHeadersConfigDialog },
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
    updateHeaders: action("updateHeaders"),
  },
  template: `
    <div>
      <v-btn color="primary" @click="showDialog = true">Open dialog</v-btn>
      <TableHeadersConfigDialog
        v-model="showDialog"
        v-bind="$props"
        @update:headers="updateHeaders"
      />
    </div>
  `,
});

export const Default = Template.bind({});
