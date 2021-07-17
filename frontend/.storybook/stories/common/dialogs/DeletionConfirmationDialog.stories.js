// Utilities
import { storyFactory } from "../../../util/helpers";
import { action } from "@storybook/addon-actions";
import { boolean, object, text } from "@storybook/addon-knobs";

// Components
import DeletionConfirmationDialog from "@/components/dialogs/DeletionConfirmationDialog";

export default { title: "Components/Common/Dialogs/DeletionConfirmationDialog" };

const story = storyFactory({ DeletionConfirmationDialog });

const buildPropsData = () => ({
  itemText: {
    default: text("Descriptive field", "name"),
  },
  deleteChildItemsWarning: {
    default: boolean("Has children", false),
  },
});

const actionsData = {
  onDeleteConfirm: action("deleteConfirm"),
};

const template = `
  <div>
    <v-btn color="error" @click="openDialog">Delete item</v-btn>
    <DeletionConfirmationDialog
      ref="deleteDialog"
      :item-text="itemText"
      :delete-child-items-warning="deleteChildItemsWarning"
      @confirm="onDeleteConfirm"
    />
  </div>
`;

export const Default = () => {
  return story({
    props: {
      item: {
        default: object("Item", { name: "Item 1" }),
      },
      ...buildPropsData(),
    },
    mounted() {
      this.openDialog();
    },
    methods: {
      openDialog() {
        this.$refs.deleteDialog.open(this.item);
      },
      ...actionsData,
    },
    template,
  });
};

export const Multiple = () => {
  return story({
    props: {
      items: {
        default: object("Item", [{ name: "Item 1" }, { name: "Item 2" }]),
      },
      ...buildPropsData(),
    },
    mounted() {
      this.openDialog();
    },
    methods: {
      openDialog() {
        this.$refs.deleteDialog.open(this.items);
      },
      ...actionsData,
    },
    template,
  });
};
