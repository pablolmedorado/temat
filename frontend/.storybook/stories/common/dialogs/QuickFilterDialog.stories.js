// Utilities
import { storyFactory } from "../../../util/helpers";
import { action } from "@storybook/addon-actions";
import { object } from "@storybook/addon-knobs";

// Components
import QuickFilterDialog from "@/components/dialogs/QuickFilterDialog";

export default { title: "Components/Common/Dialogs/QuickFilterDialog" };

const story = storyFactory({ QuickFilterDialog });

export const Default = () => {
  return story({
    props: {
      customQuickFilters: {
        default: object("Quick filters", [{ label: "Dummy filter", filters: { name__icontains: "acme" } }]),
      },
    },
    data() {
      return {
        showDialog: true,
      };
    },
    methods: {
      addQuickFilter: action("addQuickFilter"),
    },
    template: `
      <div>
        <v-btn color="primary" @click="showDialog = true">Open dialog</v-btn>
        <QuickFilterDialog
          v-model="showDialog"
          :quick-filters="customQuickFilters"
          @add:quick-filter="addQuickFilter($event)"
        />
      </div>
    `,
  });
};
