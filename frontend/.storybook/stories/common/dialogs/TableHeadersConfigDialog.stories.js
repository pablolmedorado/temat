// Utilities
import { storyFactory } from "../../../util/helpers";
import { action } from "@storybook/addon-actions";
import { object } from "@storybook/addon-knobs";

// Components
import TableHeadersConfigDialog from "@/components/common/dialogs/TableHeadersConfigDialog";

export default { title: "Components/Common/Dialogs/TableHeadersConfigDialog" };

const story = storyFactory({ TableHeadersConfigDialog });

export const Default = () => {
  return story({
    props: {
      availableHeaders: {
        default: object("Available headers", [
          { text: "Id", value: "id", fixed: true },
          { text: "Name", value: "name", default: true },
          { text: "Age", value: "age" },
          { text: "Telephone", value: "telephone" },
        ]),
      },
      headers: {
        default: object("Selected headers", [
          { text: "Id", value: "id" },
          { text: "Name", value: "name" },
          { text: "Age", value: "age" },
        ]),
      },
    },
    data() {
      return {
        showDialog: true,
      };
    },
    methods: {
      updateHeaders: action("updateHeaders"),
    },
    template: `
      <div>
        <v-btn color="primary" @click="showDialog = true">Open dialog</v-btn>
        <TableHeadersConfigDialog
          v-model="showDialog"
          :available-headers="availableHeaders"
          :headers="headers"
          @update:headers="updateHeaders($event)"
        />
      </div>
    `,
  });
};
